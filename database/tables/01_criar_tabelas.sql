-- ============================================================
-- TABELAS DO SISTEMA DE ACADEMIA
-- SGBD: PostgreSQL
-- Ordem de execucao: 1) tables  2) inserts  3) views  4) functions  5) procedures
-- ============================================================

CREATE TABLE IF NOT EXISTS planos (
    id            SERIAL PRIMARY KEY,
    nome          VARCHAR(50)   NOT NULL UNIQUE,
    preco         NUMERIC(10,2) NOT NULL,
    duracao_meses INT           NOT NULL
);

CREATE TABLE IF NOT EXISTS alunos (
    id            SERIAL PRIMARY KEY,
    nome          VARCHAR(100)  NOT NULL,
    email         VARCHAR(100)  UNIQUE,
    telefone      VARCHAR(20),
    plano         VARCHAR(50),
    data_cadastro DATE          DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS pagamentos (
    id             SERIAL PRIMARY KEY,
    aluno_id       INT REFERENCES alunos(id) ON DELETE CASCADE,
    plano_id       INT REFERENCES planos(id),
    data_pagamento DATE          DEFAULT CURRENT_DATE,
    valor          NUMERIC(10,2)
);
