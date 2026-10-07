-- ============================================================
-- VIEW: vw_situacao_alunos
--
-- POR QUE FOI CRIADA:
--   O dono da academia precisa saber, de uma so vez, quem esta em dia,
--   quem esta vencendo e quem esta inadimplente. Sem a View, essa
--   consulta (3 tabelas, subconsulta do ultimo pagamento, calculo de
--   vencimento e CASE) teria que ser repetida no codigo Python em
--   varias telas.
--
-- TABELAS ENVOLVIDAS: alunos, pagamentos, planos
--
-- O QUE RETORNA: uma linha por aluno com plano, ultimo pagamento,
--   data de vencimento, dias para vencer, total pago, quantidade de
--   pagamentos e a SITUACAO (Em dia / Vence em breve / Vencido /
--   Sem pagamento).
--
-- ONDE E USADA NA APLICACAO:
--   - Tela "Listar Alunos"            (interface_academia.py / menu Alunos)
--   - Tela "Relatorios > Situacao"    (interface_academia.py / menu Relatorios)
-- ============================================================

CREATE OR REPLACE VIEW vw_situacao_alunos AS
SELECT
    a.id                         AS aluno_id,
    a.nome,
    a.email,
    a.telefone,
    a.plano,
    a.data_cadastro,
    up.data_pagamento            AS ultimo_pagamento,
    up.data_vencimento,
    (up.data_vencimento - CURRENT_DATE)  AS dias_para_vencer,
    COALESCE(t.total_pago, 0)    AS total_pago,
    COALESCE(t.qtd_pagamentos, 0) AS qtd_pagamentos,
    CASE
        WHEN up.data_pagamento IS NULL                       THEN 'Sem pagamento'
        WHEN up.data_vencimento <  CURRENT_DATE              THEN 'Vencido'
        WHEN up.data_vencimento <= CURRENT_DATE + 7          THEN 'Vence em breve'
        ELSE 'Em dia'
    END                          AS situacao
FROM alunos a
-- ultimo pagamento de cada aluno e o vencimento dele (data + duracao do plano pago)
LEFT JOIN LATERAL (
    SELECT pg.data_pagamento,
           (pg.data_pagamento + (pl.duracao_meses * INTERVAL '1 month'))::date AS data_vencimento
    FROM pagamentos pg
    JOIN planos pl ON pl.id = pg.plano_id
    WHERE pg.aluno_id = a.id
    ORDER BY pg.data_pagamento DESC, pg.id DESC
    LIMIT 1
) up ON TRUE
-- totais de pagamentos por aluno
LEFT JOIN (
    SELECT aluno_id, SUM(valor) AS total_pago, COUNT(*) AS qtd_pagamentos
    FROM pagamentos
    GROUP BY aluno_id
) t ON t.aluno_id = a.id;
