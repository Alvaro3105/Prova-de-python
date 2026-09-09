# Prova de Python — 2ª etapa

Revisão pós-avaliação de uma aplicação Flask de gerenciamento de projetos, organizada em MVC com Service e Repository. Este repositório reúne minha entrega original e uma versão revisada com apoio de IA, documentando os problemas encontrados e as soluções propostas.

## Contexto

A atividade exigia refatorar o arquivo legado `pft_a.py`, mantendo seus endpoints e respostas. A estrutura exigida separa inicialização, modelos, acesso a dados, regras de negócio, controllers e Blueprints. A versão inicial continua disponível no histórico do GitHub, sem alterações, para comparação.

## Executar

É necessário Python 3.10 ou superior. No terminal, na raiz do projeto:

```bash
python -m venv .venv
```

No Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

No Linux/macOS, ative com `source .venv/bin/activate`. O banco SQLite de desenvolvimento é criado automaticamente em `instance/projetos.db`. Não execute `pft_a.py` junto com o projeto refatorado.

## Endpoints

| Método | Rota | Função |
| --- | --- | --- |
| GET | `/` | Lista projetos ordenados por nome |
| GET | `/projetos` | Lista e filtra por `nome` ou `departamento` |
| GET | `/projetos/{id}` | Busca um projeto |
| POST | `/projetos` | Cadastra um projeto |
| PUT | `/projetos/{id}` | Atualiza um projeto |
| DELETE | `/projetos/{id}` | Exclui um projeto |
| GET | `/concluidos` | Lista projetos concluídos |
| PATCH | `/projetos/{id}/concluir` | Alterna o status de conclusão |
| GET | `/estatisticas` | Total de projetos, concluídos e departamentos |

Exemplo de cadastro em `POST /projetos`:

```json
{"nome":"Projeto Alfa","responsavel":"Maria","departamento":"TI","orcamento":1000,"concluido":false}
```

O cadastro mantém HTTP 200 e retorna `{"mensagem":"Projeto cadastrado","id":1}`. O comportamento foi preservado do legado, não substituído por uma API diferente.

## Testes

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Os testes utilizam um SQLite temporário e verificam CRUD, respostas, filtros, duplicidade, erros, estatísticas, alternância de status e isolamento do Repository. A execução local e os resultados de CI devem ser consultados antes de afirmar que todos passaram.

## Organização

```text
app.py
database.py
models/models.py
repositories/repositories.py
services/services.py
controllers/controllers.py
routers/routers.py
pft_a.py
requirements.txt
requirements-dev.txt
tests/
docs/revisao.md
```

O histórico permite comparar a entrega inicial com a revisão. Consulte [a análise das correções](docs/revisao.md) para entender os erros e as responsabilidades de cada camada.
