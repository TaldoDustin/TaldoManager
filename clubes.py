class Clube:
    def __init__(self, nome, pais, dinheiro):
        self.nome = nome
        self.pais = pais
        self.dinheiro = dinheiro
        self.jogadores = []
    
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
        total_overall = sum(jogador.overall for jogador in self.jogadores)
        return total_overall / len(self.jogadores)