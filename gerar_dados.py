import json
import random

NUM_CLUBES = 20

clubes_nomes = [
    "FC Taldo",
    "Real Taldo",
    "Taldo United",
    "Taldo City",
    "Atlético Taldo",
    "Sport Taldo",
    "Taldo Internacional",
    "Taldo Rangers",
    "Taldo Athletic",
    "EC Taldo",
    "Taldo Nacional",
    "Taldo Stars",
    "Taldo Sporting",
    "Taldo Galaxy",
    "Taldo Royals",
    "Taldo Warriors",
    "Taldo Legends",
    "Taldo Dragons",
    "Taldo Empire",
    "Taldo FC"
]

paises = [
    "Brasil",
    "Inglaterra",
    "Espanha",
    "Argentina",
    "Itália",
    "Alemanha",
    "Portugal",
    "França"
]

nomes = [
    "João","Pedro","Lucas","Gabriel","Miguel",
    "Arthur","Enzo","Matheus","Felipe","Rafael",
    "Bruno","Thiago","Diego","Carlos","André",
    "Vinicius","Caio","Leonardo","Gustavo","Rodrigo",
    "Juan","Pablo","Alejandro","Miguel","Diego",
    "Jack","Harry","Oliver","Noah","Liam",
    "Marco","Luca","Giovanni","Francesco",
    "Pierre","Louis","Antoine"
]

sobrenomes = [
    "Silva","Souza","Santos","Oliveira",
    "Ferreira","Costa","Almeida","Rocha",
    "Pereira","Lima","Gomes","Barbosa",
    "Ribeiro","Martins","Mendes","Araujo",
    "Rodriguez","Garcia","Lopez","Perez",
    "Fernandez","Wilson","Smith","Brown",
    "Taylor","Johnson","Walker","Rossi",
    "Bianchi","Moretti","Dubois","Martin"
]

nomes_usados = set()

def gerar_nome():

    while True:

        nome = (
            random.choice(nomes)
            + " "
            + random.choice(sobrenomes)
        )

        if nome not in nomes_usados:
            nomes_usados.add(nome)
            return nome


def gerar_idade():

    faixa = random.random()

    if faixa < 0.20:
        return random.randint(16,20)

    if faixa < 0.80:
        return random.randint(21,29)

    return random.randint(30,37)


def gerar_overall(posicao):

    sorteio = random.random()

    if sorteio < 0.05:
        base = random.randint(90,95)

    elif sorteio < 0.25:
        base = random.randint(85,89)

    elif sorteio < 0.70:
        base = random.randint(80,84)

    else:
        base = random.randint(72,79)

    if posicao == "Goleiro":
        base += random.randint(-2,2)

    return max(70, min(95, base))


jogadores = []
clubes = []

id_jogador = 1

for id_clube in range(NUM_CLUBES):

    clube = {
        "id": id_clube + 1,
        "nome": clubes_nomes[id_clube],
        "pais": random.choice(paises),
        "dinheiro": random.randint(
            1_000_000,
            50_000_000
        ),
        "torcedores": random.randint(
            10000,
            10000000
        ),
        "elenco": []
    }

    formacao = (
        ["Goleiro"] * 1 +
        ["Defesa"] * 4 +
        ["Meio-Campo"] * 3 +
        ["Atacante"] * 3
    )

    for posicao in formacao:

        jogador = {
            "id": id_jogador,
            "nome": gerar_nome(),
            "idade": gerar_idade(),
            "posicao": posicao,
            "overall": gerar_overall(posicao)
        }

        jogadores.append(jogador)
        clube["elenco"].append(id_jogador)

        id_jogador += 1

    clubes.append(clube)


# jogador especial
jogadores[13]["nome"] = "Isaque Souza"
jogadores[13]["idade"] = 18
jogadores[13]["posicao"] = "Meio-Campo"
jogadores[13]["overall"] = 99


with open(
    "data/jogadores.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        jogadores,
        f,
        ensure_ascii=False,
        indent=4
    )


with open(
    "data/clubes.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        clubes,
        f,
        ensure_ascii=False,
        indent=4
    )


print("=" * 40)
print("TALDO MANAGER - GERADOR DE DADOS")
print("=" * 40)
print(f"Clubes: {len(clubes)}")
print(f"Jogadores: {len(jogadores)}")
print("=" * 40)