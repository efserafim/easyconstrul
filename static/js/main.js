// EasyConstrul - JavaScript Principal

document.addEventListener('DOMContentLoaded', function() {
    console.log('EasyConstrul carregado com sucesso!');
    
    // Inicializar componentes
    initializeTooltips();
    initializeAlerts();
    initializeFormValidation();
    initializeSearchFilters();
    initializeMasks();
    
    // Adicionar animações
    addScrollAnimations();
});

/**
 * Inicializar tooltips do Bootstrap
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Auto-dismiss para alertas
 */
function initializeAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        // Auto-dismiss após 5 segundos para alertas de sucesso
        if (alert.classList.contains('alert-success')) {
            setTimeout(() => {
                const closeButton = alert.querySelector('.btn-close');
                if (closeButton) {
                    closeButton.click();
                }
            }, 5000);
        }
    });
}

/**
 * Validação de formulários customizada
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[novalidate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Focar no primeiro campo inválido
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
            
            form.classList.add('was-validated');
        });
        
        // Validação em tempo real
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(input);
            });
            
            input.addEventListener('input', function() {
                if (input.classList.contains('is-invalid')) {
                    validateField(input);
                }
            });
        });
    });
}

/**
 * Validar campo individual
 */
function validateField(field) {
    const isValid = field.checkValidity();
    
    field.classList.remove('is-valid', 'is-invalid');
    field.classList.add(isValid ? 'is-valid' : 'is-invalid');
    
    // Mensagens customizadas
    const feedback = field.parentNode.querySelector('.invalid-feedback');
    if (!isValid && !feedback) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = getCustomErrorMessage(field);
        field.parentNode.appendChild(errorDiv);
    }
}

/**
 * Mensagens de erro customizadas
 */
function getCustomErrorMessage(field) {
    if (field.validity.valueMissing) {
        return `${field.labels[0]?.textContent || 'Este campo'} é obrigatório.`;
    }
    if (field.validity.typeMismatch) {
        if (field.type === 'email') {
            return 'Por favor, insira um email válido.';
        }
        if (field.type === 'url') {
            return 'Por favor, insira uma URL válida.';
        }
    }
    if (field.validity.tooShort) {
        return `Este campo deve ter pelo menos ${field.minLength} caracteres.`;
    }
    if (field.validity.tooLong) {
        return `Este campo não pode ter mais de ${field.maxLength} caracteres.`;
    }
    if (field.validity.rangeUnderflow) {
        return `O valor deve ser maior ou igual a ${field.min}.`;
    }
    if (field.validity.rangeOverflow) {
        return `O valor deve ser menor ou igual a ${field.max}.`;
    }
    if (field.validity.patternMismatch) {
        return 'Por favor, use o formato correto.';
    }
    
    return 'Por favor, verifique este campo.';
}

/**
 * Filtros de busca dinâmicos
 */
function initializeSearchFilters() {
    const searchForm = document.querySelector('#searchForm');
    if (searchForm) {
        const inputs = searchForm.querySelectorAll('input, select');
        
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                // Destacar filtros aplicados
                const filterContainer = input.closest('.form-group, .mb-3, .col-md-6, .col-md-4');
                if (filterContainer) {
                    if (input.value) {
                        filterContainer.classList.add('filter-applied');
                    } else {
                        filterContainer.classList.remove('filter-applied');
                    }
                }
            });
        });
    }
}

/**
 * Máscaras para campos de entrada
 */
function initializeMasks() {
    // Máscara para telefone
    const phoneInputs = document.querySelectorAll('input[name="telefone"], input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length <= 11) {
                if (value.length <= 10) {
                    value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
                } else {
                    value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
                }
            }
            
            e.target.value = value;
        });
    });
    
    // Máscara para CEP
    const cepInputs = document.querySelectorAll('input[name="cep"]');
    cepInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{5})(\d{3})/, '$1-$2');
            e.target.value = value;
        });
    });
    
    // Máscara para CNPJ
    const cnpjInputs = document.querySelectorAll('input[name="cnpj"]');
    cnpjInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
            e.target.value = value;
        });
    });
}

/**
 * Animações ao scroll
 */
function addScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observar cards e seções
    const elementsToAnimate = document.querySelectorAll('.card, .alert, .hero-section');
    elementsToAnimate.forEach(el => {
        observer.observe(el);
    });
}

/**
 * Utilitários para feedback visual
 */
function showLoading(element) {
    if (element) {
        element.classList.add('loading');
        const spinner = document.createElement('span');
        spinner.className = 'spinner me-2';
        element.prepend(spinner);
    }
}

function hideLoading(element) {
    if (element) {
        element.classList.remove('loading');
        const spinner = element.querySelector('.spinner');
        if (spinner) {
            spinner.remove();
        }
    }
}

/**
 * Função para confirmar ações
 */
function confirmAction(message, callback) {
    if (confirm(message || 'Tem certeza que deseja realizar esta ação?')) {
        if (typeof callback === 'function') {
            callback();
        }
    }
}

/**
 * Função para mostrar notificações toast
 */
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remover do DOM após ocultação
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    container.style.zIndex = '1080';
    document.body.appendChild(container);
    return container;
}

/**
 * Função para scroll suave para elementos
 */
function scrollToElement(selector, offset = 80) {
    const element = document.querySelector(selector);
    if (element) {
        const elementPosition = element.offsetTop - offset;
        window.scrollTo({
            top: elementPosition,
            behavior: 'smooth'
        });
    }
}

/**
 * Debounce para otimizar eventos
 */
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

/**
 * Função para formatação de moeda
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

/**
 * Função para formatação de data
 */
function formatDate(date, options = {}) {
    const defaultOptions = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    
    return new Intl.DateTimeFormat('pt-BR', { ...defaultOptions, ...options }).format(new Date(date));
}

// Exportar funções globais úteis
window.EC = {
    showLoading,
    hideLoading,
    confirmAction,
    showToast,
    scrollToElement,
    formatCurrency,
    formatDate,
    debounce
};

// Console log personalizado para desenvolvimento
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log('%c🏗️ EasyConstrul', 'color: #2c5aa0; font-size: 20px; font-weight: bold;');
    console.log('%cPlataforma de Construção Civil carregada com sucesso!', 'color: #27ae60; font-size: 12px;');
}
