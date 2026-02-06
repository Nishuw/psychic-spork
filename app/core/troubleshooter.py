# -*- coding: utf-8 -*-
"""
========================================
NetRouter AI - Troubleshooter de Rede
========================================
Classe central de troubleshooting do sistema.
Combina base de conhecimento local com IA.
========================================
"""

from typing import Dict, List, Optional
from datetime import datetime
from app.core.ai_engine import AIEngine
from app.config import Config


class NetworkTroubleshooter:
    """
    Classe principal de troubleshooting de rede.
    Orquestra diagnósticos combinando base local + IA.
    """
    
    def __init__(self):
        """Inicializa o troubleshooter."""
        self.ai_engine = AIEngine()
        self.historico_diagnosticos: List[Dict] = []
        self.problemas_comuns = self._carregar_problemas_comuns()
        print("🔧 NetworkTroubleshooter inicializado!")
    
    def _carregar_problemas_comuns(self) -> Dict:
        """Carrega base de conhecimento com problemas frequentes."""
        return {
            "conectividade": {
                "ping_falha": {
                    "sintomas": ["ping falha", "sem resposta", "request timed out"],
                    "causas": ["Interface destino down", "Rota faltando", "ACL bloqueando", "Firewall"],
                    "comandos_diagnostico": {
                        "cisco": ["show ip interface brief", "show ip route", "traceroute"],
                        "nokia": ["show router interface", "show router route-table"],
                        "fortigate": ["get system interface", "execute traceroute"],
                        "huawei": ["display interface brief", "display ip routing-table"]
                    },
                    "solucoes": ["Verificar interface", "Checar rotas", "Revisar ACLs"]
                },
                "interface_down": {
                    "sintomas": ["interface down", "link down", "no carrier"],
                    "causas": ["Cabo desconectado", "Speed/duplex mismatch", "SFP com defeito"],
                    "comandos_diagnostico": {
                        "cisco": ["show interface", "show controllers"],
                        "nokia": ["show port", "show port optical"],
                        "fortigate": ["get system interface physical"],
                        "huawei": ["display interface", "display transceiver"]
                    },
                    "solucoes": ["Verificar cabos", "Checar shutdown", "Testar SFP"]
                }
            },
            "roteamento": {
                "bgp_down": {
                    "sintomas": ["bgp down", "neighbor down", "idle state"],
                    "causas": ["AS incorreto", "IP errado", "MD5 mismatch", "ACL porta 179"],
                    "comandos_diagnostico": {
                        "cisco": ["show bgp summary", "show bgp neighbor"],
                        "nokia": ["show router bgp summary", "show router bgp neighbor"],
                        "fortigate": ["get router info bgp summary"],
                        "huawei": ["display bgp peer"]
                    },
                    "solucoes": ["Verificar AS e IP", "Checar senha MD5", "Verificar rota"]
                },
                "ospf_adjacency": {
                    "sintomas": ["ospf neighbor", "adjacency", "2way", "exstart"],
                    "causas": ["Hello/Dead diferentes", "Área diferente", "MTU mismatch"],
                    "comandos_diagnostico": {
                        "cisco": ["show ip ospf neighbor", "show ip ospf interface"],
                        "nokia": ["show router ospf neighbor", "show router ospf interface"],
                        "fortigate": ["get router info ospf neighbor"],
                        "huawei": ["display ospf peer"]
                    },
                    "solucoes": ["Checar área", "Verificar timers", "Conferir MTU"]
                }
            },
            "performance": {
                "cpu_alta": {
                    "sintomas": ["cpu alta", "high cpu", "lento", "cpu 100"],
                    "causas": ["Processo travado", "DDoS", "Log excessivo", "Bug"],
                    "comandos_diagnostico": {
                        "cisco": ["show processes cpu sorted"],
                        "nokia": ["show system cpu"],
                        "fortigate": ["diagnose sys top"],
                        "huawei": ["display cpu-usage"]
                    },
                    "solucoes": ["Identificar processo", "Verificar ataque", "Reduzir logs"]
                }
            },
            "seguranca": {
                "acl_bloqueio": {
                    "sintomas": ["acl deny", "bloqueado", "blocked"],
                    "causas": ["ACL restritiva", "Ordem errada", "Implicit deny"],
                    "comandos_diagnostico": {
                        "cisco": ["show access-lists"],
                        "nokia": ["show filter ip"],
                        "fortigate": ["get firewall policy"],
                        "huawei": ["display acl all"]
                    },
                    "solucoes": ["Revisar regras", "Adicionar logging", "Checar direção"]
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
            else:
                resultado = {"sucesso": False, "fonte": "", "diagnostico": {}, "erro": resposta_ia["erro"]}
        else:
            resultado = {"sucesso": False, "fonte": "", "diagnostico": {}, 
                        "erro": "Problema não encontrado na base local."}
        
        self.historico_diagnosticos.append({
            "timestamp": inicio.isoformat(), "problema": problema, "fabricante": fabricante,
            "versao": versao, "categoria": categoria, "fonte": resultado.get("fonte", ""),
            "sucesso": resultado["sucesso"]
        })
        return resultado
    
    def _buscar_local(self, problema: str, categoria: str, fabricante: str) -> Optional[Dict]:
        """Busca na base de conhecimento local por palavras-chave."""
        problema_lower = problema.lower()
        categorias = [categoria] if categoria in self.problemas_comuns else list(self.problemas_comuns.keys())
        
        for cat in categorias:
            for nome_prob, dados in self.problemas_comuns[cat].items():
                for sintoma in dados["sintomas"]:
                    if sintoma.lower() in problema_lower:
                        resultado = {"categoria": cat, "problema_identificado": nome_prob,
                                   "causas": dados["causas"], "solucoes": dados["solucoes"]}
                        if fabricante in dados["comandos_diagnostico"]:
                            resultado["comandos"] = dados["comandos_diagnostico"][fabricante]
                        else:
                            resultado["comandos"] = list(dados["comandos_diagnostico"].values())[0]
                        return resultado
        return None
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas dos diagnósticos realizados."""
        if not self.historico_diagnosticos:
            return {"total": 0, "sucesso": 0, "taxa_sucesso": 0, "por_fabricante": {}}
        total = len(self.historico_diagnosticos)
        sucesso = sum(1 for d in self.historico_diagnosticos if d["sucesso"])
        por_fab = {}
        for d in self.historico_diagnosticos:
            fab = d.get("fabricante", "desconhecido")
            por_fab[fab] = por_fab.get(fab, 0) + 1
        return {"total": total, "sucesso": sucesso, "taxa_sucesso": round((sucesso/total)*100, 1), 
                "por_fabricante": por_fab}
    
    def listar_categorias(self) -> List[str]:
        """Retorna categorias de problemas disponíveis."""
        return list(self.problemas_comuns.keys())
