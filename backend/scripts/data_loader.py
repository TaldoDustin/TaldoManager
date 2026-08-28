import json

from app.domain.jogador import Jogador
from app.domain.clube import Clube
from app.domain.campeonato import Campeonato

def carregar_jogadores():

    with open(
        "data/seeds/jogadores.json",
        encoding="utf-8"
    ) as arquivo:

        dados = json.load(arquivo)

    jogadores = {}

    for j in dados:

        jogadores[j["id"]] = Jogador(
            j["nome"],
            j["idade"],
            j["posicao"],
            j["overall"]
        )

    return jogadores

def carregar_clubes(jogadores):

    with open(
        "data/seeds/clubes.json",
        encoding="utf-8"
    ) as arquivo:

        dados = json.load(
            arquivo
        )

    clubes = []

    for c in dados:

        clube = Clube(
            c["nome"],
            c["pais"],
            c["dinheiro"],
            c["torcedores"]
        )

        for id_jogador in c["titulares"]:

            clube.contratar_jogador(
                jogadores[id_jogador]
            )

        for id_jogador in c["reservas"]:

            clube.contratar_reserva(
                jogadores[id_jogador]
            )

        clubes.append(
            clube
        )

        print(
            clube.nome,
            len(clube.jogadores),
            len(clube.titulares),
            len(clube.reservas)
        )


    return clubes

def carregar_campeonato():

    jogadores = carregar_jogadores()

    clubes = carregar_clubes(jogadores)

    return Campeonato(
        "Taldo",
        clubes
    )