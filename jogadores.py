

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
        self.clean_sheets = 0
        self.hat_tricks = 0
        self.penaltis = 0
        self.penaltis_perdidos = 0
        self.amarelos = 0
        self.vermelhos = 0
        # estatísticas ofensivas da partida
        self.chutes_partida = 0
        self.chutes_gol_partida = 0
        self.passes_chave_partida = 0
        # estatísticas defensivas da partida
        self.defesas_partida = 0
        self.desarmes_partida = 0
        self.interceptacoes_partida = 0
        
        
        # controle por partida
        self.amarelos_partida = 0
        self.expulso = False
        
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

        if self.posicao == "Defesa":
            return 1 

        if self.posicao == "Meio-Campo":
            return 5 + (self.overall // 15)

        if self.posicao == "Atacante":
            return 12 + (self.overall // 15)
    
    def peso_assistencia(self):

        if self.posicao == "Goleiro":
            return 1

        base = {
            "Atacante": 7,
            "Meio-Campo": 13,
            "Defesa": 2
        }

        return base[self.posicao] + (self.overall // 8)
    
    def nota_media(self):
        if self.partidas == 0:
            return 0.0
        
        return round(
            self.soma_nota / self.partidas, 2
        )
        
    def mostrar_estatisticas(self):

        print("\n=== ESTATÍSTICAS ===")

        print(
            f"Nome: {self.nome}\n"
            f"Posição: {self.posicao}\n"
            f"Overall: {self.overall}\n"
            f"Jogos: {self.partidas}\n"
            f"Gols: {self.gols}\n"
            f"Assistências: {self.assistencias}\n"
            f"Melhores em campo: {self.melhor_em_campo}\n"
            f"Hat-tricks: {self.hat_tricks}\n"
            f"Pênaltis: {self.penaltis}\n"
            f"Pênaltis perdidos: {self.penaltis_perdidos}\n"
            f"Clean Sheets: {self.clean_sheets}\n"
            f"Nota Média: {self.nota_media()}\n"
            f"Melhor Nota: {round(self.melhor_nota,2)}\n"
            f"Pior Nota: {round(self.pior_nota,2)}\n"
        )
        