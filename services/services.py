from models.models import Projeto
from repositories.repositories import ProjetoRepository


class ErroDeNegocio(Exception):
    def __init__(self, mensagem, status=400):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status = status


class ProjetoService:
    @staticmethod
    def listar(nome=None, departamento=None, ordenar=False):
        return ProjetoRepository.listar(nome, departamento, ordenar)

    @staticmethod
    def buscar(id):
        projeto = ProjetoRepository.buscar(id)
        if projeto is None:
            raise ErroDeNegocio("Projeto não encontrado", 404)
        return projeto

    @staticmethod
    def cadastrar(dados):
        if ProjetoRepository.buscar_por_nome(dados["nome"]):
            raise ErroDeNegocio("Projeto já cadastrado")
        projeto = Projeto(**dados)
        return ProjetoRepository.salvar(projeto)

    @staticmethod
    def atualizar(id, dados):
        projeto = ProjetoService.buscar(id)
        if "nome" in dados:
            outro = ProjetoRepository.buscar_por_nome(dados["nome"])
            if outro is not None and outro.id != projeto.id:
                raise ErroDeNegocio("Nome do projeto já utilizado")
        for campo, valor in dados.items():
            setattr(projeto, campo, valor)
        return ProjetoRepository.salvar(projeto)

    @staticmethod
    def excluir(id):
        projeto = ProjetoService.buscar(id)
        ProjetoRepository.excluir(projeto)

    @staticmethod
    def concluidos():
        return ProjetoRepository.concluidos()

    @staticmethod
    def alterar_status(id):
        projeto = ProjetoService.buscar(id)
        projeto.concluido = not projeto.concluido
        return ProjetoRepository.salvar(projeto)

    @staticmethod
    def estatisticas():
        return ProjetoRepository.estatisticas()
