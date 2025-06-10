#!/usr/bin/env python3
"""
Script de instalação e configuração do EasyConstrul
Garante que o projeto funcione em qualquer ambiente
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verificar se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário. Versão atual:", sys.version)
        sys.exit(1)
    print("✅ Python", sys.version.split()[0], "detectado")

def install_dependencies():
    """Instalar dependências necessárias"""
    dependencies = [
        "flask>=2.0.0",
        "flask-sqlalchemy>=3.0.0", 
        "flask-login>=0.6.0",
        "flask-wtf>=1.0.0",
        "email-validator>=2.0.0",
        "gunicorn>=20.0.0"
    ]
    
    print("📦 Instalando dependências...")
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep], 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ {dep.split('>=')[0]} instalado")
        except subprocess.CalledProcessError:
            print(f"⚠️  Falha ao instalar {dep}")

def setup_database():
    """Configurar banco de dados"""
    project_dir = Path(__file__).parent.absolute()
    instance_dir = project_dir / 'instance'
    instance_dir.mkdir(exist_ok=True)
    
    db_path = instance_dir / 'easyconstrul.db'
    print(f"📊 Banco de dados: {db_path}")

def create_env_file():
    """Criar arquivo .env com configurações padrão"""
    env_content = """# Configurações do EasyConstrul
SECRET_KEY=easy-constru-development-key-2024-secure
FLASK_ENV=development
DATABASE_URL=sqlite:///instance/easyconstrul.db
PORT=5000
HOST=0.0.0.0
"""
    
    env_file = Path('.env')
    if not env_file.exists():
        env_file.write_text(env_content)
        print("✅ Arquivo .env criado")
    else:
        print("✅ Arquivo .env já existe")

def main():
    """Função principal de instalação"""
    print("🏗️  EasyConstrul - Script de Instalação")
    print("=" * 50)
    
    check_python_version()
    install_dependencies()
    setup_database()
    create_env_file()
    
    print("=" * 50)
    print("✅ Instalação concluída!")
    print("\n🚀 Para executar o projeto:")
    print("   python run.py")
    print("\n🌐 Acesse: http://localhost:5000")

if __name__ == '__main__':
    main()