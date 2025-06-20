from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db
from models import Usuario, PerfilTrabalhador, PerfilCliente, PerfilLojista, PerfilAdministrador, Servico, Material, SolicitacaoServico
from forms import (FormularioLogin, FormularioRegistro, FormularioPerfilTrabalhador, 
                   FormularioServico, FormularioPerfilCliente, FormularioPerfilLojista,
                   FormularioMaterial, FormularioSolicitacao)

# Blueprint principal
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Página inicial da plataforma"""
    # Buscar alguns serviços em destaque
    servicos_destaque = Servico.query.filter_by(disponivel=True).limit(6).all()
    
    # Contar estatísticas
    total_trabalhadores = PerfilTrabalhador.query.count()
    total_servicos = Servico.query.filter_by(disponivel=True).count()
    total_lojistas = PerfilLojista.query.count()
    
    return render_template('index.html', 
                         servicos_destaque=servicos_destaque,
                         total_trabalhadores=total_trabalhadores,
                         total_servicos=total_servicos,
                         total_lojistas=total_lojistas)

# Blueprint de autenticação
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = FormularioLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.verificar_senha(form.senha.data):
            login_user(usuario, remember=form.lembrar.data)
            flash('Login realizado com sucesso!', 'success')
            
            # Redirecionar baseado no tipo de usuário
            if usuario.tipo_usuario == 'trabalhador':
                return redirect(url_for('trabalhador.perfil'))
            elif usuario.tipo_usuario == 'cliente':
                return redirect(url_for('cliente.dashboard'))
            elif usuario.tipo_usuario == 'lojista':
                return redirect(url_for('lojista.dashboard'))
            elif usuario.tipo_usuario == 'admin':
                return redirect(url_for('admin.dashboard'))
        else:
            flash('Email ou senha incorretos.', 'error')
    
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = FormularioRegistro()
    if form.validate_on_submit():
        # Verificar se email já existe
        if Usuario.query.filter_by(email=form.email.data).first():
            flash('Este email já está cadastrado.', 'error')
            return render_template('auth/register.html', form=form)
        
        # Criar novo usuário
        usuario = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            telefone=form.telefone.data,
            tipo_usuario=form.tipo_usuario.data
        )
        usuario.definir_senha(form.senha.data)
        
        db.session.add(usuario)
        db.session.commit()
        
        # Criar perfil específico baseado no tipo
        if usuario.tipo_usuario == 'trabalhador':
            perfil = PerfilTrabalhador(usuario_id=usuario.id, especialidade='outros')
            db.session.add(perfil)
        elif usuario.tipo_usuario == 'cliente':
            perfil = PerfilCliente(usuario_id=usuario.id)
            db.session.add(perfil)
        elif usuario.tipo_usuario == 'lojista':
            perfil = PerfilLojista(usuario_id=usuario.id, nome_loja=f'Loja de {usuario.nome}')
            db.session.add(perfil)
        elif usuario.tipo_usuario == 'admin':
            perfil = PerfilAdministrador(usuario_id=usuario.id, nivel_acesso='admin')
            db.session.add(perfil)
        
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('main.index'))

# Blueprint do trabalhador
trabalhador = Blueprint('trabalhador', __name__)

@trabalhador.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    """Perfil do trabalhador"""
    if current_user.tipo_usuario != 'trabalhador':
        abort(403)
    
    perfil_trab = current_user.perfil_trabalhador
    if not perfil_trab:
        abort(404)
    
    form = FormularioPerfilTrabalhador()
    if form.validate_on_submit():
        perfil_trab.especialidade = form.especialidade.data
        perfil_trab.experiencia_anos = form.experiencia_anos.data
        perfil_trab.descricao = form.descricao.data
        perfil_trab.cidade = form.cidade.data
        perfil_trab.estado = form.estado.data
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('trabalhador.perfil'))
    
    # Pré-preencher o formulário
    form.especialidade.data = perfil_trab.especialidade
    form.experiencia_anos.data = perfil_trab.experiencia_anos
    form.descricao.data = perfil_trab.descricao
    form.cidade.data = perfil_trab.cidade
    form.estado.data = perfil_trab.estado
    
    return render_template('trabalhador/perfil.html', form=form, perfil=perfil_trab)

@trabalhador.route('/servicos')
@login_required
def listar_servicos():
    """Lista serviços do trabalhador"""
    if current_user.tipo_usuario != 'trabalhador':
        abort(403)
    
    perfil_trab = current_user.perfil_trabalhador
    servicos = perfil_trab.servicos if perfil_trab else []
    
    return render_template('trabalhador/listar_servicos.html', servicos=servicos)

@trabalhador.route('/servicos/criar', methods=['GET', 'POST'])
@login_required
def criar_servico():
    """Criar novo serviço"""
    if current_user.tipo_usuario != 'trabalhador':
        abort(403)
    
    form = FormularioServico()
    if form.validate_on_submit():
        servico = Servico(
            trabalhador_id=current_user.perfil_trabalhador.id,
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            categoria=form.categoria.data,
            tipo_preco=form.tipo_preco.data,
            preco_minimo=form.preco_minimo.data,
            preco_maximo=form.preco_maximo.data
        )
        
        db.session.add(servico)
        db.session.commit()
        
        flash('Serviço criado com sucesso!', 'success')
        return redirect(url_for('trabalhador.listar_servicos'))
    
    return render_template('trabalhador/criar_servico.html', form=form)

@trabalhador.route('/solicitacoes')
@login_required
def listar_solicitacoes():
    """Lista solicitações recebidas pelo trabalhador"""
    if current_user.tipo_usuario != 'trabalhador':
        abort(403)
    
    perfil_trab = current_user.perfil_trabalhador
    if not perfil_trab:
        abort(404)
    
    # Buscar todas as solicitações para os serviços do trabalhador
    from datetime import datetime
    solicitacoes = db.session.query(SolicitacaoServico).join(Servico).filter(
        Servico.trabalhador_id == perfil_trab.id
    ).order_by(SolicitacaoServico.data_solicitacao.desc()).all()
    
    return render_template('trabalhador/solicitacoes.html', solicitacoes=solicitacoes)

@trabalhador.route('/solicitacao/<int:solicitacao_id>/aceitar', methods=['POST'])
@login_required
def aceitar_solicitacao(solicitacao_id):
    """Aceitar uma solicitação de serviço"""
    if current_user.tipo_usuario != 'trabalhador':
        abort(403)
    
    # Verificar se a solicitação pertence ao trabalhador
    solicitacao = db.session.query(SolicitacaoServico).join(Servico).filter(
        SolicitacaoServico.id == solicitacao_id,
        Servico.trabalhador_id == current_user.perfil_trabalhador.id
    ).first()
    
    if not solicitacao:
        abort(404)
    
    if solicitacao.status != 'pendente':
        flash('Esta solicitação já foi respondida.', 'warning')
        return redirect(url_for('trabalhador.listar_solicitacoes'))
    
    # Aceitar a solicitação
    solicitacao.status = 'aceito'
    solicitacao.data_resposta = datetime.utcnow()
    db.session.commit()
    
    flash(f'Solicitação de {solicitacao.cliente.usuario.nome} foi aceita!', 'success')
    return redirect(url_for('trabalhador.listar_solicitacoes'))

@trabalhador.route('/solicitacao/<int:solicitacao_id>/recusar', methods=['POST'])
@login_required
def recusar_solicitacao(solicitacao_id):
    """Recusar uma solicitação de serviço"""
    if current_user.tipo_usuario != 'trabalhador':
        abort(403)
    
    # Verificar se a solicitação pertence ao trabalhador
    solicitacao = db.session.query(SolicitacaoServico).join(Servico).filter(
        SolicitacaoServico.id == solicitacao_id,
        Servico.trabalhador_id == current_user.perfil_trabalhador.id
    ).first()
    
    if not solicitacao:
        abort(404)
    
    if solicitacao.status != 'pendente':
        flash('Esta solicitação já foi respondida.', 'warning')
        return redirect(url_for('trabalhador.listar_solicitacoes'))
    
    # Recusar a solicitação
    solicitacao.status = 'recusado'
    solicitacao.data_resposta = datetime.utcnow()
    db.session.commit()
    
    flash(f'Solicitação de {solicitacao.cliente.usuario.nome} foi recusada.', 'info')
    return redirect(url_for('trabalhador.listar_solicitacoes'))

@trabalhador.route('/solicitacao/<int:solicitacao_id>/concluir', methods=['POST'])
@login_required
def concluir_solicitacao(solicitacao_id):
    """Marcar uma solicitação como concluída"""
    if current_user.tipo_usuario != 'trabalhador':
        abort(403)
    
    # Verificar se a solicitação pertence ao trabalhador
    solicitacao = db.session.query(SolicitacaoServico).join(Servico).filter(
        SolicitacaoServico.id == solicitacao_id,
        Servico.trabalhador_id == current_user.perfil_trabalhador.id
    ).first()
    
    if not solicitacao:
        abort(404)
    
    if solicitacao.status != 'aceito':
        flash('Apenas solicitações aceitas podem ser marcadas como concluídas.', 'warning')
        return redirect(url_for('trabalhador.listar_solicitacoes'))
    
    # Marcar como concluída
    solicitacao.status = 'concluido'
    db.session.commit()
    
    flash(f'Serviço para {solicitacao.cliente.usuario.nome} foi marcado como concluído!', 'success')
    return redirect(url_for('trabalhador.listar_solicitacoes'))

# Blueprint do cliente
cliente = Blueprint('cliente', __name__)

@cliente.route('/dashboard')
@login_required
def dashboard():
    """Dashboard do cliente"""
    if current_user.tipo_usuario != 'cliente':
        abort(403)
    
    # Buscar solicitações do cliente
    solicitacoes = SolicitacaoServico.query.filter_by(cliente_id=current_user.perfil_cliente.id).order_by(SolicitacaoServico.data_solicitacao.desc()).all()
    
    return render_template('cliente/dashboard.html', solicitacoes=solicitacoes)

@cliente.route('/buscar-servicos')
@login_required
def buscar_servicos():
    """Buscar serviços disponíveis"""
    if current_user.tipo_usuario != 'cliente':
        abort(403)
    
    categoria = request.args.get('categoria', '')
    cidade = request.args.get('cidade', '')
    
    query = Servico.query.filter_by(disponivel=True)
    
    if categoria:
        query = query.filter_by(categoria=categoria)
    
    if cidade:
        query = query.join(PerfilTrabalhador).filter(PerfilTrabalhador.cidade.ilike(f'%{cidade}%'))
    
    servicos = query.all()
    
    return render_template('cliente/buscar_servicos.html', servicos=servicos, categoria=categoria, cidade=cidade)

@cliente.route('/solicitar-servico/<int:servico_id>', methods=['GET', 'POST'])
@login_required
def solicitar_servico(servico_id):
    """Solicitar um serviço"""
    if current_user.tipo_usuario != 'cliente':
        abort(403)
    
    servico = Servico.query.get_or_404(servico_id)
    form = FormularioSolicitacao()
    
    if form.validate_on_submit():
        solicitacao = SolicitacaoServico(
            cliente_id=current_user.perfil_cliente.id,
            servico_id=servico.id,
            mensagem=form.mensagem.data
        )
        
        db.session.add(solicitacao)
        db.session.commit()
        
        flash('Solicitação enviada com sucesso!', 'success')
        return redirect(url_for('cliente.dashboard'))
    
    return render_template('cliente/solicitar_servico.html', form=form, servico=servico)

# Blueprint do lojista
lojista = Blueprint('lojista', __name__)

@lojista.route('/dashboard')
@login_required
def dashboard():
    """Dashboard do lojista"""
    if current_user.tipo_usuario != 'lojista':
        abort(403)
    
    perfil_loj = current_user.perfil_lojista
    total_materiais = len(perfil_loj.materiais) if perfil_loj else 0
    
    return render_template('lojista/dashboard.html', perfil=perfil_loj, total_materiais=total_materiais)

@lojista.route('/materiais')
@login_required
def listar_materiais():
    """Lista materiais do lojista"""
    if current_user.tipo_usuario != 'lojista':
        abort(403)
    
    perfil_loj = current_user.perfil_lojista
    materiais = perfil_loj.materiais if perfil_loj else []
    
    return render_template('lojista/listar_materiais.html', materiais=materiais)

@lojista.route('/materiais/criar', methods=['GET', 'POST'])
@login_required
def criar_material():
    """Criar novo material"""
    if current_user.tipo_usuario != 'lojista':
        abort(403)
    
    form = FormularioMaterial()
    if form.validate_on_submit():
        material = Material(
            lojista_id=current_user.perfil_lojista.id,
            nome=form.nome.data,
            descricao=form.descricao.data,
            categoria=form.categoria.data,
            preco=form.preco.data,
            unidade=form.unidade.data,
            estoque=form.estoque.data
        )
        
        db.session.add(material)
        db.session.commit()
        
        flash('Material adicionado com sucesso!', 'success')
        return redirect(url_for('lojista.listar_materiais'))
    
    return render_template('lojista/criar_material.html', form=form)

# Blueprint do administrador
admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
@login_required
def dashboard():
    """Dashboard do administrador"""
    if current_user.tipo_usuario != 'admin':
        abort(403)
    
    # Estatísticas gerais do sistema
    total_usuarios = Usuario.query.count()
    total_trabalhadores = PerfilTrabalhador.query.count()
    total_clientes = PerfilCliente.query.count()
    total_lojistas = PerfilLojista.query.count()
    total_admins = PerfilAdministrador.query.count()
    total_servicos = Servico.query.count()
    total_materiais = Material.query.count()
    total_solicitacoes = SolicitacaoServico.query.count()
    
    # Usuários mais recentes
    usuarios_recentes = Usuario.query.order_by(Usuario.data_criacao.desc()).limit(10).all()
    
    # Solicitações pendentes
    solicitacoes_pendentes = SolicitacaoServico.query.filter_by(status='pendente').count()
    
    return render_template('admin/dashboard.html',
                         total_usuarios=total_usuarios,
                         total_trabalhadores=total_trabalhadores,
                         total_clientes=total_clientes,
                         total_lojistas=total_lojistas,
                         total_admins=total_admins,
                         total_servicos=total_servicos,
                         total_materiais=total_materiais,
                         total_solicitacoes=total_solicitacoes,
                         usuarios_recentes=usuarios_recentes,
                         solicitacoes_pendentes=solicitacoes_pendentes)

@admin.route('/usuarios')
@login_required
def listar_usuarios():
    """Lista todos os usuários do sistema"""
    if current_user.tipo_usuario != 'admin':
        abort(403)
    
    tipo_filtro = request.args.get('tipo', '')
    busca = request.args.get('busca', '')
    
    query = Usuario.query
    
    if tipo_filtro:
        query = query.filter_by(tipo_usuario=tipo_filtro)
    
    if busca:
        query = query.filter(
            Usuario.nome.ilike(f'%{busca}%') | 
            Usuario.email.ilike(f'%{busca}%')
        )
    
    usuarios = query.order_by(Usuario.data_criacao.desc()).all()
    
    return render_template('admin/listar_usuarios.html', 
                         usuarios=usuarios,
                         tipo_filtro=tipo_filtro,
                         busca=busca)

@admin.route('/usuarios/<int:usuario_id>/toggle')
@login_required
def toggle_usuario_ativo(usuario_id):
    """Ativar/desativar usuário"""
    if current_user.tipo_usuario != 'admin':
        abort(403)
    
    usuario = Usuario.query.get_or_404(usuario_id)
    
    # Não permitir desativar próprio usuário ou outros admins
    if usuario.id == current_user.id or usuario.tipo_usuario == 'admin':
        flash('Não é possível alterar o status deste usuário.', 'error')
        return redirect(url_for('admin.listar_usuarios'))
    
    usuario.ativo = not usuario.ativo
    db.session.commit()
    
    status = 'ativado' if usuario.ativo else 'desativado'
    flash(f'Usuário {usuario.nome} foi {status} com sucesso!', 'success')
    
    return redirect(url_for('admin.listar_usuarios'))

@admin.route('/servicos')
@login_required
def listar_servicos():
    """Lista todos os serviços do sistema"""
    if current_user.tipo_usuario != 'admin':
        abort(403)
    
    categoria = request.args.get('categoria', '')
    
    query = Servico.query
    
    if categoria:
        query = query.filter_by(categoria=categoria)
    
    servicos = query.order_by(Servico.data_criacao.desc()).all()
    
    return render_template('admin/listar_servicos.html', 
                         servicos=servicos,
                         categoria=categoria)

@admin.route('/materiais')
@login_required
def listar_materiais():
    """Lista todos os materiais do sistema"""
    if current_user.tipo_usuario != 'admin':
        abort(403)
    
    categoria = request.args.get('categoria', '')
    
    query = Material.query
    
    if categoria:
        query = query.filter_by(categoria=categoria)
    
    materiais = query.order_by(Material.data_criacao.desc()).all()
    
    return render_template('admin/listar_materiais.html', 
                         materiais=materiais,
                         categoria=categoria)

@admin.route('/solicitacoes')
@login_required
def listar_solicitacoes():
    """Lista todas as solicitações do sistema"""
    if current_user.tipo_usuario != 'admin':
        abort(403)
    
    status_filtro = request.args.get('status', '')
    
    query = SolicitacaoServico.query
    
    if status_filtro:
        query = query.filter_by(status=status_filtro)
    
    solicitacoes = query.order_by(SolicitacaoServico.data_solicitacao.desc()).all()
    
    return render_template('admin/listar_solicitacoes.html', 
                         solicitacoes=solicitacoes,
                         status_filtro=status_filtro)

@admin.route('/relatorios')
@login_required
def relatorios():
    """Página de relatórios e estatísticas"""
    if current_user.tipo_usuario != 'admin':
        abort(403)
    
    from datetime import datetime, timedelta
    from sqlalchemy import func
    
    # Estatísticas dos últimos 30 dias
    data_limite = datetime.utcnow() - timedelta(days=30)
    
    # Novos usuários por mês
    usuarios_por_mes = db.session.query(
        func.date_trunc('month', Usuario.data_criacao).label('mes'),
        func.count(Usuario.id).label('total')
    ).filter(Usuario.data_criacao >= data_limite).group_by('mes').all()
    
    # Serviços por categoria
    servicos_por_categoria = db.session.query(
        Servico.categoria,
        func.count(Servico.id).label('total')
    ).group_by(Servico.categoria).all()
    
    # Materiais por categoria
    materiais_por_categoria = db.session.query(
        Material.categoria,
        func.count(Material.id).label('total')
    ).group_by(Material.categoria).all()
    
    # Status das solicitações
    solicitacoes_por_status = db.session.query(
        SolicitacaoServico.status,
        func.count(SolicitacaoServico.id).label('total')
    ).group_by(SolicitacaoServico.status).all()
    
    return render_template('admin/relatorios.html',
                         usuarios_por_mes=usuarios_por_mes,
                         servicos_por_categoria=servicos_por_categoria,
                         materiais_por_categoria=materiais_por_categoria,
                         solicitacoes_por_status=solicitacoes_por_status)
