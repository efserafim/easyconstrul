# EasyConstrul - Replit Project Documentation

## Project Overview
Platform Flask para conectar trabalhadores da construção civil, clientes e fornecedores de materiais. Sistema completo com 4 tipos de usuários: trabalhadores, clientes, lojistas e administradores.

## Recent Changes
- **2024-12-20**: PostgreSQL database added and configured
- **2024-12-20**: Project configured for universal server compatibility
- **2024-12-20**: Administrator functionality implemented with complete dashboard
- **2024-12-20**: Sistema completo implementado com todas as funcionalidades básicas

## Project Architecture

### Database
- **Primary**: PostgreSQL (Neon-backed) - configured via DATABASE_URL environment variable
- **Fallback**: SQLite for development environments
- **Models**: Usuario, PerfilTrabalhador, PerfilCliente, PerfilLojista, PerfilAdministrador, Servico, Material, SolicitacaoServico

### Application Structure
```
app.py - Main application configuration
main.py - Entry point for the application
models.py - Database models
routes.py - Application routes and blueprints
forms.py - WTForms for user input
config.py - Environment configurations
run.py - Standalone execution script
```

### User Types
1. **Trabalhador**: Creates and manages construction services
2. **Cliente**: Searches for and requests services
3. **Lojista**: Manages construction materials inventory
4. **Administrador**: System management and monitoring

### Features Implemented
- Complete authentication system with Flask-Login
- Role-based access control
- Service marketplace for workers
- Material catalog for suppliers
- Request system between clients and workers
- Administrative dashboard with statistics
- Responsive Bootstrap UI
- Form validation with WTForms

## Technical Decisions
- Flask framework chosen for simplicity and flexibility
- SQLAlchemy ORM for database abstraction
- Bootstrap for responsive design
- WTForms for secure form handling
- Werkzeug for password hashing

## User Preferences
- All code and interface in Portuguese
- System designed for Brazilian construction market
- Focus on simplicity and ease of use
- Professional, clean design aesthetic

## Deployment Configuration
- Configured to run on any server with minimal setup
- Environment variables with secure defaults
- Automatic database initialization
- Multiple execution methods (main.py, run.py, gunicorn)

## Current Status
✅ Fully functional platform with all core features
✅ PostgreSQL database configured and ready
✅ Universal server compatibility achieved
✅ Administrator panel fully implemented
✅ Complete user management system