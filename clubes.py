class Clube:
    def __init__(
        self,
        nome,
        pais,
        dinheiro,
        torcedores=0
    ):
        self.nome = nome
        self.pais = pais
        self.dinheiro = dinheiro
        self.torcedores = torcedores

        self.jogadores = []
        self.titulares = []
        self.reservas = []
        self.formacao = "4-3-3"

        self.pontos = 0
        self.gols_marcados = 0
        self.gols_sofridos = 0

        self.vitorias = 0
        self.empates = 0
        self.derrotas = 0

        self.forma = []
        
        self.penalidade_expulsao = 0
        
    def atualizar_forma(self, resultado):

        self.forma.append(resultado)

        if len(self.forma) > 5:
            self.forma.pop(0)
    
    def bonus_forma(self):

        bonus = 0

        for resultado in self.forma:

            if resultado == "V":
                bonus += 0.5

            elif resultado == "D":
                bonus -= 0.5

        return bonus
    
    def mostrar(self):
        print(f"\nClube: {self.nome}")
        print(f"País: {self.pais}")
        print(f"Dinheiro: {self.dinheiro}")
        print("\nElenco:")
        for jogador in self.jogadores:
            print(f"- {jogador.nome} ({jogador.overall})")
            
    def mostrar_partida(self):
        print(f"\nClube: {self.nome}")
        print(f"Força: {self.calcular_forca():.0f}")
        
    def contratar_jogador(self, jogador):

        self.jogadores.append(
            jogador
        )
    
    def contratar_reserva(self, jogador):

        self.jogadores.append(jogador)
        self.reservas.append(jogador)
    
    def calcular_forca(self):

        ativos = [
            j for j in self.titulares
            if not j.expulso
        ]

        if not ativos:
            return 0

        total = 0

        for jogador in ativos:

            modificador = 1

            if jogador.condicao == "Cansado":
                modificador = 0.90

            elif jogador.condicao == "Exausto":
                modificador = 0.75

            total += (
                jogador.overall
                * modificador
            )

        return (
            total / len(ativos)
        ) - self.penalidade_expulsao
        
    def escalar_time(self):

        disponiveis = [
            j for j in self.jogadores
            if not j.expulso
        ]

        goleiros = sorted(
            [
                j for j in disponiveis
                if j.posicao == "Goleiro"
            ],
            key=lambda j: j.score_escalacao(),
            reverse=True
        )

        defensores = sorted(
            [
                j for j in disponiveis
                if j.posicao == "Defesa"
            ],
            key=lambda j: j.score_escalacao(),
            reverse=True
        )
        
        meias = sorted(
            [
                j for j in disponiveis
                if j.posicao == "Meio-Campo"
            ],
            key=lambda j: j.score_escalacao(),
            reverse=True
        )
        
        atacantes = sorted(
            [
                j for j in disponiveis
                if j.posicao == "Atacante"
            ],
            key=lambda j: j.score_escalacao(),
            reverse=True
        )

        self.titulares = (
            goleiros[:1]
            + defensores[:4]
            + meias[:3]
            + atacantes[:3]
        )

        self.reservas = [
            j for j in disponiveis
            if j not in self.titulares
        ]
    
    def saldo_gols(self):
        return self.gols_marcados - self.gols_sofridos
    
    def mostrar_elenco(self):

        print("\n=== TITULARES ===")

        for jogador in self.jogadores:
            print(
                jogador.nome,
                jogador.posicao
            )

        print("\n=== RESERVAS ===")

        for jogador in self.reservas:
            print(
                jogador.nome,
                jogador.posicao
            )
    