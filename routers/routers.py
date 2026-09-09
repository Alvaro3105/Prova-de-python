from flask import Blueprint
from controllers.controllers import ProjetoController as controller

bp = Blueprint("projetos", __name__)
bp.add_url_rule("/", view_func=controller.index, methods=["GET"])
bp.add_url_rule("/projetos", view_func=controller.listar, methods=["GET"])
bp.add_url_rule("/projetos", view_func=controller.cadastrar, methods=["POST"])
bp.add_url_rule("/projetos/<int:id>", view_func=controller.buscar, methods=["GET"])
bp.add_url_rule("/projetos/<int:id>", view_func=controller.atualizar, methods=["PUT"])
bp.add_url_rule("/projetos/<int:id>", view_func=controller.excluir, methods=["DELETE"])
bp.add_url_rule("/concluidos", view_func=controller.concluidos, methods=["GET"])
bp.add_url_rule("/projetos/<int:id>/concluir", view_func=controller.alterar_status, methods=["PATCH"])
bp.add_url_rule("/estatisticas", view_func=controller.estatisticas, methods=["GET"])
