import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configurar logging para debug
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Criar a aplicação Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "easy-constru-secret-key-2024")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configurar banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///easyconstrul.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'

# Inicializar extensões
db.init_app(app)

@login_manager.user_loader
def carregar_usuario(usuario_id):
    from models import Usuario
    return Usuario.query.get(int(usuario_id))

# Criar tabelas e importar rotas
with app.app_context():
    # Importar modelos para que as tabelas sejam criadas
    import models
    
    # Criar todas as tabelas
    db.create_all()
    
    # Importar e registrar rotas
    from routes import main, auth, trabalhador, cliente, lojista, admin
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(trabalhador, url_prefix='/trabalhador')
    app.register_blueprint(cliente, url_prefix='/cliente')
    app.register_blueprint(lojista, url_prefix='/lojista')
    app.register_blueprint(admin, url_prefix='/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
