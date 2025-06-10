import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from config import config

# Configurar logging
logging.basicConfig(level=logging.INFO)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def create_app(config_name=None):
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Determinar configuração
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Carregar configurações
    app.config.from_object(config.get(config_name, config['default']))
    config[config_name].init_app(app)
    
    # Configurar ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    # Configurar user_loader dentro do contexto da aplicação
    @login_manager.user_loader
    def load_user(user_id):
        from models import Usuario
        return Usuario.query.get(int(user_id))
    
    return app

# Criar aplicação
app = create_app()

# Inicializar aplicação
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
