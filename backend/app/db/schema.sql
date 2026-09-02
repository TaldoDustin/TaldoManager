-- Schema do Taldo Manager (SQLite).
-- Cada simulação é um "save" independente: os clubes e jogadores são um
-- snapshot daquela temporada, não referências ao catálogo da seed.

CREATE TABLE IF NOT EXISTS simulacao (
    id         INTEGER PRIMARY KEY,
    seed       INTEGER,               -- NULL quando a temporada foi aleatória
    criada_em  TEXT NOT NULL,         -- ISO 8601 (UTC)
    campeao    TEXT NOT NULL,
    rodadas    INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS clube (
    id             INTEGER PRIMARY KEY,
    simulacao_id   INTEGER NOT NULL REFERENCES simulacao(id) ON DELETE CASCADE,
    nome           TEXT NOT NULL,
    pais           TEXT NOT NULL,
    posicao_final  INTEGER NOT NULL,
    pontos         INTEGER NOT NULL,
    jogos          INTEGER NOT NULL,
    vitorias       INTEGER NOT NULL,
    empates        INTEGER NOT NULL,
    derrotas       INTEGER NOT NULL,
    gols_marcados  INTEGER NOT NULL,
    gols_sofridos  INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS jogador (
    id              INTEGER PRIMARY KEY,
    simulacao_id    INTEGER NOT NULL REFERENCES simulacao(id) ON DELETE CASCADE,
    clube_id        INTEGER NOT NULL REFERENCES clube(id) ON DELETE CASCADE,
    nome            TEXT NOT NULL,
    posicao         TEXT NOT NULL,
    idade           INTEGER NOT NULL,
    overall         INTEGER NOT NULL,
    partidas        INTEGER NOT NULL,
    gols            INTEGER NOT NULL,
    assistencias    INTEGER NOT NULL,
    nota_media      REAL NOT NULL,
    melhor_nota     REAL NOT NULL,
    pior_nota       REAL NOT NULL,
    melhor_em_campo INTEGER NOT NULL,
    clean_sheets    INTEGER NOT NULL,
    hat_tricks      INTEGER NOT NULL,
    amarelos        INTEGER NOT NULL,
    vermelhos       INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS partida (
    id                     INTEGER PRIMARY KEY,
    simulacao_id           INTEGER NOT NULL REFERENCES simulacao(id) ON DELETE CASCADE,
    rodada                 INTEGER NOT NULL,
    mandante_id            INTEGER NOT NULL REFERENCES clube(id) ON DELETE CASCADE,
    visitante_id           INTEGER NOT NULL REFERENCES clube(id) ON DELETE CASCADE,
    gols_mandante          INTEGER NOT NULL,
    gols_visitante         INTEGER NOT NULL,
    posse_mandante         INTEGER NOT NULL,
    finalizacoes_mandante  INTEGER NOT NULL,
    finalizacoes_visitante INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_clube_simulacao   ON clube(simulacao_id);
CREATE INDEX IF NOT EXISTS ix_jogador_simulacao ON jogador(simulacao_id);
CREATE INDEX IF NOT EXISTS ix_jogador_clube     ON jogador(clube_id);
CREATE INDEX IF NOT EXISTS ix_partida_simulacao ON partida(simulacao_id);
CREATE INDEX IF NOT EXISTS ix_partida_mandante  ON partida(mandante_id);
CREATE INDEX IF NOT EXISTS ix_partida_visitante ON partida(visitante_id);
