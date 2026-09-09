# Revisão pós-prova — Python, 2ª etapa

A comparação foi feita com o enunciado e com o commit original `1c89cf1cc2f59b0e6264bdc9d149ae67ff74caae`. Os problemas abaixo foram identificados no código entregue; não são uma transcrição de descontos atribuídos pelo professor.

| Arquivo | Problema encontrado | Correção na revisão |
| --- | --- | --- |
| database.py e app.py | `SQLAlchemy(app)` usava `app` inexistente, e `init_app` era chamado sem instância. | Instância global `SQLAlchemy()` e inicialização em `create_app`. |
| services/services.py | Imports para módulos inexistentes, indentação incorreta, variáveis indefinidas e retorno de `jsonify` na regra de negócio. | Imports corretos, serviços independentes de HTTP e exceções de negócio. |
| repositories/repositories.py | Variáveis `nome`, `departamento`, `dados` e `id` fora do escopo; código depois de `return`; consultas sem retorno. | Métodos completos de consulta, gravação, exclusão e estatísticas com sessão isolada. |
| controllers/controllers.py | Erros de indentação, variáveis indefinidas, ausência de chamadas ao Service e consulta direta ao banco. | Validação de entrada, serialização e tratamento de exceções. |
| routers/routers.py | Blueprint criado sem registrar as nove rotas originais. | Registro completo de rotas e métodos HTTP. |
| Projeto | Faltavam requirements, testes e documentação. | Dependências declaradas, testes de regressão e instruções de execução. |

## Decisões de compatibilidade

O arquivo `pft_a.py` é mantido sem alterações. A revisão preserva os nove endpoints, os nomes das chaves JSON, a prioridade do filtro por nome, os códigos de status originais e o comportamento de alternar `concluido`. O cadastro continua retornando 200, como no legado. As validações adicionais evitam erros 500 para JSON malformado, números inválidos e tipos incompatíveis. Não foi adicionada autenticação ou alterado o esquema do banco, pois isso extrapolaria a refatoração arquitetural pedida.

## Como estudar

Leia o legado e identifique uma operação, por exemplo cadastrar. Acompanhe a mesma operação na sequência Router → Controller → Service → Repository → Model. Observe que somente o Repository executa consultas e commits. Em seguida, execute os testes e tente implementar uma operação semelhante sem consultar a versão revisada.

A implementação desta revisão foi preparada com apoio de ChatGPT e deve ser estudada e validada pelo aluno antes de ser apresentada como experiência própria.
