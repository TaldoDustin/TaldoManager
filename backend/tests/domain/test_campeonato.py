from app.domain.campeonato import Campeonato
from app.domain.clube import Clube


def test_criar_campeonato():
    clubes = [
        Clube("FC Taldo", "Brasil", 1000000),
        Clube("Real Taldo", "Brasil", 1000000),
        Clube("Taldo United", "Brasil", 1000000),
        Clube("Taldo City", "Brasil", 1000000),
    ]

    campeonato = Campeonato(
        "Campeonato Taldo",
        clubes
    )

    assert campeonato.nome == "Campeonato Taldo"
    assert campeonato.clubes == clubes
    assert campeonato.rodada == 1
    assert campeonato.historico == []
    assert campeonato.calendario is not None