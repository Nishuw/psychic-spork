# -*- coding: utf-8 -*-
"""
========================================
NetRouter AI - Rotas Principais
========================================
Rotas para as páginas do dashboard.

Aqui definimos as URLs que o usuário acessa no navegador.
Cada rota renderiza um template HTML diferente.
========================================
"""

from flask import Blueprint, render_template, request
from app.config import Config

# Cria um Blueprint - é como um "mini-app" dentro do Flask
# Isso ajuda a organizar as rotas em módulos separados
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    Página inicial - Dashboard principal.
    
    Mostra visão geral do sistema com:
    - Estatísticas de uso
    - Atividade recente
    - Links rápidos para funcionalidades
    """
    # Pega info dos fabricantes para mostrar cards
    fabricantes = Config.FABRICANTES_SUPORTADOS
    
    return render_template(
        'dashboard.html',
        fabricantes=fabricantes,
        titulo='Dashboard'
    )


@main_bp.route('/troubleshoot')
def troubleshoot():
    """
    Página de troubleshooting.
    
    Interface para o usuário descrever problemas
    e receber diagnóstico + soluções.
    """
    fabricantes = Config.FABRICANTES_SUPORTADOS
    categorias = Config.CATEGORIAS_PROBLEMAS
    
    return render_template(
        'troubleshoot.html',
        fabricantes=fabricantes,
        categorias=categorias,
        titulo='Troubleshooting'
    )


@main_bp.route('/scripts')
def scripts():
    """
    Página de geração de scripts.
    
    O usuário escolhe fabricante, versão e tipo de script.
    Pode usar templates prontos ou gerar via IA.
    """
    fabricantes = Config.FABRICANTES_SUPORTADOS
    
    return render_template(
        'scripts.html',
        fabricantes=fabricantes,
        titulo='Gerador de Scripts'
    )


@main_bp.route('/chat')
def chat():
    """
    Página de chat com IA.
    
    Conversa livre sobre temas de rede.
    Útil para dúvidas gerais e aprendizado.
    """
    return render_template(
        'chat.html',
        titulo='Chat com IA'
    )
