import math
from flask import jsonify, request
from services.services import ErroDeNegocio, ProjetoService


def serializar(projeto, resumido=False):
    dados = {
        "id": projeto.id,
        "nome": projeto.nome,
        "responsavel": projeto.responsavel,
        "orcamento": projeto.orcamento,
    }
    if not resumido:
        dados["departamento"] = projeto.departamento
        dados["concluido"] = projeto.concluido
    return dados


def validar_json():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict) or not dados:
        raise ErroDeNegocio("JSON inválido")
    return dados


def validar_texto(dados, campo, mensagem, obrigatorio=False, limite=255):
    if campo not in dados:
        if obrigatorio:
            raise ErroDeNegocio(mensagem)
        return
    valor = dados[campo]
    if not isinstance(valor, str) or len(valor) < 3 or len(valor) > limite:
        raise ErroDeNegocio(mensagem)


def validar_dados(dados, cadastro=False):
    validar_texto(dados, "nome", "Nome do projeto muito curto" if cadastro else "Nome inválido", cadastro, 120)
    validar_texto(dados, "responsavel", "Responsável obrigatório" if cadastro else "Responsável inválido", cadastro, 100)
    if "departamento" in dados and (not isinstance(dados["departamento"], str) or not dados["departamento"] or len(dados["departamento"]) > 80):
        raise ErroDeNegocio("Departamento inválido")
    if "orcamento" not in dados and cadastro:
        raise ErroDeNegocio("Orçamento deve ser maior que zero")
    if "orcamento" in dados:
        try:
            valor = float(dados["orcamento"])
        except (TypeError, ValueError, OverflowError):
            raise ErroDeNegocio("Orçamento deve ser maior que zero" if cadastro else "Orçamento inválido")
        if not math.isfinite(valor) or valor <= 0:
            raise ErroDeNegocio("Orçamento deve ser maior que zero" if cadastro else "Orçamento inválido")
        dados["orcamento"] = valor
    if "concluido" in dados and not isinstance(dados["concluido"], bool):
        raise ErroDeNegocio("Concluído deve ser verdadeiro ou falso")
    permitidos = {"nome", "responsavel", "departamento", "orcamento", "concluido"}
    dados = {k: v for k, v in dados.items() if k in permitidos}
    if cadastro:
        dados.setdefault("departamento", "Geral")
        dados.setdefault("concluido", False)
    return dados


def responder(funcao):
    try:
        return funcao()
    except ErroDeNegocio as erro:
        return jsonify({"erro": erro.mensagem}), erro.status


class ProjetoController:
    @staticmethod
    def index():
        return responder(lambda: jsonify([serializar(p) for p in ProjetoService.listar(ordenar=True)]))

    @staticmethod
    def listar():
        return responder(lambda: jsonify([serializar(p) for p in ProjetoService.listar(
            request.args.get("nome"), request.args.get("departamento"))]))

    @staticmethod
    def buscar(id):
        return responder(lambda: jsonify(serializar(ProjetoService.buscar(id))))

    @staticmethod
    def cadastrar():
        def executar():
            dados = validar_dados(validar_json(), cadastro=True)
            projeto = ProjetoService.cadastrar(dados)
            return jsonify({"mensagem": "Projeto cadastrado", "id": projeto.id})
        return responder(executar)

    @staticmethod
    def atualizar(id):
        def executar():
            projeto = ProjetoService.buscar(id)
            dados = validar_dados(validar_json())
            ProjetoService.atualizar(projeto.id, dados)
            return jsonify({"mensagem": "Projeto atualizado"})
        return responder(executar)

    @staticmethod
    def excluir(id):
        def executar():
            ProjetoService.excluir(id)
            return jsonify({"mensagem": "Projeto removido"})
        return responder(executar)

    @staticmethod
    def concluidos():
        return responder(lambda: jsonify([serializar(p, resumido=True) for p in ProjetoService.concluidos()]))

    @staticmethod
    def alterar_status(id):
        def executar():
            projeto = ProjetoService.alterar_status(id)
            return jsonify({"mensagem": "Status alterado", "concluido": projeto.concluido})
        return responder(executar)

    @staticmethod
    def estatisticas():
        return responder(lambda: jsonify(ProjetoService.estatisticas()))
