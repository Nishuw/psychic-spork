# -*- coding: utf-8 -*-
"""
========================================
Psychic Spork - Troubleshooter de Rede
========================================
Classe central de troubleshooting do sistema.
Combina base de conhecimento local com IA.

ATUALIZADO: Agora salva estatísticas em arquivo JSON
para persistir dados entre reinicializações.
========================================
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from app.core.ai_engine import AIEngine
from app.config import Config

# Caminho para arquivo de persistência
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'estatisticas.json')


class NetworkTroubleshooter:
    """
    Classe principal de troubleshooting de rede.
    Orquestra diagnósticos combinando base local + IA.
    
    Agora persiste estatísticas em JSON para manter
    dados reais entre reinicializações do servidor.
    """
    
    def __init__(self):
        """Inicializa o troubleshooter e carrega dados salvos."""
        self.ai_engine = AIEngine()
        self.historico_diagnosticos: List[Dict] = []
        self.scripts_gerados: int = 0
        self.consultas_ia: int = 0
        self.problemas_comuns = self._carregar_problemas_comuns()
        
        # Carrega dados persistidos
        self._carregar_dados()
        print("🔧 NetworkTroubleshooter inicializado!")
    
    def _carregar_dados(self):
        """Carrega dados salvos do arquivo JSON."""
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.historico_diagnosticos = dados.get('historico', [])
                    self.scripts_gerados = dados.get('scripts_gerados', 0)
                    self.consultas_ia = dados.get('consultas_ia', 0)
                    print(f"📊 Dados carregados: {len(self.historico_diagnosticos)} diagnósticos")
        except Exception as e:
            print(f"⚠️ Erro ao carregar dados: {e}")
    
    def _salvar_dados(self):
        """Salva dados no arquivo JSON."""
        try:
            # Cria diretório se não existir
            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
            
            dados = {
                'historico': self.historico_diagnosticos[-100:],  # Mantém últimos 100
                'scripts_gerados': self.scripts_gerados,
                'consultas_ia': self.consultas_ia,
                'atualizado_em': datetime.now().isoformat()
            }
            
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Erro ao salvar dados: {e}")
    
    def _carregar_problemas_comuns(self) -> Dict:
        """Carrega base de conhecimento com problemas frequentes."""
        return {
            "conectividade": {
                "ping_falha": {
                    "sintomas": ["ping falha", "sem resposta", "request timed out", "destination unreachable"],
                    "causas": ["Interface destino down", "Rota faltando", "ACL bloqueando", "Firewall", "ICMP desabilitado"],
                    "comandos_diagnostico": {
                        "cisco": ["show ip interface brief", "show ip route", "traceroute", "show ip arp"],
                        "nokia": ["show router interface", "show router route-table", "traceroute"],
                        "fortigate": ["get system interface", "execute traceroute", "get router info routing-table all"],
                        "huawei": ["display interface brief", "display ip routing-table", "tracert"]
                    },
                    "solucoes": ["Verificar interface", "Checar rotas", "Revisar ACLs", "Confirmar conectividade física"]
                },
                "interface_down": {
                    "sintomas": ["interface down", "link down", "no carrier", "line protocol down"],
                    "causas": ["Cabo desconectado", "Speed/duplex mismatch", "SFP com defeito", "Interface shutdown"],
                    "comandos_diagnostico": {
                        "cisco": ["show interface", "show controllers", "show cdp neighbors"],
                        "nokia": ["show port", "show port optical", "show port ethernet"],
                        "fortigate": ["get system interface physical", "diagnose hardware deviceinfo nic"],
                        "huawei": ["display interface", "display transceiver", "display eth-trunk"]
                    },
                    "solucoes": ["Verificar cabos", "Remover shutdown", "Testar SFP", "Ajustar speed/duplex"]
                },
                "pacotes_perdidos": {
                    "sintomas": ["packet loss", "perda de pacotes", "timeout intermitente"],
                    "causas": ["Buffer overflow", "QoS mal configurado", "Erros de CRC", "Congestionamento"],
                    "comandos_diagnostico": {
                        "cisco": ["show interface | inc errors|drops", "show buffers", "show queueing"],
                        "nokia": ["show port statistics", "show router buffer-pool"],
                        "fortigate": ["diagnose netlink device list", "diagnose sys session stat"],
                        "huawei": ["display interface | inc Error|Drop", "display qos statistics"]
                    },
                    "solucoes": ["Verificar erros na interface", "Revisar QoS", "Aumentar buffers"]
                }
            },
            "roteamento": {
                "bgp_down": {
                    "sintomas": ["bgp down", "neighbor down", "idle state", "bgp não estabelece"],
                    "causas": ["AS incorreto", "IP errado", "MD5 mismatch", "ACL porta 179", "TTL multihop"],
                    "comandos_diagnostico": {
                        "cisco": ["show bgp summary", "show bgp neighbor", "show tcp brief | inc 179"],
                        "nokia": ["show router bgp summary", "show router bgp neighbor", "show router bgp group"],
                        "fortigate": ["get router info bgp summary", "get router info bgp neighbor"],
                        "huawei": ["display bgp peer", "display bgp routing-table"]
                    },
                    "solucoes": ["Verificar AS e IP", "Checar senha MD5", "Verificar rota para peer", "Checar ACLs"]
                },
                "ospf_adjacency": {
                    "sintomas": ["ospf neighbor", "adjacency", "2way", "exstart", "ospf stuck"],
                    "causas": ["Hello/Dead diferentes", "Área diferente", "MTU mismatch", "Tipo de rede errado"],
                    "comandos_diagnostico": {
                        "cisco": ["show ip ospf neighbor", "show ip ospf interface", "debug ip ospf adj"],
                        "nokia": ["show router ospf neighbor", "show router ospf interface detail"],
                        "fortigate": ["get router info ospf neighbor", "get router info ospf interface"],
                        "huawei": ["display ospf peer", "display ospf interface"]
                    },
                    "solucoes": ["Checar área", "Verificar timers", "Conferir MTU", "Validar tipo de rede"]
                },
                "rotas_faltando": {
                    "sintomas": ["rota não aparece", "missing route", "no route", "rota sumiu"],
                    "causas": ["AD maior", "Filtro de rotas", "Route-map", "Peer não anunciando"],
                    "comandos_diagnostico": {
                        "cisco": ["show ip route", "show ip bgp", "show route-map"],
                        "nokia": ["show router route-table", "show router policy"],
                        "fortigate": ["get router info routing-table all", "get router info bgp network"],
                        "huawei": ["display ip routing-table", "display route-policy"]
                    },
                    "solucoes": ["Verificar AD", "Checar route-maps", "Validar anúncio do peer"]
                }
            },
            "performance": {
                "cpu_alta": {
                    "sintomas": ["cpu alta", "high cpu", "lento", "cpu 100", "processos travados"],
                    "causas": ["Processo travado", "DDoS", "Log excessivo", "Bug", "Roteamento instável"],
                    "comandos_diagnostico": {
                        "cisco": ["show processes cpu sorted", "show processes cpu history"],
                        "nokia": ["show system cpu", "show system memory"],
                        "fortigate": ["diagnose sys top", "diagnose hardware sysinfo shm"],
                        "huawei": ["display cpu-usage", "display cpu-usage history"]
                    },
                    "solucoes": ["Identificar processo", "Verificar ataque", "Reduzir logs", "Atualizar firmware"]
                },
                "memoria_alta": {
                    "sintomas": ["memoria alta", "high memory", "memory exhausted", "out of memory"],
                    "causas": ["Vazamento de memória", "Muitas rotas", "Sessões acumuladas", "Bug"],
                    "comandos_diagnostico": {
                        "cisco": ["show memory summary", "show processes memory sorted"],
                        "nokia": ["show system memory", "show router route-table summary"],
                        "fortigate": ["diagnose hardware sysinfo shm", "diagnose sys session stat"],
                        "huawei": ["display memory", "display ip routing-table statistics"]
                    },
                    "solucoes": ["Identificar consumo", "Limpar sessões", "Reduzir tabela de rotas", "Reiniciar processo"]
                }
            },
            "seguranca": {
                "acl_bloqueio": {
                    "sintomas": ["acl deny", "bloqueado", "blocked", "filtrado", "access denied"],
                    "causas": ["ACL restritiva", "Ordem errada", "Implicit deny", "ACL na direção errada"],
                    "comandos_diagnostico": {
                        "cisco": ["show access-lists", "show ip access-lists interface"],
                        "nokia": ["show filter ip", "show filter ip ipv4-filter"],
                        "fortigate": ["get firewall policy", "diagnose debug flow"],
                        "huawei": ["display acl all", "display traffic-filter applied-record"]
                    },
                    "solucoes": ["Revisar regras", "Adicionar logging", "Checar direção", "Reordenar regras"]
                },
                "vpn_down": {
                    "sintomas": ["vpn down", "ipsec down", "tunnel down", "phase1 failed", "phase2 failed"],
                    "causas": ["PSK errada", "Proposta não match", "NAT-T issues", "Firewall bloqueando"],
                    "comandos_diagnostico": {
                        "cisco": ["show crypto isakmp sa", "show crypto ipsec sa"],
                        "nokia": ["show router tunnel-table", "show ipsec tunnel"],
                        "fortigate": ["get vpn ipsec tunnel summary", "diagnose vpn ike gateway"],
                        "huawei": ["display ike sa", "display ipsec sa"]
                    },
                    "solucoes": ["Verificar PSK", "Alinhar propostas", "Checar portas UDP 500/4500"]
                }
            }
        }
    
    def diagnosticar(self, problema: str, fabricante: str = "", versao: str = "",
                     categoria: str = "", logs: str = "", usar_ia: bool = True) -> Dict:
        """
        Realiza diagnóstico completo de um problema.
        Tenta base local primeiro, depois IA se necessário.
        """
        inicio = datetime.now()
        match_local = self._buscar_local(problema, categoria, fabricante)
        
        if match_local:
            resultado = {"sucesso": True, "fonte": "local", "diagnostico": match_local, "erro": ""}
        elif usar_ia:
            resposta_ia = self.ai_engine.analisar_problema(problema, fabricante, versao, logs)
            if resposta_ia["sucesso"]:
                resultado = {"sucesso": True, "fonte": "ia", 
                           "diagnostico": {"analise_ia": resposta_ia["analise"]}, "erro": ""}
                self.consultas_ia += 1
            else:
                resultado = {"sucesso": False, "fonte": "", "diagnostico": {}, "erro": resposta_ia["erro"]}
        else:
            resultado = {"sucesso": False, "fonte": "", "diagnostico": {}, 
                        "erro": "Problema não encontrado na base local."}
        
        # Salva no histórico
        self.historico_diagnosticos.append({
            "timestamp": inicio.isoformat(), 
            "problema": problema, 
            "fabricante": fabricante or "generico",
            "versao": versao, 
            "categoria": categoria, 
            "fonte": resultado.get("fonte", ""),
            "sucesso": resultado["sucesso"]
        })
        
        # Persiste dados
        self._salvar_dados()
        
        return resultado
    
    def _buscar_local(self, problema: str, categoria: str, fabricante: str) -> Optional[Dict]:
        """Busca na base de conhecimento local por palavras-chave."""
        problema_lower = problema.lower()
        categorias = [categoria] if categoria in self.problemas_comuns else list(self.problemas_comuns.keys())
        
        for cat in categorias:
            for nome_prob, dados in self.problemas_comuns[cat].items():
                for sintoma in dados["sintomas"]:
                    if sintoma.lower() in problema_lower:
                        resultado = {
                            "categoria": cat, 
                            "problema_identificado": nome_prob,
                            "causas": dados["causas"], 
                            "solucoes": dados["solucoes"]
                        }
                        if fabricante in dados["comandos_diagnostico"]:
                            resultado["comandos"] = dados["comandos_diagnostico"][fabricante]
                        elif dados["comandos_diagnostico"]:
                            resultado["comandos"] = list(dados["comandos_diagnostico"].values())[0]
                        return resultado
        return None
    
    def registrar_script_gerado(self):
        """Registra que um script foi gerado."""
        self.scripts_gerados += 1
        self._salvar_dados()
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas dos diagnósticos realizados."""
        total = len(self.historico_diagnosticos)
        
        if total == 0:
            return {
                "total": 0, 
                "sucesso": 0, 
                "taxa_sucesso": 0, 
                "scripts_gerados": self.scripts_gerados,
                "consultas_ia": self.consultas_ia,
                "por_fabricante": {},
                "por_categoria": {}
            }
        
        sucesso = sum(1 for d in self.historico_diagnosticos if d.get("sucesso", False))
        
        # Estatísticas por fabricante
        por_fab = {}
        for d in self.historico_diagnosticos:
            fab = d.get("fabricante", "generico") or "generico"
            por_fab[fab] = por_fab.get(fab, 0) + 1
        
        # Estatísticas por categoria
        por_cat = {}
        for d in self.historico_diagnosticos:
            cat = d.get("categoria", "outros") or "outros"
            por_cat[cat] = por_cat.get(cat, 0) + 1
        
        return {
            "total": total, 
            "sucesso": sucesso, 
            "taxa_sucesso": round((sucesso/total)*100, 1) if total > 0 else 0,
            "scripts_gerados": self.scripts_gerados,
            "consultas_ia": self.consultas_ia,
            "por_fabricante": por_fab,
            "por_categoria": por_cat
        }
    
    def listar_categorias(self) -> List[str]:
        """Retorna categorias de problemas disponíveis."""
        return list(self.problemas_comuns.keys())
