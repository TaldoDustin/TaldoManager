"""Rotas HTTP da API do Taldo Manager."""

from fastapi import APIRouter, HTTPException, Query, Response

from app.api.schemas import (
    ClubeDetalhe,
    ClubeSeed,
    HealthResponse,
    JogadorDetalhe,
    PartidaDetalhe,
    SimulacaoCriada,
    SimulacaoResponse,
    SimulacaoResumo,
    Tatica,
)
from app.services import simulacao_service

router = APIRouter()

_SEED_DESC = (
    "Semente aleatoria. Com o mesmo seed a simulacao e reproduzivel; "
    "sem seed cada chamada roda uma temporada nova."
)
_CLUBE_DESC = (
    "Nome do clube que o usuario 'dirige'. So esse clube usa a tatica "
    "escolhida; os outros seguem neutros. Omitir = temporada neutra."
)
_TATICA_DESC = "Postura do clube dirigido (ignorada sem 'clube')."


def _simular(salvar, seed, clube, tatica):
    """Chama o serviço traduzindo ValueError -> 400."""
    fn = (
        simulacao_service.salvar_temporada
        if salvar
        else simulacao_service.simular_temporada
    )
    try:
        return fn(seed=seed, clube_usuario=clube, tatica=tatica)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/health", response_model=HealthResponse, tags=["infra"])
def health():
    return {"status": "ok"}


@router.get("/clubes", response_model=list[ClubeSeed], tags=["infra"])
def listar_clubes():
    """Os clubes do seed — para o usuário escolher qual dirigir."""
    return simulacao_service.listar_clubes()


@router.get("/simulacao", response_model=SimulacaoResponse, tags=["simulacao"])
def simulacao_rapida(
    seed: int | None = Query(default=None, description=_SEED_DESC),
    clube: str | None = Query(default=None, description=_CLUBE_DESC),
    tatica: Tatica = Query(default="equilibrado", description=_TATICA_DESC),
):
    """Roda uma temporada e devolve o resultado sem salvar (modo rápido)."""
    return _simular(False, seed, clube, tatica)


@router.get("/simulacoes", response_model=list[SimulacaoResumo], tags=["simulacoes"])
def listar_simulacoes():
    """Lista as simulações salvas, da mais recente para a mais antiga."""
    return simulacao_service.listar_simulacoes()


@router.post(
    "/simulacoes",
    response_model=SimulacaoCriada,
    status_code=201,
    tags=["simulacoes"],
)
def criar_simulacao(
    seed: int | None = Query(default=None, description=_SEED_DESC),
    clube: str | None = Query(default=None, description=_CLUBE_DESC),
    tatica: Tatica = Query(default="equilibrado", description=_TATICA_DESC),
):
    """Roda uma temporada, salva no banco e devolve o id."""
    return {"id": _simular(True, seed, clube, tatica)}


@router.get(
    "/simulacoes/{simulacao_id}",
    response_model=SimulacaoResponse,
    tags=["simulacoes"],
)
def obter_simulacao(simulacao_id: int):
    """Classificação, rankings e recordes de uma simulação salva."""
    visao = simulacao_service.carregar_temporada(simulacao_id)
    if visao is None:
        raise HTTPException(status_code=404, detail="Simulação não encontrada")
    return visao


@router.delete("/simulacoes/{simulacao_id}", status_code=204, tags=["simulacoes"])
def apagar_simulacao(simulacao_id: int):
    if not simulacao_service.apagar_simulacao(simulacao_id):
        raise HTTPException(status_code=404, detail="Simulação não encontrada")
    return Response(status_code=204)


@router.get(
    "/simulacoes/{simulacao_id}/clubes/{clube_id}",
    response_model=ClubeDetalhe,
    tags=["simulacoes"],
)
def obter_clube(simulacao_id: int, clube_id: int):
    """Elenco e tabela de jogos de um clube dentro de uma simulação."""
    detalhe = simulacao_service.detalhe_clube(simulacao_id, clube_id)
    if detalhe is None:
        raise HTTPException(status_code=404, detail="Clube não encontrado")
    return detalhe


@router.get(
    "/simulacoes/{simulacao_id}/partidas/{partida_id}",
    response_model=PartidaDetalhe,
    tags=["simulacoes"],
)
def obter_partida(simulacao_id: int, partida_id: int):
    """Placar, estatísticas, timeline e escalações de uma partida."""
    detalhe = simulacao_service.detalhe_partida(simulacao_id, partida_id)
    if detalhe is None:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return detalhe


@router.get(
    "/simulacoes/{simulacao_id}/jogadores/{jogador_id}",
    response_model=JogadorDetalhe,
    tags=["simulacoes"],
)
def obter_jogador(simulacao_id: int, jogador_id: int):
    """Ficha do jogador e o game log (nota partida a partida)."""
    detalhe = simulacao_service.game_log_jogador(simulacao_id, jogador_id)
    if detalhe is None:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return detalhe
