# -*- coding: utf-8 -*-
"""
========================================
NetRouter AI - API REST
========================================
Endpoints da API para comunicação AJAX.

Estas rotas retornam JSON e são chamadas pelo
JavaScript do frontend para operações dinâmicas.
========================================
"""

from flask import Blueprint, request, jsonify
from app.core import NetworkTroubleshooter, ScriptGenerator
from app.config import Config

# Blueprint para rotas da API
api_bp = Blueprint('api', __name__)

# Instâncias globais (singleton pattern)
# Evita criar novas instâncias a cada requisição
_troubleshooter = None
_script_generator = None


def get_troubleshooter():
    """Retorna instância singleton do troubleshooter."""
    global _troubleshooter
    if _troubleshooter is None:
        _troubleshooter = NetworkTroubleshooter()
    return _troubleshooter


def get_script_generator():
    """Retorna instância singleton do gerador de scripts."""
    global _script_generator
    if _script_generator is None:
        _script_generator = ScriptGenerator()
    return _script_generator


@api_bp.route('/fabricantes', methods=['GET'])
def listar_fabricantes():
    """
    Lista todos os fabricantes suportados.
    
    Retorna:
        JSON com lista de fabricantes e suas versões
    """
    fabricantes = []
    for fab_id, fab_info in Config.FABRICANTES_SUPORTADOS.items():
        versoes = []
        for ver_id, ver_info in fab_info['versoes'].items():
            versoes.append({
                'id': ver_id,
                'nome': ver_info['nome'],
                'descricao': ver_info['descricao']
            })
        fabricantes.append({
            'id': fab_id,
            'nome': fab_info['nome'],
            'icone': fab_info['icone'],
            'versoes': versoes
        })
    return jsonify({'sucesso': True, 'fabricantes': fabricantes})


@api_bp.route('/diagnosticar', methods=['POST'])
def diagnosticar():
    """
    Realiza diagnóstico de um problema.
    
    Espera JSON com:
        - problema: descrição do problema
        - fabricante: id do fabricante (opcional)
        - versao: id da versão (opcional)
        - categoria: categoria do problema (opcional)
        - logs: logs relevantes (opcional)
    """
    dados = request.get_json()
    
    if not dados or 'problema' not in dados:
        return jsonify({'sucesso': False, 'erro': 'Problema não informado'}), 400
    
    troubleshooter = get_troubleshooter()
    resultado = troubleshooter.diagnosticar(
        problema=dados.get('problema', ''),
        fabricante=dados.get('fabricante', ''),
        versao=dados.get('versao', ''),
        categoria=dados.get('categoria', ''),
        logs=dados.get('logs', '')
    )
    
    return jsonify(resultado)


@api_bp.route('/estatisticas', methods=['GET'])
def obter_estatisticas():
    """Retorna estatísticas de uso do sistema."""
    troubleshooter = get_troubleshooter()
    stats = troubleshooter.obter_estatisticas()
    return jsonify({'sucesso': True, 'estatisticas': stats})


@api_bp.route('/templates/<fabricante>', methods=['GET'])
def listar_templates(fabricante):
    """Lista templates disponíveis para um fabricante."""
    versao = request.args.get('versao', '')
    generator = get_script_generator()
    templates = generator.listar_templates(fabricante, versao)
    return jsonify({'sucesso': True, 'templates': templates})


@api_bp.route('/template/<fabricante>/<template_id>', methods=['GET'])
def obter_template(fabricante, template_id):
    """Retorna um template específico."""
    generator = get_script_generator()
    template = generator.obter_template(fabricante, template_id)
    if template:
        return jsonify({'sucesso': True, 'template': template})
    return jsonify({'sucesso': False, 'erro': 'Template não encontrado'}), 404


@api_bp.route('/gerar-script', methods=['POST'])
def gerar_script():
    """
    Gera script customizado via IA.
    
    Espera JSON com:
        - descricao: o que o script deve fazer
        - fabricante: id do fabricante
        - versao: id da versão
    """
    dados = request.get_json()
    
    if not dados or 'descricao' not in dados:
        return jsonify({'sucesso': False, 'erro': 'Descrição não informada'}), 400
    
    generator = get_script_generator()
    resultado = generator.gerar_script_ia(
        descricao=dados.get('descricao', ''),
        fabricante=dados.get('fabricante', ''),
        versao=dados.get('versao', '')
    )
    
    return jsonify(resultado)


@api_bp.route('/categorias', methods=['GET'])
def listar_categorias():
    """Lista categorias de problemas disponíveis."""
    return jsonify({
        'sucesso': True,
        'categorias': Config.CATEGORIAS_PROBLEMAS
    })
