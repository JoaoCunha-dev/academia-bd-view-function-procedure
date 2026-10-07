-- ============================================================
-- PROCEDURE: sp_registrar_pagamento(p_aluno_id, p_plano_id, p_valor)
--
-- O QUE FAZ (processo com varias operacoes, na mesma transacao):
--   1. Valida aluno, plano e valor;
--   2. Insere o pagamento na tabela pagamentos;
--   3. Atualiza o plano do aluno (alunos.plano) para o plano pago.
--   Se qualquer validacao falhar, nada e gravado.
--
-- PARAMETROS:
--   p_aluno_id INT      -> aluno que esta pagando
--   p_plano_id INT      -> plano pago
--   p_valor    NUMERIC  -> valor pago (deve ser maior que zero)
--
-- ONDE E CHAMADA NA APLICACAO:
--   Tela "Pagamentos": o botao "Registrar pagamento" executa
--   CALL sp_registrar_pagamento(...)
-- ============================================================

CREATE OR REPLACE PROCEDURE sp_registrar_pagamento(
    p_aluno_id INT,
    p_plano_id INT,
    p_valor    NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_nome_plano VARCHAR(50);
BEGIN
    IF NOT EXISTS (SELECT 1 FROM alunos WHERE id = p_aluno_id) THEN
        RAISE EXCEPTION 'Aluno % nao encontrado.', p_aluno_id;
    END IF;

    SELECT nome INTO v_nome_plano FROM planos WHERE id = p_plano_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Plano % nao encontrado.', p_plano_id;
    END IF;

    IF p_valor IS NULL OR p_valor <= 0 THEN
        RAISE EXCEPTION 'Valor do pagamento deve ser maior que zero.';
    END IF;

    INSERT INTO pagamentos (aluno_id, plano_id, data_pagamento, valor)
    VALUES (p_aluno_id, p_plano_id, CURRENT_DATE, p_valor);

    UPDATE alunos SET plano = v_nome_plano WHERE id = p_aluno_id;
END;
$$;
