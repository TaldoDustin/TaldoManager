import random
class Partida:
    def __init__(self, clube1, clube2):
        self.clube1 = clube1
        self.clube2 = clube2
        self.resultado = None
        self.gols_c1 = 0
        self.gols_c2 = 0
        self.eventos = []
        self.posse_c1 = 50
        self.posse_c2 = 50
        self.finalizacoes_c1 = 0
        self.finalizacoes_c2 = 0
        self.finalizacoes_gol_c1 = 0
        self.finalizacoes_gol_c2 = 0
        
    #Orquestração
        
    def preparar_partida(self):

        self.gols_c1 = 0
        self.gols_c2 = 0

        self.finalizacoes_c1 = 0
        self.finalizacoes_c2 = 0

        self.finalizacoes_gol_c1 = 0
        self.finalizacoes_gol_c2 = 0

        self.eventos = []

        self.clube1.penalidade_expulsao = 0
        self.clube2.penalidade_expulsao = 0

        self.calcular_posse()

        for jogador in (
            self.clube1.jogadores +
            self.clube2.jogadores
        ):
            jogador.resetar_estatisticas_partida()
    
    def executar_simulacao(
        self,
        estatisticas
    ):

        for minuto in range(1,91):

            self.simular_minuto(
                minuto,
                estatisticas
            )
    
    def simular_minuto(
        self,
        minuto,
        estatisticas
    ):

        self.simular_ataque(
            minuto,
            estatisticas
        )

        self.simular_cartao(
            minuto
        )

        self.simular_penalti_minuto(
            minuto,
            estatisticas
        )
    
    def finalizar_partida(self):

        self.recalcular_placar()

        self.definir_resultado()

        self.mostrar_resultado()

        self.mostrar_eventos()

        self.atualizar_classificacao()

        self.atualizar_estatisticas_clubes()

        self.atualizar_clean_sheet()
    
    def simular_partida(self):

        self.preparar_partida()

        estatisticas = (
            self.criar_estatisticas()
        )

        self.executar_simulacao(
            estatisticas
        )

        self.processar_eventos()

        self.verificar_hat_tricks(
            estatisticas
        )

        self.finalizar_partida()

        melhor, nota = (
            self.calcular_notas(
                estatisticas
            )
        )

        self.mostrar_melhor_em_campo(
            melhor,
            nota
        )
    
    #Engine
    
    def simular_ataque(
        self,
        minuto,
        estatisticas
    ):

        # houve ataque?
        if random.random() > 0.25:
            return

        # quem atacou?
        clube_atacando = random.choices(
            [self.clube1, self.clube2],
            weights=[
                self.posse_c1,
                self.posse_c2
            ]
        )[0]

        # quem defendeu?
        clube_defendendo = (
            self.clube2
            if clube_atacando == self.clube1
            else self.clube1
        )

        # houve finalização?
        chance_finalizacao = 0.33

        if random.random() < chance_finalizacao:

            if clube_atacando == self.clube1:
                self.finalizacoes_c1 += 1
            else:
                self.finalizacoes_c2 += 1

            artilheiro = self.escolher_artilheiro(
                clube_atacando
            )

            if artilheiro is None:
                return

            artilheiro.chutes_partida += 1

            chance_no_gol = 0.53

            if random.random() > chance_no_gol:

                self.adicionar_evento(
                    minuto,
                    "chute_fora",
                    artilheiro
                )

                return

            if clube_atacando == self.clube1:
                self.finalizacoes_gol_c1 += 1
            else:
                self.finalizacoes_gol_c2 += 1

            artilheiro.chutes_gol_partida += 1

            if self.goleiro_defendeu(
                clube_defendendo
            ):
                return

            self.marcar_gol(
                clube_atacando,
                minuto,
                estatisticas,
                artilheiro
            )
    
    def goleiro_defendeu(
        self,
        clube
    ):

        goleiro = next(
            (
                j for j in clube.jogadores
                if j.posicao == "Goleiro"
            ),
            None
        )

        if goleiro is None:
            return False

        chance_defesa = (
            0.18 +
            (goleiro.overall - 70) * 0.012
        )

        if random.random() < chance_defesa:

            goleiro.defesas_partida += 1
            return True

        return False
    
    def marcar_gol(
        self,
        clube,
        minuto,
        estatisticas,
        artilheiro
    ):
        
        if artilheiro is None:
            return

        # atualiza estatísticas do jogador
        artilheiro.gols += 1
        estatisticas[artilheiro]["gols"] += 1

        # atualiza placar
        if clube == self.clube1:
            self.gols_c1 += 1
        else:
            self.gols_c2 += 1

        # registra evento
        self.adicionar_evento(
            minuto,
            "gol",
            artilheiro
        )

        # assistência
        self.distribuir_assistencia(
            clube,
            artilheiro,
            estatisticas
        )
    
    def simular_penalti_minuto(
        self,
        minuto,
        estatisticas
    ):

        # aproximadamente
        # 0.3 penaltis por partida
        if random.random() > 0.003:
            return

        clube = random.choice([
            self.clube1,
            self.clube2
        ])

        cobrador = self.escolher_cobrador(
            clube
        )

        if random.random() < 0.80:

            cobrador.gols += 1
            cobrador.penaltis += 1

            estatisticas[cobrador]["gols"] += 1

            self.adicionar_evento(
                minuto,
                "penalti",
                cobrador
            )
        else:

            cobrador.penaltis_perdidos += 1

            self.adicionar_evento(
                minuto,
                "penalti_perdido",
                cobrador
            )
    
    #Escolhas
    
    def escolher_artilheiro(
        self,
        clube
    ):

        lista = []

        for jogador in clube.jogadores:

            if jogador.expulso:
                continue

            peso = jogador.peso_gol()

            if jogador.posicao == "Goleiro":
                peso = 0

            if peso > 0:
                lista.extend(
                    [jogador] * peso
                )

        if not lista:
            return None

        return random.choice(lista)
    
    def escolher_cobrador(self, clube):

        cobradores = [
            j for j in clube.jogadores
            if j.posicao != "Goleiro"
            and not j.expulso
        ]

        pesos = []

        for jogador in cobradores:

            if jogador.posicao == "Atacante":
                peso = jogador.overall * 4

            elif jogador.posicao == "Meio-Campo":
                peso = jogador.overall * 2

            else:  # Defesa
                peso = max(1, jogador.overall // 8)

            pesos.append(peso)

        return random.choices(
            cobradores,
            weights=pesos,
            k=1
        )[0]
    
    def distribuir_assistencia(
        self,
        clube,
        artilheiro,
        estatisticas
    ):

        lista = []

        for jogador in clube.jogadores:
            
            if jogador.expulso:
                continue

            if (
                jogador != artilheiro
                and not jogador.expulso
            ):

                peso = jogador.peso_assistencia()

                if peso > 0:
                    lista.extend([jogador] * peso)

        if lista and random.random() < 0.70:

            assistente = random.choice(lista)

            assistente.assistencias += 1
            estatisticas[assistente]["assistencias"] += 1
    
    #Cartões
    
    def simular_cartao(
        self,
        minuto
    ):

        # aproximadamente 3 cartões por jogo
        if random.random() > 0.03:
            return

        clube = random.choice([
            self.clube1,
            self.clube2
        ])

        self.distribuir_cartao(
            clube,
            minuto
        )
    
    def distribuir_cartao(
        self,
        clube,
        minuto
    ):

        jogadores_validos = [
            j for j in clube.jogadores
            if not j.expulso
        ]

        if not jogadores_validos:
            return

        jogador = random.choice(
            jogadores_validos
        )

        # vermelho direto
        if random.random() < 0.01:

            jogador.vermelhos += 1
            jogador.expulso = True

            clube.penalidade_expulsao += 5

            self.adicionar_evento(
                minuto,
                "expulsao",
                jogador
            )

            return

        # amarelo
        jogador.amarelos += 1
        jogador.amarelos_partida += 1

        self.adicionar_evento(
            minuto,
            "cartao_amarelo",
            jogador
        )

        # segundo amarelo
        if (
            jogador.amarelos_partida >= 2
            and random.random() < 0.30
        ):

            jogador.vermelhos += 1
            jogador.expulso = True

            clube.penalidade_expulsao += 5

            self.adicionar_evento(
                minuto,
                "expulsao",
                jogador
            )
    
    #Eventos
    
    def adicionar_evento(
        self,
        minuto,
        tipo,
        jogador
    ):

        simbolos = {
            "gol": "⚽",
            "assistencia": "🅰️",
            "penalti": "⚽ (P)",
            "penalti_perdido": "❌ (P)",
            "chute_fora": "💨",
            "cartao_amarelo": "🟨",
            "expulsao": "🟥",
            "defesa_goleiro": "🧤",
        }

        simbolo = simbolos.get(
            tipo,
            "•"
        )

        texto = (
            f"{minuto}' "
            f"{simbolo} "
            f"{jogador.nome}"
        )

        self.eventos.append({
            "minuto": minuto,
            "tipo": tipo,
            "jogador": jogador,
            "texto": texto
        })
            
    def processar_eventos(self):

        self.eventos.sort(
            key=lambda e: e["minuto"]
        )

        expulsos = set()
        eventos_validos = []

        for evento in self.eventos:

            jogador = evento.get("jogador", None)

            if jogador and jogador in expulsos:
                continue

            eventos_validos.append(evento)

            if evento.get("tipo") == "expulsao" and jogador:
                expulsos.add(jogador)

        self.eventos = eventos_validos
    
    def mostrar_eventos(self):

        print("\nEVENTOS")

        for evento in sorted(
            self.eventos,
            key=lambda e: e["minuto"]
        ):

            print(
                evento.get(
                    "texto",
                    "Evento"
                )
            )
    
    #Estatísticas
    
    def criar_estatisticas(self):

        estatisticas = {}

        for jogador in self.clube1.jogadores + self.clube2.jogadores:
            estatisticas[jogador] = {
                "gols": 0, 
                "assistencias": 0
            }

        return estatisticas
    
    def verificar_hat_tricks(
        self,
        estatisticas
    ):

        for jogador in estatisticas:

            if estatisticas[jogador]["gols"] >= 3:

                jogador.hat_tricks += 1

                print(
                    f"\n🎩 HAT-TRICK DE "
                    f"{jogador.nome}!"
                )
    
    def calcular_notas(self, estatisticas):

        melhor_jogador = None
        maior_nota = 0

        for jogador in self.clube1.jogadores + self.clube2.jogadores:

            nota = 6.0

            gols = estatisticas[jogador]["gols"]
            assistencias = estatisticas[jogador]["assistencias"]

            # ==========================
            # IDENTIFICA O TIME
            # ==========================

            time1 = jogador in self.clube1.jogadores

            if time1:
                gols_pro = self.gols_c1
                gols_contra = self.gols_c2
            else:
                gols_pro = self.gols_c2
                gols_contra = self.gols_c1

            saldo = gols_pro - gols_contra
            clean_sheet = gols_contra == 0

            # ==========================
            # AÇÕES DA PARTIDA
            # ==========================

            if jogador.posicao == "Atacante":

                nota += gols * 1.4
                nota += assistencias * 0.8
                nota += jogador.chutes_gol_partida * 0.12
                nota += jogador.dribles_partida * 0.05

            elif jogador.posicao == "Meio-Campo":

                nota += gols * 1.1
                nota += assistencias * 1.0
                nota += jogador.passes_chave_partida * 0.10
                nota += jogador.interceptacoes_partida * 0.04
                nota += jogador.dribles_partida * 0.03

            elif jogador.posicao == "Defesa":

                nota += gols * 1.5
                nota += assistencias * 0.5
                nota += jogador.desarmes_partida * 0.06
                nota += jogador.interceptacoes_partida * 0.05
                nota += jogador.cortes_partida * 0.02

                if clean_sheet:
                    nota += 0.25

            elif jogador.posicao == "Goleiro":

                nota += jogador.defesas_partida * 0.08

                if clean_sheet:
                    nota += 0.60

                nota -= jogador.gols_sofridos_partida * 0.15

            # ==========================
            # RESULTADO
            # ==========================

            if saldo > 0:
                nota += 0.3

            elif saldo < 0:
                nota -= 0.2

            # ==========================
            # BÔNUS EXTRAS
            # ==========================

            if (
                jogador.posicao == "Atacante"
                and saldo >= 2
            ):
                nota += 0.2

            if (
                jogador.posicao == "Meio-Campo"
                and gols > 0
                and assistencias > 0
            ):
                nota += 0.1

            if (
                jogador.posicao == "Goleiro"
                and saldo == 0
                and clean_sheet
            ):
                nota += 0.2

            # ==========================
            # LIMITA NOTA
            # ==========================

            nota = max(0, min(10, nota))

            jogador.soma_nota += nota
            jogador.partidas += 1

            if nota > jogador.melhor_nota:
                jogador.melhor_nota = nota

            if nota < jogador.pior_nota:
                jogador.pior_nota = nota

            # ==========================
            # MELHOR EM CAMPO
            # ==========================

            if melhor_jogador is None:
                melhor_jogador = jogador
                maior_nota = nota

            elif (
                nota > maior_nota
                or (
                    nota == maior_nota
                    and (
                        estatisticas[jogador]["gols"],
                        estatisticas[jogador]["assistencias"]
                    ) > (
                        estatisticas[melhor_jogador]["gols"],
                        estatisticas[melhor_jogador]["assistencias"]
                    )
                )
            ):
                melhor_jogador = jogador
                maior_nota = nota

        melhor_jogador.melhor_em_campo += 1

        return melhor_jogador, maior_nota
    
    def mostrar_melhor_em_campo(self, jogador, nota):

        print("\n⭐ MELHOR EM CAMPO")

        print(
            f"{jogador.nome} " 
            f"({jogador.posicao}) " 
            f"- Nota {nota:.1f}\n")
    
    #Resultado
    
    def recalcular_placar(self):

        gols_c1 = 0
        gols_c2 = 0

        for evento in self.eventos:

            if evento["tipo"] in ["gol", "penalti"]:

                jogador = evento["jogador"]

                if jogador in self.clube1.jogadores:
                    gols_c1 += 1
                else:
                    gols_c2 += 1

        self.gols_c1 = gols_c1
        self.gols_c2 = gols_c2
    
    def definir_resultado(self):

        if self.gols_c1 > self.gols_c2:
            self.resultado = f"{self.clube1.nome} venceu!"

        elif self.gols_c2 > self.gols_c1:
            self.resultado = f"{self.clube2.nome} venceu!"

        else:
            self.resultado = "Empate!"
    
    def mostrar_resultado(self):

        print(
            f"{self.clube1.nome} "
            f"{self.gols_c1} x "
            f"{self.gols_c2} "
            f"{self.clube2.nome}"
        )

        print(f"{self.resultado}\n")
    
    #Campeonato
    
    def atualizar_classificacao(self):

        if self.gols_c1 > self.gols_c2:

            self.clube1.pontos += 3
            self.clube1.vitorias += 1
            self.clube2.derrotas += 1

            self.clube1.atualizar_forma("V")
            self.clube2.atualizar_forma("D")

        elif self.gols_c2 > self.gols_c1:

            self.clube2.pontos += 3
            self.clube2.vitorias += 1
            self.clube1.derrotas += 1

            self.clube2.atualizar_forma("V")
            self.clube1.atualizar_forma("D")

        else:

            self.clube1.pontos += 1
            self.clube2.pontos += 1

            self.clube1.empates += 1
            self.clube2.empates += 1

            self.clube1.atualizar_forma("E")
            self.clube2.atualizar_forma("E")
    
    def atualizar_estatisticas_clubes(self):

        self.clube1.gols_marcados += self.gols_c1
        self.clube1.gols_sofridos += self.gols_c2

        self.clube2.gols_marcados += self.gols_c2
        self.clube2.gols_sofridos += self.gols_c1   
    
    def atualizar_clean_sheet(self):

        if self.gols_c2 == 0:
            print(
                f"CS -> {self.clube1.nome} "
                f"(placar {self.gols_c1}x{self.gols_c2})"
            )

            for jogador in self.clube1.jogadores:
                if jogador.posicao == "Goleiro":
                    jogador.clean_sheets += 1
                    print(
                        f"   {jogador.nome}: "
                        f"{jogador.clean_sheets}"
                    )

        if self.gols_c1 == 0:
            print(
                f"CS -> {self.clube2.nome} "
                f"(placar {self.gols_c2}x{self.gols_c1})"
            )

            for jogador in self.clube2.jogadores:
                if jogador.posicao == "Goleiro":
                    jogador.clean_sheets += 1
                    print(
                        f"   {jogador.nome}: "
                        f"{jogador.clean_sheets}"
                    )
            
    #Utilidade
    
    def calcular_posse(self):

        ataque1 = sum(
            j.overall
            for j in self.clube1.jogadores
            if j.posicao == "Atacante"
        )

        meio1 = sum(
            j.overall
            for j in self.clube1.jogadores
            if j.posicao == "Meio-Campo"
        )

        ataque2 = sum(
            j.overall
            for j in self.clube2.jogadores
            if j.posicao == "Atacante"
        )

        meio2 = sum(
            j.overall
            for j in self.clube2.jogadores
            if j.posicao == "Meio-Campo"
        )

        forca1 = ataque1 * 1.2 + meio1 * 1.6
        forca2 = ataque2 * 1.2 + meio2 * 1.6

        total = forca1 + forca2

        self.posse_c1 = round(
            (forca1 / total) * 100
        )

        self.posse_c2 = 100 - self.posse_c1
    