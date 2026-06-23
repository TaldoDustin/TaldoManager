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
            peso = 12

        elif self.posicao == "Meio-Campo":
            peso = 5

        elif self.posicao == "Defesa":
            peso = 2
        
        else: 
            peso = 1

        return peso