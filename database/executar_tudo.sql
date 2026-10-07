-- ============================================================
-- Executa todos os scripts na ordem correta.
-- Uso (a partir da pasta /database, com o banco Academia_db ja criado):
--     psql -U postgres -d Academia_db -f executar_tudo.sql
-- ============================================================
\echo '>> 1/5 Tabelas'
\i tables/01_criar_tabelas.sql
\echo '>> 2/5 Dados de teste'
\i inserts/01_dados_iniciais.sql
\echo '>> 3/5 View'
\i views/vw_situacao_alunos.sql
\echo '>> 4/5 Function'
\i functions/fn_calcular_valor.sql
\echo '>> 5/5 Procedure'
\i procedures/sp_registrar_pagamento.sql
\echo '>> Pronto! Banco criado.'
