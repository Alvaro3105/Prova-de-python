from repositories.Projeto import Projetos
from models.Projeto import Projeto

class services():
    @staticmethod
    def listar_projetos():
        return repositorio.listar_projetos()

    @staticmethod
    def buscar(id):
        return repositorio.buscar_projetos(id)
    
    @staticmethod
    def cadastrar():
        projeto.nome = dados["nome"]
        projeto.responsavel = dados["responsavel"]
        projeto.departamento = dados.get("departamento", "Geral")
        projeto.orcamento = float(dados["orcamento"])
        projeto.concluido = dados.get("concluido", False)

        if not dados:
            return jsonify({"erro": "JSON inválido"}), 
        
        if "nome" not in dados or len(dados["nome"]) < 3:
            return jsonify({"erro": "Nome do projeto muito curto"}), 
        
        if "responsavel" not in dados or len(dados["responsavel"]) < 3:
            return jsonify({"erro": "Responsável obrigatório"}),
        
        if "orcamento" not in dados or float(dados["orcamento"]) <= 0:
             return jsonify({"erro": "Orçamento deve ser maior que zero"}), 
    
    @staticmethod
    def atualizar(id):
        if projeto is None:
        return jsonify({"erro": "Projeto não encontrado"}), 

        dados = request.json
        if "nome" in dados:
            if len(dados["nome"]) < 3:
                return jsonify({"erro": "Nome inválido"}),

            outro = Projeto.query.filter_by(nome=dados["nome"]).first()
            if outro and outro.id != projeto.id:
                return jsonify({"erro": "Nome do projeto já utilizado"}), 
            projeto.nome = dados["nome"]

        if "responsavel" in dados:
            if len(dados["responsavel"]) < 3:
                return jsonify({"erro": "Responsável inválido"}), 
            projeto.responsavel = dados["responsavel"]

        if "departamento" in dados:
            projeto.departamento = dados["departamento"]

        if "orcamento" in dados:
            if float(dados["orcamento"]) <= 0:
                return jsonify({"erro": "Orçamento inválido"}), 
            projeto.orcamento = float(dados["orcamento"])

        if "concluido" in dados:
            projeto.concluido = dados["concluido"]

    
    @staticmethod
    def excluir(id):
        if projeto is None:
        return jsonify({"erro": "Projeto não encontrado"})

    @staticmethod
    def concluidos():
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
        return jsonify({"erro": "Projeto não encontrado"})


    @staticmethod
    def estatisticas():
        return jsonify({
        "total_projetos": total,
        "concluidos": concluidos,
        "departamentos": departamentos
    })