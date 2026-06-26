import json

from jogadores import Jogador
from clubes import Clube
from campeonatos import Campeonato

def carregar_jogadores():

    with open(
        "data/jogadores.json",
        encoding="utf-8"
    ) as arquivo:

        dados = json.load(arquivo)

    jogadores = {}

    for j in dados:

        jogadores[j["id"]] = Jogador(
            j["nome"],
            j["idade"],
            j["posicao"],
            j["overall"]
        )

    return jogadores

def carregar_clubes(jogadores):

    with open(
        "data/clubes.json",
        encoding="utf-8"
    ) as arquivo:

        dados = json.load(arquivo)

    clubes = []

    for c in dados:

        clube = Clube(
            c["nome"],
            c["pais"],
            c["dinheiro"],
            c["torcedores"]
        )

        for id_jogador in c["elenco"]:
            clube.contratar_jogador(
                jogadores[id_jogador]
            )

        clubes.append(clube)

    return clubes

def carregar_campeonato():

    jogadores = carregar_jogadores()

    clubes = carregar_clubes(jogadores)

    return Campeonato(
        "Taldo",
        clubes
    )