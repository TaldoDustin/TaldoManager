"""Rotas HTTP da API do Taldo Manager."""

from fastapi import APIRouter, Query

from app.api.schemas import HealthResponse, SimulacaoResponse
from app.services.simulacao_service import simular_temporada

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["infra"])
def health():
    return {"status": "ok"}


@router.get("/simulacao", response_model=SimulacaoResponse, tags=["simulacao"])
def simulacao(
    seed: int | None = Query(
        default=None,
        description=(
            "Semente aleatoria. Com o mesmo seed a simulacao e reproduzivel; "
            "sem seed cada chamada roda uma temporada nova."
        ),
    ),
):
    """Roda uma temporada completa e devolve classificacao, rankings e recordes."""
    return simular_temporada(seed=seed)
