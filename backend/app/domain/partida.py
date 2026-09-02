import random


class Partida:

    # vantagem do mandante, em pontos de "overall" somados à força do time
    MANDO_DE_CAMPO = 2.5

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
        self.substituicoes_c1 = 0
        self.substituicoes_c2 = 0
        self.max_substituicoes = 5
        # {"minuto", "sai", "entra"} de cada troca, para o snapshot da escalação
        self.substituicoes_log = []
        # XI inicial de cada lado (capturado em criar_estatisticas)
        self.titulares_iniciais = set()
        
    #Orquestração
        
    def preparar_partida(self):

        self.gols_c1 = 0
        self.gols_c2 = 0

        self.finalizacoes_c1 = 0
        self.finalizacoes_c2 = 0

        self.finalizacoes_gol_c1 = 0
        self.finalizacoes_gol_c2 = 0

        self.eventos = []
        self.substituicoes_log = []

        self.clube1.penalidade_expulsao = 0
        self.clube2.penalidade_expulsao = 0

        self.calcular_posse()

        for jogador in (
            self.clube1.titulares +
            self.clube2.titulares
        ):
            jogador.resetar_estatisticas_partida()
    
    def executar_simulacao(
        self,
    ):

        for minuto in range(1,91):

            self.simular_minuto(
                minuto,
            )
    
    def simular_minuto(
        self,
        minuto
    ):

        self.simular_ataque(
            minuto,
        )

        self.simular_cartao(
            minuto
        )

        self.simular_penalti_minuto(
            minuto,
        )
        self.simular_substituicao(
            minuto
        )
        if minuto in [15, 30, 45, 60, 75, 90]:
            self.atualizar_fadiga()
    
    def finalizar_partida(self):

        self.recalcular_placar()

        self.definir_resultado()

        self.mostrar_resultado()

        self.mostrar_eventos()

        self.atualizar_classificacao()

        self.atualizar_estatisticas_clubes()

        self.atualizar_clean_sheet()
    
    def simular_partida(self):

        # o cartão vermelho tira o jogador só do resto DESTA partida; ainda
        # não há suspensão automática, então todo mundo volta a ficar
        # disponível antes da próxima escalação (senão `escalar_time` filtra
        # o expulso para sempre e o elenco vai encolhendo a cada vermelho)
        for jogador in self.clube1.jogadores + self.clube2.jogadores:
            jogador.expulso = False

        self.clube1.escalar_time()
        self.clube2.escalar_time()
        
        print("\n=== ESCALAÇÃO ===")
        print(self.clube1.nome)

        for j in self.clube1.titulares:
            print(
                j.nome,
                j.overall,
                j.energia,
                j.score_escalacao()
            )

        print("\nReservas")

        for j in self.clube1.reservas:
            print(
                j.nome,
                j.overall,
                j.energia,
                j.score_escalacao()
            )
        
        
        self.preparar_partida()

        self.estatisticas = (
            self.criar_estatisticas()
    )

        self.executar_simulacao(
        )

        self.processar_eventos()

        self.verificar_hat_tricks(
            
        )

        self.finalizar_partida()

        melhor, nota = (
            self.calcular_notas(
            )
        )

        if melhor is not None:
            self.mostrar_melhor_em_campo(
                melhor,
                nota
            )
        
        print("\n=== FADIGA ANTES DA RECUPERAÇÃO ===")

        for jogador in self.clube1.titulares[:3]:
            print(
                jogador.nome,
                jogador.energia,
                jogador.condicao
            )

        for jogador in self.clube2.titulares[:3]:
            print(
                jogador.nome,
                jogador.energia,
                jogador.condicao
            )

        self.recuperar_energia(
            self.clube1
        )

        self.recuperar_energia(
            self.clube2
        )
    
    #Engine
    
    def simular_ataque(
        self,
        minuto,
    ):

        # houve ataque?
        if random.random() > 0.28:
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
        
        self.simular_acao_defensiva(
            clube_defendendo
        )

        # quem finalizou?
        artilheiro = self.escolher_artilheiro(
            clube_atacando
        )

        if artilheiro is None:
            return

        self.gerar_drible(
            artilheiro
        )

        self.gerar_passe_chave(
            artilheiro
        )

        # houve finalização?
        if not self.gerar_finalizacao(
            clube_atacando,
            artilheiro
        ):
            return

        # foi no gol?
        if not self.finalizacao_no_gol(
            clube_atacando,
            artilheiro
        ):

            self.adicionar_evento(
                minuto,
                "chute_fora",
                artilheiro
            )

            return

        # goleiro defendeu?
        if self.goleiro_defendeu(
            clube_defendendo
        ):
            return

        # gol
        self.marcar_gol(
            clube_atacando,
            minuto,
            artilheiro
        )
    
    def gerar_finalizacao(
        self,
        clube_atacando,
        artilheiro
    ):

        chance_finalizacao = 0.25

        if random.random() > chance_finalizacao:
            return False

        if clube_atacando == self.clube1:
            self.finalizacoes_c1 += 1
        else:
            self.finalizacoes_c2 += 1

        if artilheiro:
            artilheiro.chutes_partida += 1

        return True
    
    def finalizacao_no_gol(
        self,
        clube_atacando,
        artilheiro
    ):

        chance_no_gol = 0.50 * self.fator_ataque(clube_atacando)

        if random.random() > chance_no_gol:
            return False

        if clube_atacando == self.clube1:
            self.finalizacoes_gol_c1 += 1
        else:
            self.finalizacoes_gol_c2 += 1

        if artilheiro:
            artilheiro.chutes_gol_partida += 1

        return True
    
    def goleiro_defendeu(
        self,
        clube
    ):

        goleiro = next(
            (
                j for j in clube.titulares
                if j.posicao == "Goleiro"
            ),
            None
        )

        if goleiro is None:
            return False

        chance_defesa = (
            0.14 +
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
        artilheiro
    ):
        
        if artilheiro is None:
            return

        # atualiza estatísticas do jogador
        artilheiro.gols += 1
        self.estatisticas[artilheiro]["gols"] += 1

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
            artilheiro
        )
    
    def simular_penalti_minuto(
        self,
        minuto
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
        
        if cobrador is None:
            return

        if random.random() < 0.80:

            cobrador.gols += 1
            cobrador.penaltis += 1

            self.estatisticas[cobrador]["gols"] += 1

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
    
    #Estatisticas Reais
    
    def gerar_drible(
        self,
        jogador
    ):

        if jogador.posicao == "Atacante":

            if random.random() < 0.40:
                jogador.dribles_partida += 1

        elif jogador.posicao == "Meio-Campo":

            if random.random() < 0.25:
                jogador.dribles_partida += 1
    
    def gerar_passe_chave(
        self,
        jogador
    ):

        if jogador.posicao == "Meio-Campo":

            if random.random() < 0.50:
                jogador.passes_chave_partida += 1

        elif jogador.posicao == "Atacante":

            if random.random() < 0.20:
                jogador.passes_chave_partida += 1
    
    #Ações Defensivas
    
    def simular_acao_defensiva(
        self,
        clube_defendendo
    ):

        defensores = [
            j for j in clube_defendendo.titulares
            if (
                j.posicao in [
                    "Defesa",
                    "Meio-Campo"
                ]
                and not j.expulso
            )
        ]

        if not defensores:
            return

        defensor = random.choice(
            defensores
        )

        self.gerar_desarme(
            defensor
        )

        self.gerar_interceptacao(
            defensor
        )

        self.gerar_corte(
            defensor
        )

        self.gerar_falta(
            defensor
        )
    
    def gerar_desarme(
        self,
        jogador
    ):

        if jogador.posicao == "Defesa":

            jogador.desarmes_partida += random.randint(
                0,
                2
            )

        elif jogador.posicao == "Meio-Campo":

            jogador.desarmes_partida += random.randint(
                0,
                1
            )
    
    def gerar_interceptacao(
        self,
        jogador
    ):

        if jogador.posicao == "Defesa":

            jogador.interceptacoes_partida += random.randint(
                0,
                2
            )

        elif jogador.posicao == "Meio-Campo":

            jogador.interceptacoes_partida += random.randint(
                0,
                1
            )
    
    def gerar_corte(
        self,
        jogador
    ):

        if jogador.posicao == "Defesa":

            jogador.cortes_partida += random.randint(
                0,
                3
            )
    
    def gerar_falta(
        self,
        jogador
    ):

        if random.random() < 0.20:

            jogador.faltas_partida += 1
    
    #Fadiga
    
    def atualizar_fadiga(self):

        jogadores = (
            self.clube1.titulares +
            self.clube2.titulares
        )

        for jogador in jogadores:
            jogador.reduzir_energia()

        # times que cansam perdem posse
        self.calcular_posse()
    
    def recuperar_energia(
        self,
        clube
    ):

        # quem jogou recupera parcialmente no intervalo entre rodadas
        for jogador in clube.titulares:

            jogador.energia += random.randint(
                20,
                32
            )

            jogador.energia = min(
                100,
                jogador.energia
            )

            jogador.atualizar_condicao()

        # quem ficou de fora recupera quase tudo
        for jogador in clube.reservas:

            jogador.energia += random.randint(
                55,
                80
            )

            jogador.energia = min(
                100,
                jogador.energia
            )

            jogador.atualizar_condicao()
    
    #Substituições
    
    def simular_substituicao(
        self,
        minuto
    ):

        # normalmente após os 60 minutos
        if minuto < 60:
            return

        if random.random() > 0.08:
            return

        clube = random.choice([
            self.clube1,
            self.clube2
        ])

        self.realizar_substituicao(
            clube,
            minuto
        )
    
    def escolher_substituto(
        self,
        clube,
        titular
    ):

        reservas = [
            j for j in clube.reservas
            if j.posicao == titular.posicao
        ]

        if not reservas:
            return None

        return random.choice(
            reservas
        )
    
    def realizar_substituicao(
        self,
        clube,
        minuto
    ):

        if clube == self.clube1:

            if self.substituicoes_c1 >= self.max_substituicoes:
                return

        else:

            if self.substituicoes_c2 >= self.max_substituicoes:
                return

        # jogadores de linha em campo neste momento (goleiro nao entra
        # no rodizio de substituicao)
        em_campo = [
            j for j in clube.titulares
            if not j.expulso
            and j.posicao != "Goleiro"
        ]

        if not em_campo:
            return

        em_campo.sort(
            key=lambda j: j.energia
        )

        saindo = em_campo[0]

        entrando = self.escolher_substituto(
            clube,
            saindo
        )

        if entrando is None:
            return

        # entra zerado (podia ter estatistica de partida antiga)
        entrando.resetar_estatisticas_partida()

        # a troca acontece so na escalacao da partida (titulares/reservas),
        # nunca em clube.jogadores, que e o elenco fixo da temporada
        clube.titulares.remove(saindo)
        clube.titulares.append(entrando)

        clube.reservas.remove(entrando)
        clube.reservas.append(saindo)

        self.substituicoes_log.append({
            "minuto": minuto,
            "sai": saindo,
            "entra": entrando,
        })

        if entrando not in self.estatisticas:

            self.estatisticas[entrando] = {
                "gols": 0,
                "assistencias": 0,
                "passes": 0,
                "desarmes": 0,
                "nota": 6.0,
            }

        if clube == self.clube1:
            self.substituicoes_c1 += 1
        else:
            self.substituicoes_c2 += 1

        self.adicionar_evento(
            minuto,
            "substituicao",
            entrando
        )
    
    #Escolhas
    
    def escolher_artilheiro(
        self,
        clube
    ):

        candidatos = []
        pesos = []

        for jogador in clube.titulares:

            if jogador.expulso or jogador.posicao == "Goleiro":
                continue

            peso = jogador.peso_gol()

            if peso > 0:
                candidatos.append(jogador)
                # ao quadrado: concentra os gols nos melhores finalizadores
                pesos.append(peso ** 2)

        if not candidatos:
            return None

        return random.choices(candidatos, weights=pesos, k=1)[0]
    
    def escolher_cobrador(self, clube):

        cobradores = [
            j for j in clube.titulares
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

        if not cobradores:
            return None

        return random.choices(
            cobradores,
            weights=pesos,
            k=1
        )[0]
    
    def distribuir_assistencia(
        self,
        clube,
        artilheiro
    ):

        lista = []

        for jogador in clube.titulares:

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
            self.estatisticas[assistente]["assistencias"] += 1
    
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
            j for j in clube.titulares
            if not j.expulso
        ]

        if not jogadores_validos:
            return

        jogador = random.choice(
            jogadores_validos
        )
        
        self.gerar_desarme(
            jogador
        )

        self.gerar_interceptacao(
            jogador
        )

        self.gerar_corte(
            jogador
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
            "substituicao": "🔄",
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

        self.estatisticas = {}

        # quem começou jogando (para o snapshot da escalação; um titular pode
        # sair e voltar quando o substituto entra por outro companheiro)
        self.titulares_iniciais = set(
            self.clube1.titulares + self.clube2.titulares
        )

        # so quem comeca jogando. Reservas entram no dict apenas se forem
        # acionados em realizar_substituicao (senao contariam jogo e nota
        # sem terem entrado em campo).
        for jogador in (
            self.clube1.titulares +
            self.clube2.titulares
        ):

            self.estatisticas[jogador] = {
                "gols":0,
                "assistencias":0,
                "passes":0,
                "desarmes":0,
                "nota":6.0
            }

        return self.estatisticas

    def verificar_hat_tricks(
        self,
    ):

        for jogador in self.estatisticas:

            if self.estatisticas[jogador]["gols"] >= 3:

                jogador.hat_tricks += 1

                print(
                    f"\n🎩 HAT-TRICK DE "
                    f"{jogador.nome}!"
                )
    
    def calcular_notas(self):

        melhor_jogador = None
        maior_nota = 0

        for jogador in self.estatisticas:

            nota = 6.0

            gols = self.estatisticas[jogador]["gols"]
            assistencias = self.estatisticas[jogador]["assistencias"]

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

                nota += gols * 1.6
                nota += assistencias * 1.0
                nota += jogador.chutes_gol_partida * 0.15
                nota += jogador.dribles_partida * 0.06

            elif jogador.posicao == "Meio-Campo":

                nota += gols * 1.3
                nota += assistencias * 1.2
                nota += jogador.passes_chave_partida * 0.09
                nota += jogador.interceptacoes_partida * 0.05
                nota += jogador.dribles_partida * 0.04

            elif jogador.posicao == "Defesa":

                nota += gols * 1.6
                nota += assistencias * 0.8
                nota += jogador.desarmes_partida * 0.07
                nota += jogador.interceptacoes_partida * 0.06
                nota += jogador.cortes_partida * 0.03

                if clean_sheet:
                    nota += 0.9

            elif jogador.posicao == "Goleiro":

                nota += jogador.defesas_partida * 0.10

                if clean_sheet:
                    nota += 0.8

                nota -= jogador.gols_sofridos_partida * 0.18

            # ==========================
            # RESULTADO
            # ==========================

            if saldo > 0:
                nota += 0.4

            elif saldo < 0:
                nota -= 0.25

            # ==========================
            # BÔNUS EXTRAS
            # ==========================

            if (
                jogador.posicao == "Atacante"
                and saldo >= 2
            ):
                nota += 0.3

            # atuação de destaque: dois ou mais gols
            if gols >= 2:
                nota += 0.4

            if (
                jogador.posicao in ("Atacante", "Meio-Campo")
                and gols > 0
                and assistencias > 0
            ):
                nota += 0.3

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

            # guarda a nota da partida (o snapshot em `atuacao` usa isto)
            self.estatisticas[jogador]["nota"] = round(nota, 2)

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
                        self.estatisticas[jogador]["gols"],
                        self.estatisticas[jogador]["assistencias"]
                    ) > (
                        self.estatisticas[melhor_jogador]["gols"],
                        self.estatisticas[melhor_jogador]["assistencias"]
                    )
                )
            ):
                melhor_jogador = jogador
                maior_nota = nota

        if melhor_jogador is not None:
            melhor_jogador.melhor_em_campo += 1

        return melhor_jogador, maior_nota
    
    def mostrar_melhor_em_campo(self, jogador, nota):

        print("\n⭐ MELHOR EM CAMPO")

        print(
            f"{jogador.nome} "
            f"({jogador.posicao}) "
            f"- Nota {nota:.1f}\n")

    #Snapshot para persistência / navegação

    def _clube_do(self, jogador):
        """Clube do jogador pelo elenco fixo da temporada, não pela escalação
        (o autor de um gol pode já ter sido substituído)."""

        return (
            self.clube1
            if jogador in self.clube1.jogadores
            else self.clube2
        )

    def resumo_eventos(self):
        """Timeline da partida como lista de dicts, em ordem cronológica.
        Chamar depois de `processar_eventos`."""

        sai_de = {
            s["entra"]: s["sai"].nome
            for s in self.substituicoes_log
        }

        linhas = []

        for evento in sorted(
            self.eventos,
            key=lambda e: e["minuto"]
        ):

            jogador = evento.get("jogador")

            clube = (
                self._clube_do(jogador)
                if jogador is not None
                else None
            )

            detalhe = None

            if (
                evento["tipo"] == "substituicao"
                and jogador in sai_de
            ):
                detalhe = f"sai {sai_de[jogador]}"

            linhas.append({
                "minuto": evento["minuto"],
                "tipo": evento["tipo"],
                "jogador": jogador.nome if jogador is not None else None,
                "clube": clube.nome if clube is not None else None,
                "detalhe": detalhe,
            })

        return linhas

    def resumo_escalacao(self):
        """Uma linha por jogador que entrou em campo: se foi titular, quando
        entrou/saiu, contribuição e nota. Chamar depois de `calcular_notas`."""

        # percorre as trocas em ordem: um titular pode sair e voltar (quando
        # o substituto entra no lugar de outro companheiro), então a última
        # troca é que vale.
        entrou_min = {}
        saiu_min = {}

        for troca in self.substituicoes_log:
            sai, entra, minuto = troca["sai"], troca["entra"], troca["minuto"]

            saiu_min[sai] = minuto

            saiu_min.pop(entra, None)  # voltou a campo
            if entra not in self.titulares_iniciais:
                entrou_min[entra] = minuto

        atuacoes = []

        for jogador, stats in self.estatisticas.items():

            titular = jogador in self.titulares_iniciais

            atuacoes.append({
                "jogador": jogador.nome,
                "clube": self._clube_do(jogador).nome,
                "posicao": jogador.posicao,
                "titular": titular,
                "entrou_min": None if titular else entrou_min.get(jogador),
                "saiu_min": saiu_min.get(jogador),
                "gols": stats["gols"],
                "assistencias": stats["assistencias"],
                "nota": stats["nota"],
            })

        return atuacoes
    
    #Resultado
    
    def recalcular_placar(self):

        gols_c1 = 0
        gols_c2 = 0

        for evento in self.eventos:

            if evento["tipo"] in ["gol", "penalti"]:

                jogador = evento["jogador"]

                # elenco fixo, nao a escalacao — o autor do gol pode ter
                # sido substituido antes do fim
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

        # credita o clean sheet so ao goleiro que estava em campo no fim
        # (titulares), dos dois lados igualmente.
        if self.gols_c2 == 0:

            for jogador in self.clube1.titulares:
                if jogador.posicao == "Goleiro":
                    jogador.clean_sheets += 1

        if self.gols_c1 == 0:

            for jogador in self.clube2.titulares:
                if jogador.posicao == "Goleiro":
                    jogador.clean_sheets += 1
            
    #Utilidade
    
    def forca_em_campo(self, clube):
        """Força do time neste momento: média de overall do XI ajustada por
        fadiga e expulsões (Clube.calcular_forca), mais o mando de campo se
        for o mandante."""

        forca = clube.calcular_forca()

        if clube is self.clube1:
            forca += self.MANDO_DE_CAMPO

        return forca

    def adversario(self, clube):

        if clube is self.clube1:
            return self.clube2

        return self.clube1

    def fator_ataque(self, clube_atacando):
        """Multiplicador da chance de gol: > 1 quando o ataque é mais forte
        que a defesa adversária, < 1 quando é mais fraco. Centrado em 1.

        A tática entra aqui: o clube ofensivo cria mais (mod_ataque) e o
        adversário defensivo concede menos (mod_defesa)."""

        adversario = self.adversario(clube_atacando)

        ataque = self.forca_em_campo(clube_atacando)
        defesa = self.forca_em_campo(adversario)

        if defesa <= 0:
            return 1.55

        fator = (ataque / defesa) ** 3
        fator *= clube_atacando.mod_ataque()
        fator /= adversario.mod_defesa()

        return max(0.7, min(1.55, fator))

    def calcular_posse(self):

        f1 = self.forca_em_campo(self.clube1)
        f2 = self.forca_em_campo(self.clube2)

        if f1 <= 0 or f2 <= 0:
            self.posse_c1 = 50
            self.posse_c2 = 50
            return

        # elevar a força a uma potência transforma diferenças pequenas de
        # overall em diferenças visíveis de posse
        peso1 = f1 ** 4
        peso2 = f2 ** 4

        self.posse_c1 = round(peso1 / (peso1 + peso2) * 100)
        self.posse_c2 = 100 - self.posse_c1

