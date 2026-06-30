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
        self.jogadores.append(jogador)
        
    def calcular_forca(self):

        if not self.jogadores:
            return 0

        total = sum(
            jogador.overall
            for jogador in self.jogadores
            if not jogador.expulso
        )

        ativos = [
            j for j in self.jogadores
            if not j.expulso
        ]

        if not ativos:
            return 0

        return (
            total / len(ativos)
        ) - self.penalidade_expulsao
    
    def saldo_gols(self):
        return self.gols_marcados - self.gols_sofridos
    