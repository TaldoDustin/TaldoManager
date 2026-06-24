class Jogador:
    def __init__(self, nome, idade, posicao, overall):
        self.nome = nome
        self.idade = idade
        self.posicao = posicao
        self.overall = overall
        self.gols = 0
        self.assistencias = 0
        self.partidas = 0
        self.soma_nota = 0.0
        self.melhor_nota = 0.0
        self.pior_nota = 0.0
        
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
    
    def peso_assistencia(self):

        base = {
            "Atacante": 5,
            "Meio-Campo": 12,
            "Defesa": 3,
            "Goleiro": 0
        }

        return base[self.posicao] + (self.overall // 8)
    
    def nota_media(self):
        if self.partidas == 0:
            return 0.0
        
        return round(
            self.soma_nota / self.partidas, 2
        )
        