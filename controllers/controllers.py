from flask import request, jsonify
from services.services import projetos 
class controller():

    @staticmethod
    def index():

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

    @staticmethod
    def listar():
        nome = request.args.get("nome")
        departamento = request.args.get("departamento")
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

    @staticmethod
    def buscar(id):
            return jsonify({"erro": "Projeto não encontrado"}), 404

        return jsonify({
            "id": projeto.id,
            "nome": projeto.nome,
            "responsavel": projeto.responsavel,
            "departamento": projeto.departamento,
            "orcamento": projeto.orcamento,
            "concluido": projeto.concluido
        })

    @staticmethod
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

        return jsonify({"mensagem": "Projeto cadastrado", "id": projeto.id})

    @staticmethod
    def atualizar(id):
        if projeto is None:
            return jsonify({"erro": "Projeto não encontrado"}), 404

        dados = request.json
        if "nome" in dados:
            if len(dados["nome"]) < 3:
                return jsonify({"erro": "Nome inválido"}), 400

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

        return jsonify({"mensagem": "Projeto atualizado"})

    @staticmethod
    def excluir(id):
        if projeto is None:
            return jsonify({"erro": "Projeto não encontrado"}), 404

        return jsonify({"mensagem": "Projeto removido"})

    @staticmethod
    def concluidos():
        lista = []
        for p in projetos:
            lista.append({
                "id": p.id,
                "nome": p.nome,
                "responsavel": p.responsavel,
                "orcamento": p.orcamento
            })
        return jsonify(lista)

    @staticmethod
    def alterar_status(id):
        
        if projeto is None:
            return jsonify({"erro": "Projeto não encontrado"}), 404

        projeto.concluido = not projeto.concluido

        return jsonify({"mensagem": "Status alterado", "concluido": projeto.concluido})

    @staticmethod
    def estatisticas():
        return jsonify({
            "total_projetos": total,
            "concluidos": concluidos,
            "departamentos": departamentos
        })