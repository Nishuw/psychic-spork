# -*- coding: utf-8 -*-
"""
Pacote core - Núcleo do sistema NetRouter AI
Este pacote contém a lógica principal do sistema.
"""

# Importamos as classes principais para facilitar o uso
# Assim, quem importar o pacote pode fazer:
# from app.core import AIEngine, NetworkTroubleshooter, ScriptGenerator
from app.core.ai_engine import AIEngine
from app.core.troubleshooter import NetworkTroubleshooter
from app.core.script_generator import ScriptGenerator

# Lista do que é exportado quando alguém faz "from app.core import *"
__all__ = ['AIEngine', 'NetworkTroubleshooter', 'ScriptGenerator']
