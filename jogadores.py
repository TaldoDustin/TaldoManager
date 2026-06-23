class Jogador:
    def __init__(self, nome, idade, posicao, overall):
        self.nome = nome
        self.idade = idade
        self.posicao = posicao
        self.overall = overall
        self.gols = 0
        
    def mostrar(self):
        print(
            f"Nome: {self.nome}, "
            f"Idade: {self.idade}, "
            f"Posição: {self.posicao}, "
            f"Overall: {self.overall}"
        )
        
    def peso_gol(self):

        if self.posicao == "Atacante":
            return 5

        elif self.posicao == "Meio-Campo":
            return 3

        elif self.posicao == "Defesa":
            return 1

        return 1