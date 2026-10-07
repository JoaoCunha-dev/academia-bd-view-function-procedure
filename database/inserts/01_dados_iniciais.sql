-- ============================================================
-- DADOS PARA TESTAR O SISTEMA
-- As datas dos pagamentos sao relativas a CURRENT_DATE, assim a View
-- sempre mostra as quatro situacoes (Em dia, Vence em breve, Vencido
-- e Sem pagamento), independentemente do dia em que o script rodar.
-- Pode ser executado mais de uma vez sem duplicar dados.
-- ============================================================

INSERT INTO planos (nome, preco, duracao_meses) VALUES
    ('Mensal',     99.90,  1),
    ('Trimestral', 249.90, 3),
    ('Anual',      799.90, 12)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO alunos (nome, email, telefone, plano) VALUES
    ('Joao Silva',  'joao@email.com',   '86999991111', 'Mensal'),
    ('Maria Souza', 'maria@email.com',  '86999992222', 'Anual'),
    ('Carlos Lima', 'carlos@email.com', '86999993333', 'Trimestral'),
    ('Ana Paula',   'ana@email.com',    '86999994444', 'Mensal'),
    ('Pedro Alves', 'pedro@email.com',  '86999995555', 'Anual')
ON CONFLICT (email) DO NOTHING;

-- Pagamentos de exemplo (so insere se a tabela estiver vazia)
INSERT INTO pagamentos (aluno_id, plano_id, data_pagamento, valor)
SELECT a.id, pl.id, CURRENT_DATE - v.dias_atras, v.valor
FROM (VALUES
    ('joao@email.com',   'Mensal',      70,  99.90),   -- 3 pagamentos: ganha desconto de fidelidade
    ('joao@email.com',   'Mensal',      40,  99.90),
    ('joao@email.com',   'Mensal',      10,  99.90),   -- vence daqui a ~20 dias  -> Em dia
    ('maria@email.com',  'Anual',       30, 799.90),   -- vence daqui a ~11 meses -> Em dia
    ('carlos@email.com', 'Trimestral', 120, 249.90),   -- venceu ha ~30 dias      -> Vencido (multa)
    ('ana@email.com',    'Mensal',      28,  99.90)    -- vence em ~2 dias        -> Vence em breve
) AS v(email, plano, dias_atras, valor)
JOIN alunos a  ON a.email = v.email
JOIN planos pl ON pl.nome = v.plano
WHERE NOT EXISTS (SELECT 1 FROM pagamentos);
-- Pedro Alves fica sem pagamento de proposito -> Sem pagamento
