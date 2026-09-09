from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///projetos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    responsavel = db.Column(db.String(100), nullable=False)
    departamento = db.Column(db.String(80), nullable=False)
    orcamento = db.Column(db.Float, nullable=False)
    concluido = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()

@app.route("/")
def index():
    projetos = Projeto.query.order_by(Projeto.nome).all()
    resultado = []
    for p in projetos:
        resultado.append({
            "id": p.id,
            "nome": p.nome,
            "responsavel": p.responsavel,
            "departamento": p.departamento,
            "orcamento": p.orcamento,
            "concluido": p.concluido
        })
    return jsonify(resultado)

@app.route("/projetos", methods=["GET"])
def listar():
    nome = request.args.get("nome")
    departamento = request.args.get("departamento")

    if nome:
        projetos = Projeto.query.filter(Projeto.nome.like(f"%{nome}%")).all()
    elif departamento:
        projetos = Projeto.query.filter_by(departamento=departamento).all()
    else:
        projetos = Projeto.query.all()

    dados = []
    for p in projetos:
        dados.append({
            "id": p.id,
            "nome": p.nome,
            "responsavel": p.responsavel,
            "departamento": p.departamento,
            "orcamento": p.orcamento,
            "concluido": p.concluido
        })
    return jsonify(dados)

@app.route("/projetos/<int:id>")
def buscar(id):
    projeto = Projeto.query.get(id)
    if not projeto:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    return jsonify({
        "id": projeto.id,
        "nome": projeto.nome,
        "responsavel": projeto.responsavel,
        "departamento": projeto.departamento,
        "orcamento": projeto.orcamento,
        "concluido": projeto.concluido
    })

@app.route("/projetos", methods=["POST"])
def cadastrar():
    dados = request.json
    if not dados:
        return jsonify({"erro": "JSON inválido"}), 400

    if "nome" not in dados or len(dados["nome"]) < 3:
        return jsonify({"erro": "Nome do projeto muito curto"}), 400

    if "responsavel" not in dados or len(dados["responsavel"]) < 3:
        return jsonify({"erro": "Responsável obrigatório"}), 400

    if "orcamento" not in dados or float(dados["orcamento"]) <= 0:
        return jsonify({"erro": "Orçamento deve ser maior que zero"}), 400

    existe = Projeto.query.filter_by(nome=dados["nome"]).first()
    if existe:
        return jsonify({"erro": "Projeto já cadastrado"}), 400

    projeto = Projeto()
    projeto.nome = dados["nome"]
    projeto.responsavel = dados["responsavel"]
    projeto.departamento = dados.get("departamento", "Geral")
    projeto.orcamento = float(dados["orcamento"])
    projeto.concluido = dados.get("concluido", False)

    db.session.add(projeto)
    db.session.commit()

    return jsonify({"mensagem": "Projeto cadastrado", "id": projeto.id})

@app.route("/projetos/<int:id>", methods=["PUT"])
def atualizar(id):
    projeto = Projeto.query.get(id)
    if projeto is None:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    dados = request.json
    if "nome" in dados:
        if len(dados["nome"]) < 3:
            return jsonify({"erro": "Nome inválido"}), 400

        outro = Projeto.query.filter_by(nome=dados["nome"]).first()
        if outro and outro.id != projeto.id:
            return jsonify({"erro": "Nome do projeto já utilizado"}), 400
        projeto.nome = dados["nome"]

    if "responsavel" in dados:
        if len(dados["responsavel"]) < 3:
            return jsonify({"erro": "Responsável inválido"}), 400
        projeto.responsavel = dados["responsavel"]

    if "departamento" in dados:
        projeto.departamento = dados["departamento"]

    if "orcamento" in dados:
        if float(dados["orcamento"]) <= 0:
            return jsonify({"erro": "Orçamento inválido"}), 400
        projeto.orcamento = float(dados["orcamento"])

    if "concluido" in dados:
        projeto.concluido = dados["concluido"]

    db.session.commit()
    return jsonify({"mensagem": "Projeto atualizado"})

@app.route("/projetos/<int:id>", methods=["DELETE"])
def excluir(id):
    projeto = Projeto.query.get(id)
    if projeto is None:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    db.session.delete(projeto)
    db.session.commit()
    return jsonify({"mensagem": "Projeto removido"})

@app.route("/concluidos")
def concluidos():
    projetos = Projeto.query.filter_by(concluido=True).order_by(Projeto.nome).all()
    lista = []
    for p in projetos:
        lista.append({
            "id": p.id,
            "nome": p.nome,
            "responsavel": p.responsavel,
            "orcamento": p.orcamento
        })
    return jsonify(lista)

@app.route("/projetos/<int:id>/concluir", methods=["PATCH"])
def alterar_status(id):
    projeto = Projeto.query.get(id)
    if projeto is None:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    projeto.concluido = not projeto.concluido
    db.session.commit()

    return jsonify({"mensagem": "Status alterado", "concluido": projeto.concluido})

@app.route("/estatisticas")
def estatisticas():
    total = Projeto.query.count()
    concluidos = Projeto.query.filter_by(concluido=True).count()
    departamentos = db.session.query(Projeto.departamento).distinct().count()

    return jsonify({
        "total_projetos": total,
        "concluidos": concluidos,
        "departamentos": departamentos
    })


if __name__ == "__main__":
    app.run(debug=True)