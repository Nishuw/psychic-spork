# -*- coding: utf-8 -*-
"""
========================================
NetRouter AI - Inicialização do App
========================================
Este arquivo configura e cria a aplicação Flask.

O que é o padrão Application Factory?
- É uma função que CRIA e RETORNA a aplicação
- Permite criar várias instâncias (útil para testes)
- Facilita configurações diferentes (dev, prod, test)

Por que usar esse padrão?
- Mais flexível que criar o app diretamente
- Evita problemas de importação circular
- É a forma recomendada pelo Flask
========================================
"""

# Importa o Flask - framework web que vamos usar
from flask import Flask

# Importa as configurações do sistema
from app.config import Config


def criar_app(config_class=Config):
    """
    Função factory que cria e configura a aplicação Flask.
    
    Parâmetros:
    -----------
    config_class : class
        Classe de configuração a ser usada (padrão: Config)
        Podemos passar outras configs para testes, por exemplo
    
    Retorna:
    --------
    Flask
        Instância da aplicação configurada e pronta para uso
    
    Exemplo de uso:
    ---------------
    >>> app = criar_app()
    >>> app.run()
    """
    
    # Cria a instância do Flask
    # __name__ ajuda o Flask a encontrar os arquivos do projeto
    app = Flask(__name__)
    
    # Carrega as configurações da classe Config
    # Isso aplica todas as settings (secret key, debug, etc)
    app.config.from_object(config_class)
    
    # ========================================
    # Registro de Blueprints (rotas)
    # ========================================
    # Blueprints são como "mini-aplicações" dentro do Flask
    # Ajudam a organizar o código em módulos separados
    
    # Importa e registra as rotas principais (páginas do dashboard)
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    # Importa e registra as rotas da API (endpoints JSON)
    from app.routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Importa e registra as rotas do chat com IA
    from app.routes.ai_chat import ai_chat_bp
    app.register_blueprint(ai_chat_bp, url_prefix='/ai')
    
    # Mensagem de log para confirmar que tudo foi carregado
    # Útil para debug
    print("✅ Aplicação NetRouter AI inicializada com sucesso!")
    
    # Retorna a aplicação pronta para uso
    return app
