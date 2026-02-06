/**
 * ========================================
 * NetRouter AI - JavaScript do Dashboard
 * ========================================
 * 
 * Scripts para funcionalidades interativas:
 * - Chat flutuante com IA
 * - Animações e efeitos
 * - Funções utilitárias
 * 
 * Por que JavaScript vanilla?
 * - Mais leve que frameworks
 * - Fácil de manter
 * - Funciona sem dependências extras
 * ========================================
 */

// ========================================
// CHAT FLUTUANTE
// ========================================

/**
 * Alterna a visibilidade do chat flutuante.
 * Chamado quando clica no botão do chat.
 */
function toggleChat() {
    const container = document.getElementById('chatContainer');
    const toggle = document.querySelector('.chat-toggle');
    
    // Alterna a classe 'active' para mostrar/esconder
    container.classList.toggle('active');
    
    // Se abriu o chat, foca no input
    if (container.classList.contains('active')) {
        document.getElementById('chatInput').focus();
        toggle.style.display = 'none';
    } else {
        toggle.style.display = 'flex';
    }
}

/**
 * Envia mensagem no chat flutuante.
 * Chama a API de IA e mostra a resposta.
 */
function enviarMensagem() {
    const input = document.getElementById('chatInput');
    const mensagem = input.value.trim();
    
    // Não envia mensagem vazia
    if (!mensagem) return;
    
    // Adiciona a mensagem do usuário na tela
    adicionarMensagemChat('user', mensagem);
    
    // Limpa o input
    input.value = '';
    
    // Mostra indicador de "digitando..."
    adicionarMensagemChat('assistant', '<em class="typing">Pensando...</em>');
    
    // Chama a API do chat
    fetch('/ai/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mensagem: mensagem })
    })
    .then(response => response.json())
    .then(data => {
        // Remove o indicador de "digitando"
        const mensagens = document.getElementById('chatMessages');
        mensagens.removeChild(mensagens.lastChild);
        
        if (data.sucesso) {
            // Mostra a resposta da IA
            adicionarMensagemChat('assistant', data.resposta);
        } else {
            // Mostra erro
            adicionarMensagemChat('assistant', '❌ ' + data.erro);
        }
    })
    .catch(error => {
        // Remove indicador e mostra erro
        const mensagens = document.getElementById('chatMessages');
        mensagens.removeChild(mensagens.lastChild);
        adicionarMensagemChat('assistant', '❌ Erro de conexão com o servidor.');
        console.error('Erro no chat:', error);
    });
}

/**
 * Adiciona uma mensagem na área de mensagens do chat.
 * 
 * @param {string} role - 'user' ou 'assistant'
 * @param {string} conteudo - Conteúdo HTML da mensagem
 */
function adicionarMensagemChat(role, conteudo) {
    const container = document.getElementById('chatMessages');
    
    // Cria o elemento da mensagem
    const div = document.createElement('div');
    div.className = 'message ' + role;
    
    // Formata o conteúdo (converte markdown básico)
    let html = conteudo
        .replace(/```(\w*)\n?([\s\S]*?)```/g, '<pre>$2</pre>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>');
    
    div.innerHTML = '<p>' + html + '</p>';
    
    // Adiciona ao container
    container.appendChild(div);
    
    // Scroll automático para a última mensagem
    container.scrollTop = container.scrollHeight;
}

// ========================================
// ANIMAÇÕES E EFEITOS
// ========================================

/**
 * Inicializa animações quando a página carrega.
 */
document.addEventListener('DOMContentLoaded', function() {
    // Animação de fade-in nos cards
    animarCardsEntrada();
    
    // Inicializa tooltips se houver
    inicializarTooltips();
});

/**
 * Anima os cards com fade-in gradual.
 */
function animarCardsEntrada() {
    const cards = document.querySelectorAll('.stat-card, .vendor-card, .card');
    
    cards.forEach((card, index) => {
        // Define delay baseado na posição
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.4s ease';
        
        // Anima com delay escalonado
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

/**
 * Inicializa tooltips customizados.
 * (Preparado para uso futuro)
 */
function inicializarTooltips() {
    const elementos = document.querySelectorAll('[data-tooltip]');
    
    elementos.forEach(el => {
        el.addEventListener('mouseenter', mostrarTooltip);
        el.addEventListener('mouseleave', esconderTooltip);
    });
}

function mostrarTooltip(event) {
    const texto = event.target.dataset.tooltip;
    if (!texto) return;
    
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = texto;
    document.body.appendChild(tooltip);
    
    // Posiciona próximo ao elemento
    const rect = event.target.getBoundingClientRect();
    tooltip.style.top = (rect.top - 35) + 'px';
    tooltip.style.left = (rect.left + rect.width / 2) + 'px';
}

function esconderTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) tooltip.remove();
}

// ========================================
// FUNÇÕES UTILITÁRIAS
// ========================================

/**
 * Formata data para exibição.
 * 
 * @param {string} dataISO - Data em formato ISO
 * @returns {string} Data formatada
 */
function formatarData(dataISO) {
    const data = new Date(dataISO);
    return data.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Debounce - evita execução repetida de funções.
 * Útil para buscas e inputs com delay.
 * 
 * @param {Function} func - Função a ser executada
 * @param {number} wait - Tempo de espera em ms
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Mostra notificação toast.
 * 
 * @param {string} mensagem - Texto da notificação
 * @param {string} tipo - 'success', 'error', 'info'
 */
function mostrarNotificacao(mensagem, tipo = 'info') {
    // Remove notificação anterior se existir
    const existente = document.querySelector('.toast-notification');
    if (existente) existente.remove();
    
    // Cria elemento da notificação
    const toast = document.createElement('div');
    toast.className = 'toast-notification toast-' + tipo;
    
    // Define ícone baseado no tipo
    const icones = {
        success: '✅',
        error: '❌',
        info: 'ℹ️'
    };
    
    toast.innerHTML = `<span>${icones[tipo] || ''}</span> ${mensagem}`;
    
    // Adiciona ao body
    document.body.appendChild(toast);
    
    // Anima entrada
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Remove após 4 segundos
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

/**
 * Copia texto para a área de transferência.
 * 
 * @param {string} texto - Texto a copiar
 */
function copiarParaClipboard(texto) {
    navigator.clipboard.writeText(texto).then(() => {
        mostrarNotificacao('Copiado para a área de transferência!', 'success');
    }).catch(err => {
        console.error('Erro ao copiar:', err);
        mostrarNotificacao('Erro ao copiar', 'error');
    });
}

// ========================================
// ESTILOS DINÂMICOS PARA TOAST
// ========================================

// Adiciona estilos do toast se não existirem
(function() {
    const style = document.createElement('style');
    style.textContent = `
        .toast-notification {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 15px 25px;
            border-radius: 10px;
            color: var(--text-primary);
            font-size: 0.95rem;
            z-index: 9999;
            opacity: 0;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .toast-notification.show {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
        
        .toast-success { border-left: 3px solid var(--accent-green); }
        .toast-error { border-left: 3px solid var(--accent-red); }
        .toast-info { border-left: 3px solid var(--accent-blue); }
        
        .tooltip {
            position: fixed;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.8rem;
            color: var(--text-secondary);
            z-index: 9999;
            transform: translateX(-50%);
        }
    `;
    document.head.appendChild(style);
})();

// Log para confirmar que o script carregou
console.log('🚀 NetRouter AI - Dashboard carregado!');
