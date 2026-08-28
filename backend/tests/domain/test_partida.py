from app.domain.partida import Partida
from app.domain.clube import Clube


def test_criar_partida():
    clube1 = Clube(
        "FC Taldo",
        "Brasil",
        1000000
    )

    clube2 = Clube(
        "Real Taldo",
        "Brasil",
        1000000
    )

    partida = Partida(clube1, clube2)

    assert partida.clube1 == clube1
    assert partida.clube2 == clube2
    assert partida.resultado is None
    assert partida.gols_c1 == 0
    assert partida.gols_c2 == 0
    
def test_simular_partida_funciona():
    clube1 = Clube(
        "FC Taldo",
        "Brasil",
        1000000
    )

    clube2 = Clube(
        "Real Taldo",
        "Brasil",
        1000000
    )

    partida = Partida(clube1, clube2)

    partida.simular_partida()

    assert partida.resultado is not None
    assert partida.gols_c1 >= 0
    assert partida.gols_c2 >= 0
    assert isinstance(partida.eventos, list)