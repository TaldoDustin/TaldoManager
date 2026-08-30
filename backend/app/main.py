"""Ponto de entrada da API (FastAPI).

Uso (a partir da pasta backend/):
    uvicorn app.main:app --reload

Docs interativas:  http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(
    title="Taldo Manager API",
    description="API de leitura para visualizar os resultados da simulacao.",
    version="0.1.0",
)

# Libera o frontend (index.html aberto localmente ou servido em outra porta).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["infra"])
def raiz():
    return {"api": "Taldo Manager", "docs": "/docs", "simulacao": "/simulacao"}
