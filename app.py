import os
from flask import Flask
from database import db


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///projetos.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if config:
        app.config.update(config)

    db.init_app(app)
    from models.models import Projeto  # registra o modelo antes de criar as tabelas
    from routers.routers import bp
    app.register_blueprint(bp)
    with app.app_context():
        db.create_all()
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
