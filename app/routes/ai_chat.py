# -*- coding: utf-8 -*-
"""
========================================
NetRouter AI - Rotas do Chat com IA
========================================
Endpoints para o chat interativo com IA.
========================================
"""

from flask import Blueprint, request, jsonify
from app.core import AIEngine

ai_chat_bp = Blueprint('ai_chat', __name__)

# Instância global da engine de IA
_ai_engine = None


def get_ai_engine():
    """Retorna instância singleton da AI Engine."""
    global _ai_engine
    if _ai_engine is None:
        _ai_engine = AIEngine()
    return _ai_engine


@ai_chat_bp.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint do chat com IA.
    
    Espera JSON com:
        - mensagem: texto do usuário
    
    Retorna:
        - sucesso: bool
        - resposta: resposta da IA
    """
    dados = request.get_json()
    
    if not dados or 'mensagem' not in dados:
        return jsonify({'sucesso': False, 'erro': 'Mensagem não informada'}), 400
    
    ai_engine = get_ai_engine()
    resultado = ai_engine.chat_livre(dados['mensagem'])
    
    return jsonify(resultado)


@ai_chat_bp.route('/limpar', methods=['POST'])
def limpar_historico():
    """Limpa o histórico de conversa."""
    ai_engine = get_ai_engine()
    ai_engine.limpar_historico()
    return jsonify({'sucesso': True, 'mensagem': 'Histórico limpo!'})


@ai_chat_bp.route('/historico', methods=['GET'])
def obter_historico():
    """Retorna o histórico da conversa atual."""
    ai_engine = get_ai_engine()
    historico = ai_engine.obter_historico()
    return jsonify({'sucesso': True, 'historico': historico})
