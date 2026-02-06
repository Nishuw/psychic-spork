#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================
NetRouter AI - Script de Inicialização
========================================
Este é o ponto de entrada da aplicação.
Execute com: python run.py

O que esse arquivo faz:
1. Carrega as variáveis de ambiente do arquivo .env
2. Importa a aplicação Flask
3. Inicia o servidor web

Por que separar isso do __init__.py?
- Deixa o código mais organizado
- Facilita testes (posso importar o app sem iniciar o servidor)
- É uma boa prática em projetos Flask
========================================
"""

# Importa a biblioteca para carregar variáveis de ambiente
# Isso é importante para não expor dados sensíveis no código
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
# Precisa ser feito ANTES de importar o app
load_dotenv()

# Agora sim importa a aplicação Flask
# O app é criado no __init__.py do pacote app
from app import criar_app

# Cria a instância da aplicação
# A função criar_app() segue o padrão "Application Factory"
# Isso facilita testes e diferentes configurações
app = criar_app()

# Esse bloco só executa se rodarmos diretamente o run.py
# Se importarmos de outro lugar, não executa
if __name__ == '__main__':
    # Pega a porta das variáveis de ambiente ou usa 5000 como padrão
    porta = int(os.getenv('PORT', 5000))
    
    # Verifica se estamos em modo debug
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Mensagem amigável no console
    print("=" * 50)
    print("🚀 NetRouter AI - Sistema de Troubleshooting")
    print("=" * 50)
    print(f"📡 Servidor rodando em: http://localhost:{porta}")
    print(f"🔧 Modo Debug: {'Ativado' if debug else 'Desativado'}")
    print("=" * 50)
    print("Pressione CTRL+C para parar o servidor")
    print("=" * 50)
    
    # Inicia o servidor Flask
    # host='0.0.0.0' permite acesso de outras máquinas na rede
    app.run(
        host='0.0.0.0',
        port=porta,
        debug=debug
    )
