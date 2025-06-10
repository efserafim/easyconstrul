import os
from pathlib import Path

class Config:
    """Configuração base da aplicação"""
    
    # Diretório base do projeto
    BASE_DIR = Path(__file__).parent.absolute()
    
    # Chave secreta - usar variável de ambiente ou padrão seguro
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'easy-constru-development-key-2024-secure'
    
    # Configuração do banco de dados
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        # Criar diretório instance se não existir
        instance_dir = BASE_DIR / 'instance'
        instance_dir.mkdir(exist_ok=True)
        DATABASE_URL = f'sqlite:///{instance_dir}/easyconstrul.db'
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }
    
    # Configurações de desenvolvimento
    DEBUG = os.environ.get('FLASK_ENV') != 'production'
    
    # Configurações de sessão
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configurações de upload (para futuras funcionalidades)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Configurações de email (para futuras funcionalidades)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    @staticmethod
    def init_app(app):
        """Inicializar configurações específicas da aplicação"""
        pass

class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log para stderr em produção
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Mapa de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}