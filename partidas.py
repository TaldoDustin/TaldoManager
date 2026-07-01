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
    
    def simular_cartoes(self):

        self.distribuir_cartoes(
            self.clube1
        )

        self.distribuir_cartoes(
            self.clube2
        )
    
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
    
    def simular_gols(
        self,
        estatisticas
    ):

        self.distribuir_gols(
            self.clube1,
            self.gols_c1,
            estatisticas
        )

        self.distribuir_gols(
            self.clube2,
            self.gols_c2,
            estatisticas
        )
    
    def simular_penaltis(
        self,
        estatisticas
    ):

        self.simular_penalti(
            self.clube1,
            estatisticas
        )

        self.simular_penalti(
            self.clube2,
            estatisticas
        )
    
    def simular_ataque(
        self,
        minuto,
        estatisticas
    ):

        forca_c1 = (
            self.clube1.calcular_forca()
            - self.clube1.penalidade_expulsao
        )

        forca_c2 = (
            self.clube2.calcular_forca()
            - self.clube2.penalidade_expulsao
        )

        # houve ataque?
        if random.random() > 0.18:
            return

        # quem atacou?
        clube_atacando = random.choices(
            [self.clube1, self.clube2],
            weights=[forca_c1, forca_c2],
            k=1
        )[0]

        # quem defendeu?
        clube_defendendo = (
            self.clube2
            if clube_atacando == self.clube1
            else self.clube1
        )

        # houve finalização?
        chance_finalizacao = 0.30

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

            chance_no_gol = 0.45

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
    
    def simular_penalti_minuto(
        self,
        minuto,
        estatisticas
    ):
        pass
    
    #Simulação
    
    def gerar_gols(self):

        forca_c1, forca_c2 = self.calcular_forcas()

        (
            chance_c1,
            chance_c2,
            chance_empate,
            diferenca_abs
        ) = self.calcular_probabilidades(
            forca_c1,
            forca_c2
        )

        self.mostrar_analise(
            forca_c1,
            forca_c2,
            chance_c1,
            chance_c2,
            chance_empate
        )

        (
            vitorias_favorito,
            vitorias_azarao,
            empates
        ) = self.definir_placares(
            diferenca_abs
        )

        return self.sortear_resultado(
            chance_c1,
            chance_empate,
            vitorias_favorito,
            vitorias_azarao,
            empates
        )
    
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
    
    def distribuir_gols(
        self,
        clube,
        quantidade_gols,
        estatisticas
    ):

        for _ in range(quantidade_gols):

            minuto = random.randint(
                1,
                90
            )

            self.marcar_gol(
                clube,
                minuto,
                estatisticas
            )
    
    def distribuir_assistencia(self, clube, artilheiro, estatisticas):

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

            self.eventos.append({
                "minuto": minuto,
                "tipo": "expulsao",
                "jogador": jogador
            })

            return

        # amarelo
        jogador.amarelos += 1
        jogador.amarelos_partida += 1

        self.eventos.append({
            "minuto": minuto,
            "tipo": "cartao_amarelo",
            "jogador": jogador
        })

        # segundo amarelo
        if (
            jogador.amarelos_partida >= 2
            and random.random() < 0.30
        ):

            jogador.vermelhos += 1
            jogador.expulso = True

            clube.penalidade_expulsao += 5

            self.eventos.append({
                "minuto": minuto,
                "tipo": "expulsao",
                "jogador": jogador
            })
    
    def distribuir_cartoes(self, clube):

        quantidade = random.choices(
            [0,1,2,3,4],
            weights=[55,30,12,3,1]
        )[0]

        for _ in range(quantidade):

            minuto = random.randint(
                1,
                90
            )

            self.distribuir_cartao(
                clube,
                minuto
            )
    
    def simular_penalti(self, clube, estatisticas):

        if random.random() > 0.03:
            return

        cobrador = self.escolher_cobrador(clube)

        minuto = random.randint(1, 90)

        if random.random() < 0.80:

            cobrador.gols += 1
            cobrador.penaltis += 1

            # ADICIONE ESTA LINHA
            estatisticas[cobrador]["gols"] += 1

            # Atualiza o placar
            if clube == self.clube1:
                self.gols_c1 += 1
            else:
                self.gols_c2 += 1

            self.eventos.append({
                "minuto": minuto,
                "tipo": "penalti",
                "jogador": cobrador,
            })

        else:

            cobrador.penaltis_perdidos += 1

            self.eventos.append({
                "minuto": minuto,
                "tipo": "penalti_perdido",
                "jogador": cobrador,
            })
    
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
            "penalti_perdido": "❌",
            "chute_fora": "💨"
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

        eventos = sorted(
            self.eventos,
            key=lambda e: e["minuto"]
        )

        for evento in eventos:

            tipo = evento.get("tipo")

            if tipo == "gol":
                print(
                    f"{int(evento['minuto'])}' ⚽ "
                    f"{evento['jogador'].nome}"
                )

            elif tipo == "cartao_amarelo":
                print(
                    f"{int(evento['minuto'])}' 🟨 "
                    f"{evento['jogador'].nome}"
                )

            elif tipo == "expulsao":
                print(
                    f"{int(evento['minuto'])}' 🟥 "
                    f"{evento['jogador'].nome}"
                )

            elif tipo == "penalti":
                print(
                    f"{int(evento['minuto'])}' ⚽ (P) "
                    f"{evento['jogador'].nome}"
                )
                
            elif tipo == "penalti_perdido":
                print(
                    f"{int(evento['minuto'])}' ❌ (P) "
                    f"{evento['jogador'].nome}"
                )

            else:
                print(
                    evento.get(
                        "texto",
                        "Evento desconhecido"
                    )
                )
    
    #Estatisticas
    
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
    
    #Engine
    
    def calcular_forcas(self):

        forca_c1 = self.clube1.calcular_forca()
        forca_c2 = self.clube2.calcular_forca()

        # vantagem do mandante
        forca_c1 += 1

        # dia bom / ruim
        forca_c1 += random.randint(-1, 1)
        forca_c2 += random.randint(-1, 1)

        return forca_c1, forca_c2
    
    def calcular_probabilidades(
        self,
        forca_c1,
        forca_c2
    ):

        diferenca = forca_c1 - forca_c2
        diferenca_abs = abs(diferenca)

        chance_c1 = 0.5 + (diferenca * 0.06)

        chance_c1 = max(
            0.15,
            min(0.85, chance_c1)
        )

        chance_c2 = 1 - chance_c1

        if diferenca_abs <= 2:
            chance_empate = 0.20

        elif diferenca_abs <= 5:
            chance_empate = 0.18

        elif diferenca_abs <= 8:
            chance_empate = 0.12

        else:
            chance_empate = 0.10

        total = chance_c1 + chance_c2

        chance_c1 = (
            chance_c1 / total
        ) * (1 - chance_empate)

        chance_c2 = (
            chance_c2 / total
        ) * (1 - chance_empate)

        return (
            chance_c1,
            chance_c2,
            chance_empate,
            diferenca_abs
        )
    
    def definir_placares(
        self,
        diferenca_abs
    ):

        if diferenca_abs <= 2:

            vitorias_favorito = [
                (1,0),
                (1,0),
                (1,0),
                (2,1),
                (2,1),
                (2,1),
                (3,2)
            ]

            vitorias_azarao = [
                (1,0),
                (1,0),
                (2,1),
                (2,1)
            ]

            empates = [
                (0,0),
                (1,1),
                (1,1),
                (1,1),
                (2,2)
            ]

        elif diferenca_abs <= 6:

            vitorias_favorito = [
                (1,0),
                (1,0),
                (2,0),
                (2,0),
                (2,1),
                (2,1),
                (3,1),
                (3,0)
            ]

            vitorias_azarao = [
                (1,0),
                (1,0),
                (2,1),
                (2,1),
                (2,0)
            ]

            empates = [
                (0,0),
                (1,1),
                (1,1),
                (2,2)
            ]

        else:

            vitorias_favorito = [
                (1,0),
                (2,0),
                (2,0),
                (2,0),
                (2,1),
                (3,0),
                (3,1),
                (3,1),
                (4,0),
                (4,1)
            ]

            vitorias_azarao = [
                (1,0),
                (1,0),
                (2,0),
                (2,1)
            ]

            empates = [
                (0,0),
                (1,1)
            ]

        if diferenca_abs >= 10:

            vitorias_favorito.extend([
                (2,0),
                (3,0),
                (3,1),
                (4,0),
                (5,0)
            ])

            vitorias_azarao = [
                (1,0),
                (1,0),
                (2,0),
                (2,1)
            ]

            empates = [
                (0,0),
                (1,1)
            ]

        return (
            vitorias_favorito,
            vitorias_azarao,
            empates
        )
    
    def sortear_resultado(
        self,
        chance_c1,
        chance_empate,
        vitorias_favorito,
        vitorias_azarao,
        empates
    ):

        sorteio = random.random()

        if sorteio < chance_c1:

            gols_c1, gols_c2 = random.choice(
                vitorias_favorito
            )

        elif sorteio < chance_c1 + chance_empate:

            gols_c1, gols_c2 = random.choice(
                empates
            )

        else:

            gols_c2, gols_c1 = random.choice(
                vitorias_azarao
            )

        return gols_c1, gols_c2
    
    def mostrar_analise(
        self,
        forca_c1,
        forca_c2,
        chance_c1,
        chance_c2,
        chance_empate
    ):

        print("\n--- ANÁLISE DA PARTIDA ---")

        print(
            f"{self.clube1.nome}: "
            f"força {forca_c1:.1f} | "
            f"chance {chance_c1:.1%}"
        )

        print(
            f"{self.clube2.nome}: "
            f"força {forca_c2:.1f} | "
            f"chance {chance_c2:.1%}"
        )

        print(
            f"Chance empate: {chance_empate:.1%}"
        )

        print("--------------------------")
        
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