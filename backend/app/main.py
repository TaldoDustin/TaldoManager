"""Ponto de entrada da API (FastAPI).

Uso (a partir da pasta backend/):
    uvicorn app.main:app --reload

Docs interativas:  http://localhost:8000/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.db.conexao import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Taldo Manager API",
    description="API para simular temporadas e navegar nos resultados.",
    version="0.2.0",
    lifespan=lifespan,
)

# Libera o frontend (index.html aberto localmente ou servido em outra porta).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["infra"])
def raiz():
    return {"api": "Taldo Manager", "docs": "/docs"}
