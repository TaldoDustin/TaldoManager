from app.domain.jogador import Jogador


def test_criar_jogador():
    jogador = Jogador(
        "Louis Silva",
        25,
        "Atacante",
        85
    )

    assert jogador.nome == "Louis Silva"
    assert jogador.idade == 25
    assert jogador.posicao == "Atacante"
    assert jogador.overall == 85

def test_nota_media_sem_partidas():
    jogador = Jogador(
        "Teste",
        25,
        "Atacante",
        80
    )

    assert jogador.nota_media() == 0.0


def test_nota_media_com_partidas():
    jogador = Jogador(
        "Teste",
        25,
        "Atacante",
        80
    )

    jogador.partidas = 3
    jogador.soma_nota = 24.75

    assert jogador.nota_media() == 8.25
    
def test_score_escalacao_normal():
    jogador = Jogador(
        "Teste",
        25,
        "Atacante",
        80
    )

    jogador.energia = 100
    jogador.condicao = "Normal"

    assert jogador.score_escalacao() == 95.0


def test_score_escalacao_cansado():
    jogador = Jogador(
        "Teste",
        25,
        "Atacante",
        80
    )

    jogador.energia = 60
    jogador.condicao = "Cansado"

    assert jogador.score_escalacao() == 84.0


def test_score_escalacao_exausto():
    jogador = Jogador(
        "Teste",
        25,
        "Atacante",
        80
    )

    jogador.energia = 30
    jogador.condicao = "Exausto"

    assert jogador.score_escalacao() == 69.5

def test_peso_gol_goleiro_e_defesa():
    goleiro = Jogador("Goleiro", 25, "Goleiro", 80)
    defesa = Jogador("Defesa", 25, "Defesa", 80)

    assert goleiro.peso_gol() == 0
    assert defesa.peso_gol() == 0


def test_peso_gol_meio_campo():
    jogador = Jogador(
        "Meia",
        25,
        "Meio-Campo",
        90
    )

    assert jogador.peso_gol() == 13


def test_peso_gol_atacante():
    jogador = Jogador(
        "Atacante",
        25,
        "Atacante",
        90
    )

    assert jogador.peso_gol() == 18


def test_peso_gol_considera_condicao():
    jogador = Jogador(
        "Atacante",
        25,
        "Atacante",
        90
    )

    jogador.condicao = "Cansado"

    assert jogador.peso_gol() == 16

    jogador.condicao = "Exausto"

    assert jogador.peso_gol() == 12

def test_peso_assistencia_goleiro():
    jogador = Jogador(
        "Goleiro",
        25,
        "Goleiro",
        90
    )

    assert jogador.peso_assistencia() == 1


def test_peso_assistencia_por_posicao():
    atacante = Jogador("Atacante", 25, "Atacante", 80)
    meia = Jogador("Meia", 25, "Meio-Campo", 80)
    defesa = Jogador("Defesa", 25, "Defesa", 80)

    assert atacante.peso_assistencia() == 17
    assert meia.peso_assistencia() == 23
    assert defesa.peso_assistencia() == 12


def test_peso_assistencia_considera_condicao():
    jogador = Jogador(
        "Meia",
        25,
        "Meio-Campo",
        80
    )

    jogador.condicao = "Cansado"

    assert jogador.peso_assistencia() == 20

    jogador.condicao = "Exausto"

    assert jogador.peso_assistencia() == 16
    
def test_resetar_estatisticas_partida():
    jogador = Jogador(
        "Teste",
        25,
        "Atacante",
        80
    )

    jogador.chutes_partida = 5
    jogador.chutes_gol_partida = 3
    jogador.passes_chave_partida = 2
    jogador.dribles_partida = 4
    jogador.desarmes_partida = 3
    jogador.interceptacoes_partida = 2
    jogador.cortes_partida = 1
    jogador.bloqueios_partida = 2
    jogador.defesas_partida = 1
    jogador.gols_sofridos_partida = 2
    jogador.faltas_partida = 4
    jogador.amarelos_partida = 1
    jogador.expulso = True

    jogador.resetar_estatisticas_partida()

    assert jogador.chutes_partida == 0
    assert jogador.chutes_gol_partida == 0
    assert jogador.passes_chave_partida == 0
    assert jogador.dribles_partida == 0
    assert jogador.desarmes_partida == 0
    assert jogador.interceptacoes_partida == 0
    assert jogador.cortes_partida == 0
    assert jogador.bloqueios_partida == 0
    assert jogador.defesas_partida == 0
    assert jogador.gols_sofridos_partida == 0
    assert jogador.faltas_partida == 0
    assert jogador.amarelos_partida == 0
    assert jogador.expulso is False
    