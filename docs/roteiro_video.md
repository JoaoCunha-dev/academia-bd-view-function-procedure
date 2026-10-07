# Roteiro do vídeo explicativo (6 a 8 minutos)

Antes de gravar: banco criado com `executar_tudo.sql`, pgAdmin aberto com os 3 scripts, VS Code com `interface_academia.py` aberto e a interface rodando.

## 1. Apresentação do sistema (≈ 40 s)
- **Mostrar:** tela de login e menu lateral.
- **Falar:** o sistema gerencia alunos, planos e pagamentos de uma academia. O problema: saber quem está em dia ou inadimplente, calcular o valor certo da mensalidade e registrar o pagamento com segurança. Evoluí o CRUD do trabalho anterior, levando essa lógica para o banco (View, Function e Procedure).

## 2. Demonstração das telas (≈ 1 min)
Passar rapidamente por: **Listar Alunos**, **Cadastrar Aluno**, **Buscar Aluno**, **Pagamentos** e **Relatórios**.

## 3. View (≈ 1 min 30 s)
- **Mostrar:** `database/views/vw_situacao_alunos.sql` no editor ou pgAdmin.
- **Falar:** por que foi criada (consulta com 3 tabelas e regra de vencimento que seria repetida em várias telas); tabelas: `alunos`, `pagamentos`, `planos`; retorna uma linha por aluno com vencimento e situação.
- **Mostrar na prática:** `SELECT * FROM vw_situacao_alunos;` no pgAdmin e depois as telas **Listar Alunos** e **Relatórios > VIEW**, que usam essa View.

## 4. Function (≈ 1 min 30 s)
- **Mostrar:** `database/functions/fn_calcular_valor.sql`.
- **Falar:** recebe `p_aluno_id` e `p_plano_id`, retorna `NUMERIC(10,2)`; aplica 5% de desconto (3+ pagamentos) e 2% de multa (plano vencido).
- **Mostrar na prática:** no pgAdmin `SELECT fn_calcular_valor(3, 2);` (Carlos, vencido, com multa) e `SELECT fn_calcular_valor(1, 1);` (João, com desconto). Depois a tela **Pagamentos**, botão *Calcular valor (Function)*; mostrar no código `cur.execute("SELECT fn_calcular_valor(%s, %s)", ...)`.

## 5. Procedure (≈ 1 min 30 s)
- **Mostrar:** `database/procedures/sp_registrar_pagamento.sql`.
- **Falar:** parâmetros `p_aluno_id`, `p_plano_id`, `p_valor`; operações: valida, insere em `pagamentos`, atualiza o plano do aluno, tudo na mesma transação.
- **Mostrar no código:** `cur.execute("CALL sp_registrar_pagamento(%s, %s, %s)", ...)` na classe `PainelPagamentos`.
- **Mostrar na prática:** tentar valor `-5` (a procedure recusa e nada é gravado) e depois registrar com o valor correto.

## 6. Funcionamento integrado (≈ 1 min 30 s)
Fazer o fluxo completo, falando em voz alta cada etapa:
1. Em **Listar Alunos**, mostrar o Carlos como **Vencido**.
2. Em **Pagamentos**, escolher Carlos + Trimestral → **Calcular valor** (Function devolve com multa).
3. **Registrar pagamento** (Procedure grava).
4. Voltar em **Listar Alunos** / **Relatórios**: o Carlos agora está **Em dia** (View atualizada).

Frase de fechamento: *tela → chamada ao banco → View/Function/Procedure → resultado na aplicação*.

## Checklist da entrega (07/10/2026)
- [ ] README: preencher nome da disciplina, nome do professor e link do vídeo
- [ ] Repositório público no GitHub com a estrutura de pastas deste projeto
- [ ] Vídeo gravado e link colocado no README
- [ ] Link do repositório enviado na atividade
