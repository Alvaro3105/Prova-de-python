from database import db
from datetime import datetime 
from models.models import Projeto


class repositorio():
    @staticmethod
    def index():
        return Projeto.query.order_by(Projeto.nome).all()

    @staticmethod
    def listar_projetos(name): 
        Projeto = Projeto.query.get(name)
        if nome:
            projetos = Projeto.query.filter(Projeto.nome.like(f"%{nome}%")).all()
        elif departamento:
            projetos = Projeto.query.filter_by(departamento=departamento).all()
        else:
            projetos = Projeto.query.all()
        return  Projeto
    
    @staticmethod
    def buscar_projetos(id):
       return  Projeto.query.get(id)

    @staticmethod
    def cadastrar_projeto(projeto):
        return Projeto.query.filter_by(nome=dados["nome"]).first()
        db.session.add(projeto)
        db.session.commit()
    
    @staticmethod
    def atualizar(id, projeto): 
        projeto = Projeto.query.get(id)
        outro = Projeto.query.filter_by(nome=dados["nome"]).first()
        db.session.commit()

    @staticmethod
    def excluir():
        projeto = Projeto.query.get(id)
        db.session.delete(projeto)
        db.session.commit()

    @staticmethod
    def concluidos():
        return Projeto.query.filter_by(concluido=True).order_by(Projeto.nome).all()

    @staticmethod
    def alterar_status(id):
        projeto = Projeto.query.get(id)
        db.session.commit()

    @staticmethod
    def estatisticas():
        total = Projeto.query.count()
        concluidos = Projeto.query.filter_by(concluido=True).count()
        departamentos = db.session.query(Projeto.departamento).distinct().count()

