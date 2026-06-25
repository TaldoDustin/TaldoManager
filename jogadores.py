

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
        self.pior_nota = 10.0
        self.melhor_em_campo = 0
        
    def mostrar(self):
        print(
            f"Nome: {self.nome}, "
            f"Idade: {self.idade}, "
            f"Posição: {self.posicao}, "
            f"Overall: {self.overall}"
        )
        
    def mostrar_nota(self):
        print(
            f"Nome: {self.nome}, "
            f"Posição: {self.posicao}, "
            f"Nota Média: {self.soma_nota}, "
            f"Melhor Nota: {self.melhor_nota}, "
            f"Pior Nota: {self.pior_nota}"
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
            "Goleiro": 1
        }

        if self.posicao == "Goleiro":
            return 1

        return base[self.posicao] + (self.overall // 8)
    
    def nota_media(self):
        if self.partidas == 0:
            return 0.0
        
        return round(
            self.soma_nota / self.partidas, 2
        )
        
    def mostrar_estatisticas(self):
        print("\n=== MVP ===")
        
        print(
            f"Nome: {self.nome} \n"
            f"Posição: {self.posicao} \n"
            f"Overall: {self.overall} \n"
            f"Jogos: {self.partidas} \n"
            f"Gols: {self.gols} \n"
            f"Assistências: {self.assistencias} \n"
            f"Nota Média: {self.nota_media()} \n"
            f"Melhor Nota: {round(self.melhor_nota, 2)} \n"
            f"Pior Nota: {round(self.pior_nota, 2)} \n"
        )
        