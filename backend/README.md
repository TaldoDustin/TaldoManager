# Backend — Taldo Manager

API FastAPI + engine de simulação + persistência em SQLite (`sqlite3` puro,
sem ORM). O roadmap do projeto fica no [README raiz](../README.md).

## Rodar

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- API: `http://localhost:8000`
- Docs interativas: `http://localhost:8000/docs`
- O banco local é criado em `data/database/taldo_manager.db` no primeiro
  start (gitignorado; o schema versionado é `app/db/schema.sql`). Dá pra
  trocar o caminho pela env `TALDO_DB`.

## Testes

```bash
cd backend
python -m pytest -q
```

`tests/conftest.py` dá um SQLite temporário por teste (nunca toca no banco
real).

## Organização

```text
app/
├── api/            rotas + schemas Pydantic
├── core/           config (caminho do banco, etc.)
├── db/             schema.sql + conexao.py (init_db idempotente no lifespan)
├── domain/         Jogador, Clube, Partida, Campeonato — a engine, sem I/O
├── repositories/   uma função pura por tabela, recebe a conn
├── services/       simulacao_service: _rodar -> _serializar -> _montar_visao
└── main.py         app FastAPI + CORS + lifespan
scripts/data_loader.py   monta o Campeonato a partir do seed JSON
```

### Fluxo de uma temporada

`simulacao_service` tem três entradas que produzem a mesma visão:

- `simular_temporada(seed)` — roda e devolve, **não** salva
- `salvar_temporada(seed)` — roda, persiste (simulação + clubes + jogadores
  + partidas + lances + atuações) e devolve o id
- `carregar_temporada(id)` — lê do banco

Mais: `detalhe_clube`, `detalhe_partida` (timeline + escalações com nota) e
`game_log_jogador` (nota partida a partida).

## Endpoints

| Método | Rota | O quê |
|---|---|---|
| `GET` | `/simulacao?seed=` | roda sem salvar (modo rápido) |
| `GET` | `/simulacoes` | lista as salvas |
| `POST` | `/simulacoes?seed=` | roda e salva |
| `GET` | `/simulacoes/{id}` | classificação, rankings, recordes |
| `DELETE` | `/simulacoes/{id}` | apaga (cascata) |
| `GET` | `/simulacoes/{id}/clubes/{clube_id}` | elenco + 38 jogos |
| `GET` | `/simulacoes/{id}/partidas/{partida_id}` | placar, stats, timeline, escalações |
| `GET` | `/simulacoes/{id}/jogadores/{jogador_id}` | ficha + game log |
