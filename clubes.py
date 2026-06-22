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
        
    def contratar_jogador(self, jogador):
        self.jogadores.append(jogador)