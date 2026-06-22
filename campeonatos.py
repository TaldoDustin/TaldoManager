class Campeonato:
    def __init__(self, nome, clubes):
        self.nome = nome
        self.clubes = clubes
        
    def jogar_rodada(self):
        print(f"Jogando rodada do campeonato {self.nome}...")
        # Lógica para simular os jogos entre os clubes
        for clube in self.clubes:
            print(f"{clube.nome} jogou sua partida.")