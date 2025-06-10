from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(UserMixin, db.Model):
    """Modelo base para todos os usuários da plataforma"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    senha_hash = db.Column(db.String(256), nullable=False)
    tipo_usuario = db.Column(db.String(20), nullable=False)  # 'trabalhador', 'cliente', 'lojista', 'admin'
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    perfil_trabalhador = db.relationship('PerfilTrabalhador', backref='usuario', uselist=False, cascade='all, delete-orphan')
    perfil_cliente = db.relationship('PerfilCliente', backref='usuario', uselist=False, cascade='all, delete-orphan')
    perfil_lojista = db.relationship('PerfilLojista', backref='usuario', uselist=False, cascade='all, delete-orphan')
    perfil_administrador = db.relationship('PerfilAdministrador', backref='usuario', uselist=False, cascade='all, delete-orphan')
    
    def definir_senha(self, senha):
        """Criptografa e armazena a senha do usuário"""
        self.senha_hash = generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        """Verifica se a senha fornecida é correta"""
        return check_password_hash(self.senha_hash, senha)
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'

class PerfilTrabalhador(db.Model):
    """Perfil específico para trabalhadores da construção civil"""
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    experiencia_anos = db.Column(db.Integer)
    descricao = db.Column(db.Text)
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    avaliacao_media = db.Column(db.Float, default=0.0)
    total_avaliacoes = db.Column(db.Integer, default=0)
    
    # Relacionamentos
    servicos = db.relationship('Servico', backref='trabalhador', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<PerfilTrabalhador {self.usuario.nome} - {self.especialidade}>'

class PerfilCliente(db.Model):
    """Perfil específico para clientes"""
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    endereco = db.Column(db.String(200))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    cep = db.Column(db.String(10))
    
    # Relacionamentos
    solicitacoes = db.relationship('SolicitacaoServico', backref='cliente', lazy=True)
    
    def __repr__(self):
        return f'<PerfilCliente {self.usuario.nome}>'

class PerfilLojista(db.Model):
    """Perfil específico para lojistas/fornecedores"""
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    nome_loja = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    cep = db.Column(db.String(10))
    horario_funcionamento = db.Column(db.String(100))
    
    # Relacionamentos
    materiais = db.relationship('Material', backref='lojista', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<PerfilLojista {self.nome_loja}>'

class Servico(db.Model):
    """Serviços oferecidos pelos trabalhadores"""
    id = db.Column(db.Integer, primary_key=True)
    trabalhador_id = db.Column(db.Integer, db.ForeignKey('perfil_trabalhador.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # elétrica, encanamento, alvenaria, etc.
    preco_minimo = db.Column(db.Float)
    preco_maximo = db.Column(db.Float)
    tipo_preco = db.Column(db.String(20), default='negociavel')  # fixo, por_hora, negociavel
    disponivel = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    solicitacoes = db.relationship('SolicitacaoServico', backref='servico', lazy=True)
    
    def __repr__(self):
        return f'<Servico {self.titulo}>'

class Material(db.Model):
    """Materiais oferecidos pelos lojistas"""
    id = db.Column(db.Integer, primary_key=True)
    lojista_id = db.Column(db.Integer, db.ForeignKey('perfil_lojista.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(50), nullable=False)  # cimento, tijolo, tinta, etc.
    preco = db.Column(db.Float)
    unidade = db.Column(db.String(20))  # kg, m², unidade, etc.
    disponivel = db.Column(db.Boolean, default=True)
    estoque = db.Column(db.Integer)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Material {self.nome}>'

class SolicitacaoServico(db.Model):
    """Solicitações de serviço feitas pelos clientes"""
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('perfil_cliente.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id'), nullable=False)
    mensagem = db.Column(db.Text)
    status = db.Column(db.String(20), default='pendente')  # pendente, aceito, recusado, concluido
    data_solicitacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_resposta = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<SolicitacaoServico {self.id}>'

class PerfilAdministrador(db.Model):
    """Perfil específico para administradores do sistema"""
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    nivel_acesso = db.Column(db.String(20), default='admin')  # admin, super_admin
    departamento = db.Column(db.String(100))
    permissoes_especiais = db.Column(db.Text)  # JSON com permissões específicas
    data_ultimo_acesso = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<PerfilAdministrador {self.usuario.nome}>'
