"""Rotas HTTP da API do Taldo Manager."""

from fastapi import APIRouter, HTTPException, Query, Response

from app.api.schemas import (
    ClubeDetalhe,
    HealthResponse,
    SimulacaoCriada,
    SimulacaoResponse,
    SimulacaoResumo,
)
from app.services import simulacao_service

router = APIRouter()

_SEED_DESC = (
    "Semente aleatoria. Com o mesmo seed a simulacao e reproduzivel; "
    "sem seed cada chamada roda uma temporada nova."
)


@router.get("/health", response_model=HealthResponse, tags=["infra"])
def health():
    return {"status": "ok"}


@router.get("/simulacao", response_model=SimulacaoResponse, tags=["simulacao"])
def simulacao_rapida(seed: int | None = Query(default=None, description=_SEED_DESC)):
    """Roda uma temporada e devolve o resultado sem salvar (modo rápido)."""
    return simulacao_service.simular_temporada(seed=seed)


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
def criar_simulacao(seed: int | None = Query(default=None, description=_SEED_DESC)):
    """Roda uma temporada, salva no banco e devolve o id."""
    return {"id": simulacao_service.salvar_temporada(seed=seed)}


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
