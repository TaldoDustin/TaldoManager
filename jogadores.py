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

        if self.posicao == "Goleiro":   
            return 0

        base = {
            "Atacante": 12,
            "Meio-Campo": 5,
            "Defesa": 2,
            "Goleiro": 0
        }
        
        peso = base.get(self.posicao, 0) * (self.overall // 80)
        
        return peso + (self.overall // 5)