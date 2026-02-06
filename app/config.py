# -*- coding: utf-8 -*-
"""
========================================
NetRouter AI - Configurações do Sistema
========================================
Centralizamos todas as configurações aqui.

Por que usar uma classe de configuração?
- Organiza todas as settings em um só lugar
- Facilita trocar entre ambientes (dev/prod)
- O Flask carrega automaticamente com from_object()

Dica de segurança:
- NUNCA coloque senhas ou API keys direto aqui
- Use variáveis de ambiente (arquivo .env)
========================================
"""

import os


class Config:
    """
    Classe de configuração principal da aplicação.
    
    Todas as configurações que o Flask precisa ficam aqui.
    Valores sensíveis são puxados das variáveis de ambiente.
    
    Atributos:
    ----------
    SECRET_KEY : str
        Chave secreta usada pelo Flask para sessões e cookies
        IMPORTANTE: mude isso em produção!
    
    GOOGLE_API_KEY : str
        Chave da API do Google Gemini para usar a IA
    
    DEBUG : bool
        Se True, mostra erros detalhados (usar só em dev)
    
    FABRICANTES_SUPORTADOS : dict
        Lista de fabricantes e suas versões suportadas
        Isso centraliza a info usada em várias partes do sistema
    """
    
    # ========================================
    # Configurações do Flask
    # ========================================
    
    # Chave secreta - usada para assinar cookies e sessões
    # os.getenv() tenta pegar do ambiente, se não achar usa o valor padrão
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'chave-temporaria-mude-em-producao')
    
    # Modo debug - NUNCA deixe True em produção!
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # ========================================
    # Configurações da API Google Gemini
    # ========================================
    
    # Chave da API do Google - OBRIGATÓRIA para o sistema funcionar
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    
    # Modelo do Gemini a ser usado
    # O formato deve ser 'models/gemini-2.0-flash' para a nova API
    GEMINI_MODEL = 'models/gemini-2.0-flash'
    
    # ========================================
    # Fabricantes e Versões Suportadas
    # ========================================
    # Aqui definimos todos os roteadores que o sistema suporta
    # Isso é usado no dropdown do dashboard e na geração de scripts
    
    FABRICANTES_SUPORTADOS = {
        'cisco': {
            'nome': 'Cisco',
            'icone': '🔵',
            'versoes': {
                'ios-15': {
                    'nome': 'IOS 15.x',
                    'descricao': 'Roteadores clássicos (ISR G1/G2)',
                    'cli_prompt': 'Router#'
                },
                'ios-xe-16': {
                    'nome': 'IOS-XE 16.x',
                    'descricao': 'Catalyst 9000, ISR 4000',
                    'cli_prompt': 'Router#'
                },
                'ios-xe-17': {
                    'nome': 'IOS-XE 17.x',
                    'descricao': 'Versão mais recente IOS-XE',
                    'cli_prompt': 'Router#'
                },
                'ios-xr-7': {
                    'nome': 'IOS-XR 7.x',
                    'descricao': 'ASR 9000, NCS Series',
                    'cli_prompt': 'RP/0/RSP0/CPU0:Router#'
                },
                'nx-os-9': {
                    'nome': 'NX-OS 9.x',
                    'descricao': 'Nexus Data Center',
                    'cli_prompt': 'switch#'
                }
            }
        },
        'nokia': {
            'nome': 'Nokia',
            'icone': '🟠',
            'versoes': {
                'sros-19': {
                    'nome': 'SR OS 19.x',
                    'descricao': '7750 SR, 7950 XRS',
                    'cli_prompt': 'A:router#'
                },
                'sros-20': {
                    'nome': 'SR OS 20.x',
                    'descricao': '7750 SR, 7950 XRS',
                    'cli_prompt': 'A:router#'
                },
                'sros-21': {
                    'nome': 'SR OS 21.x',
                    'descricao': '7750 SR, 7950 XRS',
                    'cli_prompt': 'A:router#'
                },
                'sros-22': {
                    'nome': 'SR OS 22.x',
                    'descricao': '7750 SR, 7950 XRS',
                    'cli_prompt': 'A:router#'
                },
                'sros-23': {
                    'nome': 'SR OS 23.x',
                    'descricao': 'Versão mais recente',
                    'cli_prompt': 'A:router#'
                }
            }
        },
        'fortigate': {
            'nome': 'FortiGate',
            'icone': '🔴',
            'versoes': {
                'fortios-62': {
                    'nome': 'FortiOS 6.2',
                    'descricao': 'FortiGate 60-3000 Series',
                    'cli_prompt': 'FortiGate #'
                },
                'fortios-64': {
                    'nome': 'FortiOS 6.4',
                    'descricao': 'FortiGate 60-3000 Series',
                    'cli_prompt': 'FortiGate #'
                },
                'fortios-70': {
                    'nome': 'FortiOS 7.0',
                    'descricao': 'FortiGate Next-Gen',
                    'cli_prompt': 'FortiGate #'
                },
                'fortios-72': {
                    'nome': 'FortiOS 7.2',
                    'descricao': 'FortiGate Next-Gen',
                    'cli_prompt': 'FortiGate #'
                },
                'fortios-74': {
                    'nome': 'FortiOS 7.4',
                    'descricao': 'Versão mais recente',
                    'cli_prompt': 'FortiGate #'
                }
            }
        },
        'huawei': {
            'nome': 'Huawei',
            'icone': '🟢',
            'versoes': {
                'vrp-5': {
                    'nome': 'VRP 5.x',
                    'descricao': 'NE Series (Legacy)',
                    'cli_prompt': '<Huawei>'
                },
                'vrp-8': {
                    'nome': 'VRP 8.x',
                    'descricao': 'NE40E, NE8000',
                    'cli_prompt': '<Huawei>'
                },
                'vrp-ar': {
                    'nome': 'VRP 8.x (AR Series)',
                    'descricao': 'AR1200, AR2200, AR3200',
                    'cli_prompt': '<Huawei>'
                },
                'ce-6': {
                    'nome': 'CloudEngine 6.x',
                    'descricao': 'CE12800, CE8800, CE6800',
                    'cli_prompt': '<HUAWEI>'
                },
                'usg-6': {
                    'nome': 'USG 6.x',
                    'descricao': 'USG6000 Series Firewall',
                    'cli_prompt': '<USG>'
                }
            }
        }
    }
    
    # ========================================
    # Configurações de Troubleshooting
    # ========================================
    
    # Categorias de problemas comuns para o diagnóstico
    CATEGORIAS_PROBLEMAS = [
        'conectividade',      # Problemas de ping, traceroute
        'roteamento',         # BGP, OSPF, rotas estáticas
        'interface',          # Interfaces down, erros, CRC
        'performance',        # CPU alta, memória, buffers
        'seguranca',          # ACLs, firewall, autenticação
        'configuracao'        # Erros de config, restore
    ]
