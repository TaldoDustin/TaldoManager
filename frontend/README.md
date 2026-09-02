# Frontend — Taldo Manager

Visualização básica dos resultados da simulação. **Sem build, sem npm**: é um
único arquivo `index.html` com JavaScript puro que consome a API.

## Como rodar

### 1. Suba a API (terminal 1)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000`. Docs interativas: `http://localhost:8000/docs`.

### 2. Sirva o frontend (terminal 2)

```bash
cd frontend
python -m http.server 5500
```

Abra `http://localhost:5500` no navegador e clique em **Nova temporada**.

> Dá pra abrir o `index.html` direto (dois cliques), mas servir via
> `http.server` evita problemas de CORS/caminho e é mais parecido com produção.

## O que dá pra fazer

- **Nova temporada** — roda e **salva** a simulação (SQLite). O campo *Seed*
  deixa reproduzível: mesmo seed → mesmo resultado.
- **Lista de simulações salvas** — troca entre temporadas já rodadas; **Apagar**
  remove a selecionada.
- **Visão da temporada** — campeão, MVP, classificação (com forma), artilharia,
  assistências, notas, clean sheets, hat-tricks, histórico, recordes.
- **Página do clube** — clique no nome de um clube na classificação: elenco
  completo + tabela das 38 partidas (mando, placar, resultado).
- **Página da partida** — clique no placar de um jogo: posse, finalizações,
  linha do tempo (gols, cartões, substituições) e as duas escalações com nota.
- **Página do jogador** — clique no nome em qualquer tabela: ficha + game log
  (nota, gols e assistências partida a partida).

O botão **← Voltar** desfaz a última navegação.

## Próximos passos

1. Gráfico da evolução da pontuação por rodada.
