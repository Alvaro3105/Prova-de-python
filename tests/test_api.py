import pytest
from app import create_app
from database import db


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(tmp_path / "test.db")})
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.session.remove()
        db.drop_all()


def novo(client, nome="Projeto Alfa", **campos):
    dados = {"nome": nome, "responsavel": "Maria", "orcamento": 100.0}
    dados.update(campos)
    return client.post("/projetos", json=dados)


def test_crud_e_respostas_originais(client):
    assert client.get("/").json == []
    resposta = novo(client)
    assert resposta.status_code == 200
    assert resposta.json["mensagem"] == "Projeto cadastrado"
    id = resposta.json["id"]
    assert client.get(f"/projetos/{id}").json == {
        "id": id, "nome": "Projeto Alfa", "responsavel": "Maria",
        "departamento": "Geral", "orcamento": 100.0, "concluido": False,
    }
    assert client.put(f"/projetos/{id}", json={"orcamento": 150}).json == {"mensagem": "Projeto atualizado"}
    assert client.get(f"/projetos/{id}").json["orcamento"] == 150.0
    assert client.delete(f"/projetos/{id}").json == {"mensagem": "Projeto removido"}
    assert client.get(f"/projetos/{id}").status_code == 404
    assert client.put(f"/projetos/{id}", json={"nome": "Outro"}).status_code == 404
    assert client.delete(f"/projetos/{id}").status_code == 404


def test_filtros_ordenacao_e_estatisticas(client):
    a = novo(client, "Zeta", departamento="TI").json["id"]
    b = novo(client, "Alfa", departamento="RH", concluido=True).json["id"]
    assert [p["nome"] for p in client.get("/").json] == ["Alfa", "Zeta"]
    assert len(client.get("/projetos?nome=Zet").json) == 1
    assert [p["id"] for p in client.get("/projetos?departamento=RH").json] == [b]
    assert [p["id"] for p in client.get("/projetos?nome=Zet&departamento=RH").json] == [a]
    assert client.get("/concluidos").json == [{"id": b, "nome": "Alfa", "responsavel": "Maria", "orcamento": 100.0}]
    assert client.get("/estatisticas").json == {"total_projetos": 2, "concluidos": 1, "departamentos": 2}
    assert client.patch(f"/projetos/{a}/concluir").json == {"mensagem": "Status alterado", "concluido": True}
    assert client.patch(f"/projetos/{a}/concluir").json["concluido"] is False
    assert client.get("/estatisticas").json["concluidos"] == 1


def test_validacoes_e_duplicidade(client):
    for dados in [None, [], {"nome": "Ab", "responsavel": "Maria", "orcamento": 1},
                  {"nome": "Válido", "responsavel": "Ma", "orcamento": 1},
                  {"nome": "Válido", "responsavel": "Maria", "orcamento": 0},
                  {"nome": "Válido", "responsavel": "Maria", "orcamento": "abc"},
                  {"nome": "Válido", "responsavel": "Maria", "orcamento": float("inf")},
                  {"nome": "Válido", "responsavel": "Maria", "orcamento": 1, "concluido": "sim"}]:
        response = client.post("/projetos", json=dados) if dados is not None else client.post("/projetos", data="inválido", content_type="application/json")
        assert response.status_code == 400
        assert "erro" in response.json
    primeiro = novo(client).json["id"]
    assert novo(client).json == {"erro": "Projeto já cadastrado"}
    segundo = novo(client, "Projeto Beta").json["id"]
    assert client.put(f"/projetos/{segundo}", json={"nome": "Projeto Alfa"}).json == {"erro": "Nome do projeto já utilizado"}
    assert client.put(f"/projetos/{primeiro}", json={"nome": "Projeto Alfa"}).status_code == 200
    assert client.put(f"/projetos/{primeiro}", json={"orcamento": "infinito"}).status_code == 400
    assert client.get(f"/projetos/{primeiro}").json["orcamento"] == 100.0
    assert client.put(f"/projetos/{primeiro}", data="[]", content_type="application/json").status_code == 400
    assert client.patch("/projetos/999/concluir").status_code == 404


def test_repositorio_isolado_e_factory(client):
    import ast
    from pathlib import Path
    raiz = Path(__file__).resolve().parents[1]
    for arquivo in [raiz / "controllers/controllers.py", raiz / "services/services.py", raiz / "routers/routers.py"]:
        codigo = arquivo.read_text(encoding="utf-8")
        assert "db.session" not in codigo
        assert ".query." not in codigo
        assert "sqlalchemy" not in codigo.lower()
        ast.parse(codigo)
    assert client.get("/projetos").status_code == 200
