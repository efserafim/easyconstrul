#!/usr/bin/env python3
"""
Script principal para executar a aplicação EasyConstrul
Este script garante que a aplicação funcione em qualquer ambiente
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório do projeto ao Python path
project_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_dir))

def setup_environment():
    """Configurar variáveis de ambiente necessárias"""
    
    # Definir chave secreta se não estiver definida
    if not os.environ.get('SECRET_KEY'):
        os.environ['SECRET_KEY'] = 'easy-constru-development-key-2024-secure'
    
    # Definir ambiente Flask se não estiver definido
    if not os.environ.get('FLASK_ENV'):
        os.environ['FLASK_ENV'] = 'development'
    
    # Definir URL do banco se não estiver definida (usar SQLite simples)
    if not os.environ.get('DATABASE_URL'):
        os.environ['DATABASE_URL'] = 'sqlite:///easyconstrul.db'

def main():
    """Função principal para executar a aplicação"""
    
    print("🏗️  Iniciando EasyConstrul...")
    print("=" * 50)
    
    # Configurar ambiente
    setup_environment()
    
    try:
        # Importar e executar a aplicação
        from app import app
        
        print("✅ Aplicação configurada com sucesso!")
        print("📊 Banco de dados:", os.environ.get('DATABASE_URL'))
        print("🌐 Ambiente:", os.environ.get('FLASK_ENV'))
        print("🔑 Chave secreta configurada:", "✅" if os.environ.get('SECRET_KEY') else "❌")
        print("=" * 50)
        print("🚀 Servidor iniciando em http://0.0.0.0:5000")
        print("📱 Acesse a aplicação no seu navegador!")
        print("=" * 50)
        
        # Executar aplicação
        port = int(os.environ.get('PORT', 5000))
        host = os.environ.get('HOST', '0.0.0.0')
        debug = os.environ.get('FLASK_ENV') == 'development'
        
        app.run(host=host, port=port, debug=debug)
        
    except ImportError as e:
        print("❌ Erro ao importar dependências:")
        print(f"   {e}")
        print("\n💡 Verifique se todas as dependências estão instaladas:")
        print("   pip install flask flask-sqlalchemy flask-login flask-wtf email-validator")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()