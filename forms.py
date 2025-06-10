from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, IntegerField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, EqualTo, ValidationError
from models import Usuario

class FormularioLogin(FlaskForm):
    """Formulário de login"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar = BooleanField('Lembrar de mim')

class FormularioRegistro(FlaskForm):
    """Formulário de registro de usuário"""
    nome = StringField('Nome Completo', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[Optional(), Length(max=20)])
    tipo_usuario = SelectField('Tipo de Usuário', 
                              choices=[('trabalhador', 'Trabalhador'), 
                                     ('cliente', 'Cliente'), 
                                     ('lojista', 'Lojista'),
                                     ('admin', 'Administrador')],
                              validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Senha', 
                                   validators=[DataRequired(), 
                                             EqualTo('senha', message='As senhas devem ser iguais')])
    
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este email já está cadastrado. Use outro email.')

class FormularioPerfilTrabalhador(FlaskForm):
    """Formulário para perfil do trabalhador"""
    especialidade = SelectField('Especialidade', 
                               choices=[('eletrica', 'Elétrica'),
                                      ('encanamento', 'Encanamento'),
                                      ('alvenaria', 'Alvenaria'),
                                      ('pintura', 'Pintura'),
                                      ('carpintaria', 'Carpintaria'),
                                      ('serralheria', 'Serralheria'),
                                      ('gesso', 'Gesso e Drywall'),
                                      ('ceramica', 'Cerâmica e Azulejo'),
                                      ('telhado', 'Telhado e Cobertura'),
                                      ('jardinagem', 'Jardinagem'),
                                      ('limpeza', 'Limpeza Pós-Obra'),
                                      ('outros', 'Outros')],
                               validators=[DataRequired()])
    experiencia_anos = IntegerField('Anos de Experiência', validators=[Optional(), NumberRange(min=0, max=50)])
    descricao = TextAreaField('Descrição dos Serviços', validators=[Optional(), Length(max=500)])
    cidade = StringField('Cidade', validators=[Optional(), Length(max=100)])
    estado = SelectField('Estado',
                        choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
                               ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
                               ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
                               ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
                               ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
                               ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
                               ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
                               ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
                               ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
                               ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')],
                        validators=[Optional()])

class FormularioServico(FlaskForm):
    """Formulário para criar/editar serviços"""
    titulo = StringField('Título do Serviço', validators=[DataRequired(), Length(min=5, max=100)])
    descricao = TextAreaField('Descrição Detalhada', validators=[DataRequired(), Length(min=20, max=1000)])
    categoria = SelectField('Categoria',
                           choices=[('eletrica', 'Elétrica'),
                                  ('encanamento', 'Encanamento'),
                                  ('alvenaria', 'Alvenaria'),
                                  ('pintura', 'Pintura'),
                                  ('carpintaria', 'Carpintaria'),
                                  ('serralheria', 'Serralheria'),
                                  ('gesso', 'Gesso e Drywall'),
                                  ('ceramica', 'Cerâmica e Azulejo'),
                                  ('telhado', 'Telhado e Cobertura'),
                                  ('jardinagem', 'Jardinagem'),
                                  ('limpeza', 'Limpeza Pós-Obra'),
                                  ('outros', 'Outros')],
                           validators=[DataRequired()])
    tipo_preco = SelectField('Tipo de Preço',
                            choices=[('fixo', 'Preço Fixo'),
                                   ('por_hora', 'Por Hora'),
                                   ('negociavel', 'Negociável')],
                            validators=[DataRequired()])
    preco_minimo = FloatField('Preço Mínimo (R$)', validators=[Optional(), NumberRange(min=0)])
    preco_maximo = FloatField('Preço Máximo (R$)', validators=[Optional(), NumberRange(min=0)])

class FormularioPerfilCliente(FlaskForm):
    """Formulário para perfil do cliente"""
    endereco = StringField('Endereço', validators=[Optional(), Length(max=200)])
    cidade = StringField('Cidade', validators=[Optional(), Length(max=100)])
    estado = SelectField('Estado',
                        choices=[('', 'Selecione...'), ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
                               ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
                               ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
                               ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
                               ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
                               ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
                               ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
                               ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
                               ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
                               ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')],
                        validators=[Optional()])
    cep = StringField('CEP', validators=[Optional(), Length(max=10)])

class FormularioPerfilLojista(FlaskForm):
    """Formulário para perfil do lojista"""
    nome_loja = StringField('Nome da Loja', validators=[DataRequired(), Length(min=2, max=100)])
    cnpj = StringField('CNPJ', validators=[Optional(), Length(max=20)])
    endereco = StringField('Endereço', validators=[Optional(), Length(max=200)])
    cidade = StringField('Cidade', validators=[Optional(), Length(max=100)])
    estado = SelectField('Estado',
                        choices=[('', 'Selecione...'), ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
                               ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
                               ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
                               ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
                               ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
                               ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
                               ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
                               ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
                               ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
                               ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')],
                        validators=[Optional()])
    cep = StringField('CEP', validators=[Optional(), Length(max=10)])
    horario_funcionamento = StringField('Horário de Funcionamento', validators=[Optional(), Length(max=100)])

class FormularioMaterial(FlaskForm):
    """Formulário para criar/editar materiais"""
    nome = StringField('Nome do Material', validators=[DataRequired(), Length(min=2, max=100)])
    descricao = TextAreaField('Descrição', validators=[Optional(), Length(max=500)])
    categoria = SelectField('Categoria',
                           choices=[('cimento', 'Cimento e Argamassa'),
                                  ('tijolo', 'Tijolos e Blocos'),
                                  ('tinta', 'Tintas e Vernizes'),
                                  ('madeira', 'Madeira'),
                                  ('eletrico', 'Material Elétrico'),
                                  ('hidraulico', 'Material Hidráulico'),
                                  ('ceramica', 'Cerâmica e Azulejo'),
                                  ('ferro', 'Ferro e Aço'),
                                  ('ferramenta', 'Ferramentas'),
                                  ('outros', 'Outros')],
                           validators=[DataRequired()])
    preco = FloatField('Preço (R$)', validators=[Optional(), NumberRange(min=0)])
    unidade = SelectField('Unidade',
                         choices=[('unidade', 'Unidade'),
                                ('kg', 'Quilograma'),
                                ('m', 'Metro'),
                                ('m2', 'Metro Quadrado'),
                                ('m3', 'Metro Cúbico'),
                                ('litro', 'Litro'),
                                ('pacote', 'Pacote'),
                                ('caixa', 'Caixa')],
                         validators=[Optional()])
    estoque = IntegerField('Quantidade em Estoque', validators=[Optional(), NumberRange(min=0)])

class FormularioSolicitacao(FlaskForm):
    """Formulário para solicitar serviço"""
    mensagem = TextAreaField('Mensagem', validators=[DataRequired(), Length(min=10, max=500)])

class FormularioPerfilAdministrador(FlaskForm):
    """Formulário para perfil do administrador"""
    nivel_acesso = SelectField('Nível de Acesso',
                              choices=[('admin', 'Administrador'),
                                     ('super_admin', 'Super Administrador')],
                              validators=[DataRequired()])
    departamento = StringField('Departamento', validators=[Optional(), Length(max=100)])
    
class FormularioUsuarioAdmin(FlaskForm):
    """Formulário para gerenciamento de usuários pelo admin"""
    nome = StringField('Nome Completo', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[Optional(), Length(max=20)])
    tipo_usuario = SelectField('Tipo de Usuário', 
                              choices=[('trabalhador', 'Trabalhador'), 
                                     ('cliente', 'Cliente'), 
                                     ('lojista', 'Lojista'),
                                     ('admin', 'Administrador')],
                              validators=[DataRequired()])
    ativo = BooleanField('Usuário Ativo')
