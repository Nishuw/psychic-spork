# -*- coding: utf-8 -*-
"""
========================================
NetRouter AI - Gerador de Scripts
========================================
Gera scripts de configuração para roteadores.

Este módulo tem templates prontos para operações comuns
e também pode gerar scripts customizados via IA.

Por que usar templates?
- Mais rápido que gerar via IA
- Sempre consistente e testado
- Funciona offline

Por que usar IA também?
- Para scripts complexos/customizados
- Para explicar comandos
- Para adaptar a situações específicas
========================================
"""

from typing import Dict, List, Optional
from app.core.ai_engine import AIEngine
from app.config import Config


class ScriptGenerator:
    """
    Gerador de scripts para roteadores.
    Combina templates pré-definidos com geração via IA.
    """
    
    def __init__(self):
        """Inicializa o gerador de scripts."""
        self.ai_engine = AIEngine()
        self.templates = self._carregar_templates()
        print("📝 ScriptGenerator inicializado!")
    
    def _carregar_templates(self) -> Dict:
        """
        Carrega templates de scripts por fabricante.
        Templates são scripts prontos para operações comuns.
        """
        return {
            # ========================================
            # Templates Cisco
            # ========================================
            "cisco": {
                "backup_config": {
                    "nome": "Backup de Configuração",
                    "descricao": "Salva a configuração atual",
                    "script": """! === Backup de Configuração Cisco ===
! Primeiro, mostra a config atual
show running-config

! Salva na memória flash (persistente)
copy running-config startup-config

! Para copiar para servidor TFTP:
! copy running-config tftp://<IP_SERVIDOR>/<NOME_ARQUIVO>.cfg
""",
                    "versoes": ["ios-15", "ios-xe-16", "ios-xe-17"]
                },
                "diagnostico_basico": {
                    "nome": "Diagnóstico Básico",
                    "descricao": "Comandos essenciais de diagnóstico",
                    "script": """! === Diagnóstico Básico Cisco ===
! Versão e uptime
show version | include uptime|Version

! Status das interfaces
show ip interface brief

! Uso de CPU e memória
show processes cpu sorted | head 10
show memory statistics

! Últimos logs
show logging | tail 20
""",
                    "versoes": ["ios-15", "ios-xe-16", "ios-xe-17", "ios-xr-7", "nx-os-9"]
                },
                "config_interface": {
                    "nome": "Configurar Interface",
                    "descricao": "Template para configurar interface",
                    "script": """! === Configuração de Interface Cisco ===
configure terminal

! Substitua os valores entre <>
interface <NOME_INTERFACE>
 description <DESCRICAO>
 ip address <IP> <MASCARA>
 no shutdown
 
! Saia e salve
end
write memory
""",
                    "versoes": ["ios-15", "ios-xe-16", "ios-xe-17"]
                },
                "config_ospf": {
                    "nome": "Configurar OSPF",
                    "descricao": "Configuração básica de OSPF",
                    "script": """! === Configuração OSPF Cisco ===
configure terminal

router ospf <PROCESS_ID>
 router-id <ROUTER_ID>
 network <REDE> <WILDCARD> area <AREA>
 passive-interface default
 no passive-interface <INTERFACE_ATIVA>

end
write memory

! Verificar adjacências
show ip ospf neighbor
""",
                    "versoes": ["ios-15", "ios-xe-16", "ios-xe-17"]
                },
                "config_bgp": {
                    "nome": "Configurar BGP",
                    "descricao": "Configuração básica de BGP",
                    "script": """! === Configuração BGP Cisco ===
configure terminal

router bgp <ASN_LOCAL>
 bgp router-id <ROUTER_ID>
 neighbor <IP_NEIGHBOR> remote-as <ASN_REMOTO>
 neighbor <IP_NEIGHBOR> description <DESCRICAO>
 
 ! Anunciar redes
 network <REDE> mask <MASCARA>

end
write memory

! Verificar sessão
show bgp summary
""",
                    "versoes": ["ios-15", "ios-xe-16", "ios-xe-17"]
                }
            },
            
            # ========================================
            # Templates Nokia
            # ========================================
            "nokia": {
                "backup_config": {
                    "nome": "Backup de Configuração",
                    "descricao": "Salva a configuração atual",
                    "script": """# === Backup de Configuração Nokia ===
# Mostra config atual
admin display-config

# Salva a configuração
admin save

# Para copiar para servidor:
# file copy cf3:/config.cfg ftp://<USER>@<IP>/<ARQUIVO>
""",
                    "versoes": ["sros-19", "sros-20", "sros-21", "sros-22", "sros-23"]
                },
                "diagnostico_basico": {
                    "nome": "Diagnóstico Básico",
                    "descricao": "Comandos essenciais de diagnóstico",
                    "script": """# === Diagnóstico Básico Nokia ===
# Versão e uptime
show version
show system information

# Status das portas
show port

# CPU e memória
show system cpu
show system memory-pools

# Logs recentes
show log log-id 99
""",
                    "versoes": ["sros-19", "sros-20", "sros-21", "sros-22", "sros-23"]
                },
                "config_interface": {
                    "nome": "Configurar Interface",
                    "descricao": "Template para configurar interface",
                    "script": """# === Configuração de Interface Nokia ===
configure router interface "<NOME>"
    address <IP>/<PREFIXO>
    port <PORTA>
    no shutdown
exit

# Verificar
show router interface
""",
                    "versoes": ["sros-19", "sros-20", "sros-21", "sros-22", "sros-23"]
                }
            },
            
            # ========================================
            # Templates FortiGate
            # ========================================
            "fortigate": {
                "backup_config": {
                    "nome": "Backup de Configuração",
                    "descricao": "Salva a configuração atual",
                    "script": """# === Backup de Configuração FortiGate ===
# Mostra config completa
show full-configuration

# Para backup via CLI para USB:
# execute backup config usb <NOME_ARQUIVO>

# Para backup via TFTP:
# execute backup config tftp <NOME_ARQUIVO> <IP_SERVIDOR>
""",
                    "versoes": ["fortios-62", "fortios-64", "fortios-70", "fortios-72", "fortios-74"]
                },
                "diagnostico_basico": {
                    "nome": "Diagnóstico Básico",
                    "descricao": "Comandos essenciais de diagnóstico",
                    "script": """# === Diagnóstico Básico FortiGate ===
# Versão do sistema
get system status

# Status das interfaces
get system interface physical

# Performance do sistema
get system performance status

# Sessões ativas
get system session status

# Logs de sistema
execute log display
""",
                    "versoes": ["fortios-62", "fortios-64", "fortios-70", "fortios-72", "fortios-74"]
                },
                "config_interface": {
                    "nome": "Configurar Interface",
                    "descricao": "Template para configurar interface",
                    "script": """# === Configuração de Interface FortiGate ===
config system interface
    edit "<NOME_INTERFACE>"
        set ip <IP> <MASCARA>
        set allowaccess ping https ssh
        set alias "<DESCRICAO>"
        set status up
    next
end

# Verificar
get system interface physical
""",
                    "versoes": ["fortios-62", "fortios-64", "fortios-70", "fortios-72", "fortios-74"]
                },
                "config_firewall_policy": {
                    "nome": "Criar Política de Firewall",
                    "descricao": "Template para política de firewall",
                    "script": """# === Política de Firewall FortiGate ===
config firewall policy
    edit 0
        set name "<NOME_REGRA>"
        set srcintf "<INTERFACE_ORIGEM>"
        set dstintf "<INTERFACE_DESTINO>"
        set srcaddr "all"
        set dstaddr "all"
        set action accept
        set schedule "always"
        set service "ALL"
        set logtraffic all
    next
end

# Verificar políticas
get firewall policy
""",
                    "versoes": ["fortios-62", "fortios-64", "fortios-70", "fortios-72", "fortios-74"]
                }
            },
            
            # ========================================
            # Templates Huawei
            # ========================================
            "huawei": {
                "backup_config": {
                    "nome": "Backup de Configuração",
                    "descricao": "Salva a configuração atual",
                    "script": """# === Backup de Configuração Huawei ===
# Mostra config atual
display current-configuration

# Salva configuração
save
# Confirme com 'Y'

# Para copiar para servidor TFTP:
# tftp <IP_SERVIDOR> put vrpcfg.zip
""",
                    "versoes": ["vrp-5", "vrp-8", "vrp-ar", "ce-6", "usg-6"]
                },
                "diagnostico_basico": {
                    "nome": "Diagnóstico Básico",
                    "descricao": "Comandos essenciais de diagnóstico",
                    "script": """# === Diagnóstico Básico Huawei ===
# Versão do sistema
display version

# Status das interfaces
display interface brief

# CPU e memória
display cpu-usage
display memory-usage

# Logs do sistema
display logbuffer
""",
                    "versoes": ["vrp-5", "vrp-8", "vrp-ar", "ce-6", "usg-6"]
                },
                "config_interface": {
                    "nome": "Configurar Interface",
                    "descricao": "Template para configurar interface",
                    "script": """# === Configuração de Interface Huawei ===
system-view

interface <NOME_INTERFACE>
 description <DESCRICAO>
 ip address <IP> <MASCARA>
 undo shutdown
 quit

# Salvar
save
# Confirme com 'Y'

# Verificar
display interface <NOME_INTERFACE>
""",
                    "versoes": ["vrp-5", "vrp-8", "vrp-ar", "ce-6", "usg-6"]
                },
                "config_ospf": {
                    "nome": "Configurar OSPF",
                    "descricao": "Configuração básica de OSPF",
                    "script": """# === Configuração OSPF Huawei ===
system-view

ospf <PROCESS_ID> router-id <ROUTER_ID>
 area <AREA>
  network <REDE> <WILDCARD>
 quit
quit

# Ativar OSPF na interface
interface <INTERFACE>
 ospf enable <PROCESS_ID> area <AREA>
 quit

save

# Verificar
display ospf peer
""",
                    "versoes": ["vrp-5", "vrp-8", "vrp-ar", "ce-6"]
                }
            }
        }
    
    def listar_templates(self, fabricante: str, versao: str = "") -> List[Dict]:
        """
        Lista templates disponíveis para um fabricante/versão.
        
        Retorna lista de templates com nome e descrição.
        """
        if fabricante not in self.templates:
            return []
        
        resultado = []
        for nome_template, dados in self.templates[fabricante].items():
            # Filtra por versão se especificada
            if versao and versao not in dados.get("versoes", []):
                continue
            resultado.append({
                "id": nome_template,
                "nome": dados["nome"],
                "descricao": dados["descricao"]
            })
        return resultado
    
    def obter_template(self, fabricante: str, template_id: str) -> Optional[Dict]:
        """
        Retorna um template específico.
        """
        if fabricante not in self.templates:
            return None
        if template_id not in self.templates[fabricante]:
            return None
        return self.templates[fabricante][template_id]
    
    def gerar_script_ia(self, descricao: str, fabricante: str, versao: str) -> Dict:
        """
        Gera script customizado usando IA.
        Usado quando não há template disponível.
        """
        return self.ai_engine.gerar_script_ia(descricao, fabricante, versao)
    
    def obter_fabricantes(self) -> List[Dict]:
        """Retorna lista de fabricantes suportados."""
        resultado = []
        for fab_id, fab_info in Config.FABRICANTES_SUPORTADOS.items():
            resultado.append({
                "id": fab_id,
                "nome": fab_info["nome"],
                "icone": fab_info["icone"],
                "versoes": list(fab_info["versoes"].keys())
            })
        return resultado
