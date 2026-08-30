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

Abra `http://localhost:5500` no navegador e clique em **Simular temporada**.

> Dá pra abrir o `index.html` direto (dois cliques), mas servir via
> `http.server` evita problemas de CORS/caminho e é mais parecido com produção.

## O que dá pra ver

- Campeão e MVP da temporada
- Classificação completa (com forma recente)
- Artilharia, assistências, melhores notas, clean sheets, hat-tricks
- Histórico de todas as partidas
- Recordes do campeonato

O campo **Seed** deixa a simulação reproduzível: mesmo seed → mesmo resultado.

## Próximos passos sugeridos

1. Separar o JS em `app.js` e adicionar um seletor de clube (ver elenco).
2. Um gráfico simples da evolução da pontuação por rodada.
3. Quando quiser aprender componentes/estado: migrar para Vite + React
   reaproveitando os mesmos endpoints.
