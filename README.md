# EasyConstrul

Plataforma Flask para conectar trabalhadores da construção civil, clientes e fornecedores de materiais.

## 🚀 Como Executar

### Opção 1: Execução Simples
```bash
python run.py
```

### Opção 2: Execução Manual
```bash
python main.py
```

### Opção 3: Com Gunicorn (Produção)
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## 📋 Dependências

O projeto inclui todas as dependências necessárias:
- Flask
- Flask-SQLAlchemy  
- Flask-Login
- Flask-WTF
- Gunicorn
- Psycopg2-binary

## 🗄️ Banco de Dados

O sistema funciona automaticamente com SQLite por padrão. Para usar PostgreSQL em produção, defina a variável `DATABASE_URL`.

## 🔧 Configuração

### Variáveis de Ambiente (Opcionais)

```bash
# Chave secreta (gerada automaticamente se não definida)
SECRET_KEY=sua-chave-secreta

# URL do banco de dados (SQLite por padrão)
DATABASE_URL=sqlite:///instance/easyconstrul.db

# Ambiente (development por padrão)
FLASK_ENV=development

# Porta do servidor (5000 por padrão)
PORT=5000
```

## 👥 Tipos de Usuário

1. **Trabalhador**: Divulga serviços e recebe solicitações
2. **Cliente**: Busca profissionais e solicita serviços
3. **Lojista**: Anuncia materiais de construção
4. **Administrador**: Gerencia o sistema

## 🌐 Acesso

Após iniciar o servidor, acesse:
- **Local**: http://localhost:5000
- **Rede**: http://0.0.0.0:5000

## 📁 Estrutura do Projeto

```
easyconstrul/
├── app.py              # Configuração principal
├── config.py           # Configurações por ambiente
├── run.py              # Script de execução
├── main.py             # Ponto de entrada
├── models.py           # Modelos do banco
├── routes.py           # Rotas da aplicação
├── forms.py            # Formulários WTF
├── static/             # Arquivos estáticos
├── templates/          # Templates HTML
└── instance/           # Banco de dados SQLite
```

## 🔐 Segurança

- Senhas criptografadas com Werkzeug
- Autenticação via Flask-Login
- Proteção CSRF nos formulários
- Configurações seguras para produção

## 📱 Compatibilidade

- Funciona em qualquer sistema operacional
- Interface responsiva (mobile-friendly)
- Compatível com SQLite e PostgreSQL