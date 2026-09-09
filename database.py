from flask_sqlalchemy import SQLAlchemy

# A instância não depende da aplicação; evita importações circulares.
db = SQLAlchemy()
