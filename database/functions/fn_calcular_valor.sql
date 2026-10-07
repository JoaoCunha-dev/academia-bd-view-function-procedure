-- ============================================================
-- FUNCTION: fn_calcular_valor(p_aluno_id, p_plano_id)
--
-- O QUE FAZ:
--   Calcula o valor que o aluno deve pagar ao contratar/renovar um plano.
--   Parte do preco do plano e aplica duas regras de negocio:
--     - Desconto de fidelidade de 5% para quem ja fez 3 ou mais pagamentos;
--     - Multa de 2% se o ultimo plano do aluno ja esta vencido.
--
-- PARAMETROS:
--   p_aluno_id INT  -> id do aluno
--   p_plano_id INT  -> id do plano que sera pago
--
-- RETORNO: NUMERIC(10,2) com o valor final a cobrar.
--   Gera erro se o aluno ou o plano nao existirem.
--
-- ONDE E USADA NA APLICACAO:
--   Tela "Pagamentos": o botao "Calcular valor" chama a Function e
--   preenche o campo de valor antes de confirmar o pagamento.
-- ============================================================

CREATE OR REPLACE FUNCTION fn_calcular_valor(p_aluno_id INT, p_plano_id INT)
RETURNS NUMERIC(10,2)
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    v_preco       NUMERIC(10,2);
    v_qtd         INT;
    v_vencimento  DATE;
    v_valor       NUMERIC(12,4);
BEGIN
    SELECT preco INTO v_preco FROM planos WHERE id = p_plano_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Plano % nao encontrado.', p_plano_id;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM alunos WHERE id = p_aluno_id) THEN
        RAISE EXCEPTION 'Aluno % nao encontrado.', p_aluno_id;
    END IF;

    v_valor := v_preco;

    -- Regra 1: desconto de fidelidade (3 ou mais pagamentos)
    SELECT COUNT(*) INTO v_qtd FROM pagamentos WHERE aluno_id = p_aluno_id;
    IF v_qtd >= 3 THEN
        v_valor := v_valor * 0.95;
    END IF;

    -- Regra 2: multa de 2% se o ultimo pagamento ja venceu
    SELECT (pg.data_pagamento + (pl.duracao_meses * INTERVAL '1 month'))::date
      INTO v_vencimento
      FROM pagamentos pg
      JOIN planos pl ON pl.id = pg.plano_id
     WHERE pg.aluno_id = p_aluno_id
     ORDER BY pg.data_pagamento DESC, pg.id DESC
     LIMIT 1;

    IF v_vencimento IS NOT NULL AND v_vencimento < CURRENT_DATE THEN
        v_valor := v_valor * 1.02;
    END IF;

    RETURN ROUND(v_valor, 2);
END;
$$;
