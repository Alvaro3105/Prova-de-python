from sqlalchemy import distinct, func, select
from sqlalchemy.exc import SQLAlchemyError
from database import db
from models.models import Projeto


class ProjetoRepository:
    @staticmethod
    def listar(nome=None, departamento=None, ordenar=False):
        consulta = select(Projeto)
        if nome:
            consulta = consulta.where(Projeto.nome.like(f"%{nome}%"))
        elif departamento:
            consulta = consulta.where(Projeto.departamento == departamento)
        if ordenar:
            consulta = consulta.order_by(Projeto.nome)
        return db.session.execute(consulta).scalars().all()

    @staticmethod
    def buscar(id):
        return db.session.get(Projeto, id)

    @staticmethod
    def buscar_por_nome(nome):
        return db.session.execute(select(Projeto).where(Projeto.nome == nome)).scalar_one_or_none()

    @staticmethod
    def salvar(projeto):
        try:
            db.session.add(projeto)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
        return projeto

    @staticmethod
    def excluir(projeto):
        try:
            db.session.delete(projeto)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

    @staticmethod
    def concluidos():
        consulta = select(Projeto).where(Projeto.concluido.is_(True)).order_by(Projeto.nome)
        return db.session.execute(consulta).scalars().all()

    @staticmethod
    def estatisticas():
        return {
            "total_projetos": db.session.scalar(select(func.count()).select_from(Projeto)),
            "concluidos": db.session.scalar(select(func.count()).select_from(Projeto).where(Projeto.concluido.is_(True))),
            "departamentos": db.session.scalar(select(func.count(distinct(Projeto.departamento)))),
        }
