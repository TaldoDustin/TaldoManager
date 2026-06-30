import random
class Partida:
    def __init__(self, clube1, clube2):
        self.clube1 = clube1
        self.clube2 = clube2
        self.resultado = None
        self.gols_c1 = 0
        self.gols_c2 = 0
        self.eventos = []
    
    def simular_partida(self):
        
        for jogador in self.clube1.jogadores + self.clube2.jogadores:
            jogador.expulso = False
            jogador.amarelos_partida = 0

        self.gols_c1, self.gols_c2 = self.gerar_gols()

        estatisticas = self.criar_estatisticas()
        
        self.distribuir_cartoes(self.clube1)
        self.distribuir_cartoes(self.clube2)

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
        
        self.simular_penalti(self.clube1, estatisticas)
        self.simular_penalti(self.clube2, estatisticas)
        
        self.verificar_hat_tricks(
            estatisticas
        )

        self.processar_eventos()
        self.definir_resultado()
        self.mostrar_resultado()
        self.mostrar_eventos()

        self.atualizar_classificacao()
        self.atualizar_estatisticas_clubes()
        self.atualizar_clean_sheet()

        melhor_jogador, maior_nota = self.calcular_notas(estatisticas)

        self.mostrar_melhor_em_campo(
            melhor_jogador,
            maior_nota
        )    

#distribuição

    def criar_estatisticas(self):

        estatisticas = {}

        for jogador in self.clube1.jogadores + self.clube2.jogadores:
            estatisticas[jogador] = {
                "gols": 0, 
                "assistencias": 0
            }

        return estatisticas
    
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
            "penalti_perdido": "❌"
        }

        texto = f"{minuto}' {simbolos[tipo]} {jogador.nome}"

        self.eventos.append({
            "minuto": minuto,
            "tipo": tipo,
            "jogador": jogador,
            "texto": texto
        })
    
    def distribuir_gols(self, clube, quantidade_gols, estatisticas):

        lista = []

        for jogador in clube.jogadores:

            if jogador.expulso:
                continue

            peso = jogador.peso_gol()

            if peso > 0:
                lista.extend([jogador] * peso)

        if not lista:
            return

        for _ in range(quantidade_gols):

            artilheiro = random.choice(lista)

            artilheiro.gols += 1
            estatisticas[artilheiro]["gols"] += 1
            
            minuto = random.randint(1,90)
            
            self.adicionar_evento(
                minuto,
                "gol",
                artilheiro
            )

            self.distribuir_assistencia(
                clube,
                artilheiro,
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

#resultado

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
#campeonato

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

#jogadores

    def calcular_notas(self, estatisticas):

        melhor_jogador = None
        maior_nota = 0

        bonus_posicao = {
            "Atacante": (0.8, 0.4),
            "Meio-Campo": (0.9, 0.6),
            "Defesa": (0.6, 0.6),
            "Goleiro": (1.5, 1.0)
        }

        for jogador in self.clube1.jogadores + self.clube2.jogadores:

            nota = 6.0

            gols = estatisticas[jogador]["gols"]
            assistencias = estatisticas[jogador]["assistencias"]

            bonus_gol, bonus_assistencia = bonus_posicao[jogador.posicao]

            nota += gols * bonus_gol
            nota += assistencias * bonus_assistencia

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
            # RESULTADO DA PARTIDA
            # ==========================

            if saldo > 0:
                nota += 0.3

            elif saldo < 0:
                nota -= 0.2

            # ==========================
            # BÔNUS POR POSIÇÃO
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
                jogador.posicao == "Defesa"
                and clean_sheet
            ):
                nota += 0.5

            if (
                jogador.posicao == "Goleiro"
                and clean_sheet
            ):
                nota += 0.2

            # Futuramente
            # if jogador.capitao:
            #     nota += 0.1

            # ==========================
            # LIMITA A NOTA
            # ==========================

            nota = max(0, min(10, nota))

            # ==========================
            # SALVA ESTATÍSTICAS
            # ==========================

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
    
    def mostrar_melhor_em_campo(self, jogador, nota):

        print("\n⭐ MELHOR EM CAMPO")

        print(
            f"{jogador.nome} " 
            f"({jogador.posicao}) " 
            f"- Nota {nota:.1f}\n")
        
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

#simulação

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

        pesos = [j.overall for j in cobradores]

        return random.choices(
            cobradores,
            weights=pesos,
            k=1
        )[0]
        
    def distribuir_cartoes(self, clube):

        quantidade = random.choices(
            [0,1,2,3,4],
            weights=[55,30,12,3,1]
        )[0]

        for _ in range(quantidade):

            jogadores_validos = [
                j for j in clube.jogadores
                if not j.expulso
            ]

            if not jogadores_validos:
                return

            jogador = random.choice(jogadores_validos)

            minuto = random.randint(1, 90)

            # Vermelho direto
            if random.random() < 0.01:

                jogador.vermelhos += 1
                jogador.expulso = True
                
                clube.penalidade_expulsao += 5

                self.eventos.append({
                    "minuto": minuto,
                    "tipo": "expulsao",
                    "jogador": jogador
                })

                continue 

            # Amarelo
            jogador.amarelos += 1
            jogador.amarelos_partida += 1

            self.eventos.append({
                "minuto": minuto,
                "tipo": "cartao_amarelo",
                "jogador": jogador
            })

            # Segundo amarelo
            if (
                jogador.amarelos_partida >= 2
                and random.random() < 0.30
            ):

                jogador.vermelhos += 1
                jogador.expulso = True

                self.eventos.append({
                    "minuto": minuto,
                    "tipo": "expulsao",
                    "jogador": jogador
                })

                continue
    
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
            chance_empate = 0.15

        elif diferenca_abs <= 5:
            chance_empate = 0.12

        elif diferenca_abs <= 8:
            chance_empate = 0.08

        else:
            chance_empate = 0.05

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