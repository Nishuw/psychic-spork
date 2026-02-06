# -*- coding: utf-8 -*-
"""
========================================
NetRouter AI - Engine de Inteligência Artificial
========================================
Este é o coração inteligente do sistema!

Aqui fazemos a integração com o Google Gemini para:
- Analisar problemas de rede descritos pelo usuário
- Sugerir soluções baseadas no contexto do roteador
- Gerar explicações sobre comandos e configurações
- Responder perguntas sobre troubleshooting

Por que usar Google Gemini?
- É uma IA muito poderosa e atualizada
- Tem excelente compreensão de contexto técnico
- A API é simples de usar
- Suporta conversas longas com histórico
========================================
"""

import os
import google.generativeai as genai
from typing import Optional, List, Dict

# Importa as configurações do sistema
from app.config import Config


class AIEngine:
    """
    Classe que encapsula toda a lógica de IA do sistema.
    
    Ela é responsável por:
    1. Configurar e conectar com a API do Gemini
    2. Montar prompts específicos para troubleshooting de rede
    3. Processar as respostas da IA
    4. Manter o contexto da conversa
    
    Atributos:
    ----------
    model : GenerativeModel
        Instância do modelo Gemini configurado
    
    chat_history : List[Dict]
        Histórico da conversa atual (para contexto)
    
    system_prompt : str
        Prompt base que define o comportamento da IA
    
    Exemplo de uso:
    ---------------
    >>> engine = AIEngine()
    >>> resposta = engine.analisar_problema(
    ...     "Roteador não responde a ping",
    ...     fabricante="cisco",
    ...     versao="ios-xe-17"
    ... )
    >>> print(resposta)
    """
    
    def __init__(self):
        """
        Inicializa a engine de IA.
        
        Configura a API do Gemini e prepara o modelo para uso.
        Se a API key não estiver configurada, avisa mas não quebra.
        """
        # Pega a API key das configurações
        self.api_key = Config.GOOGLE_API_KEY
        
        # Inicializa como None - será configurado se tiver API key
        self.model = None
        self.chat = None
        
        # Histórico de mensagens para manter contexto
        self.chat_history: List[Dict] = []
        
        # Prompt do sistema - define a "personalidade" da IA
        # Isso é MUITO importante para a qualidade das respostas
        self.system_prompt = self._criar_system_prompt()
        
        # Tenta configurar o Gemini
        if self.api_key:
            self._configurar_gemini()
        else:
            print("⚠️ AVISO: API Key do Google não configurada!")
            print("   O sistema funcionará, mas sem recursos de IA.")
            print("   Configure GOOGLE_API_KEY no arquivo .env")
    
    def _configurar_gemini(self):
        """
        Configura a conexão com a API do Google Gemini.
        
        Este método é chamado no __init__ se tivermos API key.
        Configura o modelo e as opções de geração de texto.
        """
        try:
            # Configura a biblioteca com nossa API key
            genai.configure(api_key=self.api_key)
            
            # Configurações de geração - controla como a IA responde
            generation_config = {
                # Temperatura: 0 = mais preciso, 1 = mais criativo
                # Para troubleshooting, queremos precisão!
                "temperature": 0.3,
                
                # Top P: diversidade das respostas
                "top_p": 0.8,
                
                # Top K: quantas palavras considerar
                "top_k": 40,
                
                # Máximo de tokens na resposta
                "max_output_tokens": 2048,
            }
            
            # Configurações de segurança - relaxamos um pouco
            # porque estamos falando de termos técnicos que podem
            # ser mal interpretados (como "kill process", "terminate", etc)
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                }
            ]
            
            # Cria o modelo com as configurações
            self.model = genai.GenerativeModel(
                model_name=Config.GEMINI_MODEL,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            # Inicia uma sessão de chat para manter contexto
            self.chat = self.model.start_chat(history=[])
            
            print("✅ Engine de IA configurada com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao configurar Gemini: {str(e)}")
            self.model = None
    
    def _criar_system_prompt(self) -> str:
        """
        Cria o prompt do sistema que define o comportamento da IA.
        
        Esse prompt é FUNDAMENTAL para a qualidade das respostas.
        Ele ensina a IA a:
        - Se comportar como um engenheiro de redes experiente
        - Dar respostas práticas e objetivas
        - Considerar o fabricante e versão específicos
        - Formatar as respostas de forma clara
        
        Retorna:
        --------
        str
            O prompt do sistema completo
        """
        # Prompt bem detalhado para obter respostas de qualidade
        return """Você é um Engenheiro de Redes Sênior especializado em troubleshooting e configuração de roteadores enterprise.

EXPERTISE:
- Cisco (IOS, IOS-XE, IOS-XR, NX-OS)
- Nokia Service Router (SR OS)
- Fortinet FortiGate (FortiOS)
- Huawei (VRP, CloudEngine, USG)

COMPORTAMENTO:
1. Seja DIRETO e PRÁTICO nas respostas
2. Sempre considere o fabricante e versão específicos informados
3. Forneça comandos EXATOS que podem ser copiados e colados
4. Explique o que cada comando faz em comentários
5. Sugira comandos de verificação após correções
6. Alerte sobre riscos ou impactos das ações

FORMATO DAS RESPOSTAS:
- Use markdown para formatação
- Separe comandos em blocos de código
- Liste passos numerados quando apropriado
- Destaque avisos importantes com ⚠️
- Use ✅ para confirmações e ❌ para alertas

IMPORTANTE:
- Nunca invente comandos que não existem
- Se não souber algo específico de uma versão, avise
- Priorize segurança - sugira backups antes de mudanças
- Considere impactos em ambiente de produção"""
    
    def analisar_problema(
        self,
        descricao_problema: str,
        fabricante: str = "",
        versao: str = "",
        logs: str = "",
        contexto_adicional: str = ""
    ) -> Dict:
        """
        Analisa um problema de rede e retorna diagnóstico + soluções.
        
        Esta é a função principal de troubleshooting!
        Ela monta um prompt detalhado com todas as informações
        e pede para a IA analisar e sugerir soluções.
        
        Parâmetros:
        -----------
        descricao_problema : str
            Descrição do problema pelo usuário
            Ex: "BGP session não estabelece com peer"
        
        fabricante : str
            Fabricante do equipamento (cisco, nokia, fortigate, huawei)
        
        versao : str
            Versão do sistema operacional
            Ex: "ios-xe-17" ou "fortios-74"
        
        logs : str
            Logs ou outputs de comandos relevantes (opcional)
        
        contexto_adicional : str
            Qualquer info extra útil (topologia, histórico, etc)
        
        Retorna:
        --------
        Dict
            Dicionário com:
            - sucesso: bool
            - analise: str (resposta da IA)
            - erro: str (se houver erro)
        
        Exemplo:
        --------
        >>> resultado = engine.analisar_problema(
        ...     "Interface GigabitEthernet0/0 está flapping",
        ...     fabricante="cisco",
        ...     versao="ios-xe-17"
        ... )
        """
        # Se não temos modelo configurado, retorna erro amigável
        if not self.model:
            return {
                "sucesso": False,
                "analise": "",
                "erro": "IA não configurada. Verifique a API key."
            }
        
        try:
            # Monta o prompt completo para análise
            prompt = self._montar_prompt_analise(
                descricao_problema,
                fabricante,
                versao,
                logs,
                contexto_adicional
            )
            
            # Envia para a IA e aguarda resposta
            # Usamos o chat para manter contexto entre mensagens
            resposta = self.chat.send_message(prompt)
            
            # Adiciona ao histórico local
            self.chat_history.append({
                "role": "user",
                "content": descricao_problema
            })
            self.chat_history.append({
                "role": "assistant",
                "content": resposta.text
            })
            
            return {
                "sucesso": True,
                "analise": resposta.text,
                "erro": ""
            }
            
        except Exception as e:
            # Se der erro, retorna info útil para debug
            return {
                "sucesso": False,
                "analise": "",
                "erro": f"Erro ao analisar: {str(e)}"
            }
    
    def _montar_prompt_analise(
        self,
        problema: str,
        fabricante: str,
        versao: str,
        logs: str,
        contexto: str
    ) -> str:
        """
        Monta o prompt completo para análise de problema.
        
        Aqui organizamos todas as informações em um formato
        que a IA consiga entender bem e dar respostas relevantes.
        """
        # Começa com o contexto do equipamento
        prompt_parts = [self.system_prompt, "\n\n---\n\n"]
        
        # Adiciona info do fabricante se informado
        if fabricante:
            info_fab = Config.FABRICANTES_SUPORTADOS.get(fabricante, {})
            nome_fab = info_fab.get('nome', fabricante.title())
            prompt_parts.append(f"**Equipamento:** {nome_fab}\n")
        
        # Adiciona versão se informada
        if versao and fabricante:
            versoes = Config.FABRICANTES_SUPORTADOS.get(fabricante, {}).get('versoes', {})
            info_versao = versoes.get(versao, {})
            nome_versao = info_versao.get('nome', versao)
            prompt_parts.append(f"**Versão:** {nome_versao}\n")
        
        # Adiciona o problema principal
        prompt_parts.append(f"\n**PROBLEMA RELATADO:**\n{problema}\n")
        
        # Adiciona logs se fornecidos
        if logs:
            prompt_parts.append(f"\n**LOGS/OUTPUT:**\n```\n{logs}\n```\n")
        
        # Adiciona contexto extra
        if contexto:
            prompt_parts.append(f"\n**CONTEXTO ADICIONAL:**\n{contexto}\n")
        
        # Instrução final
        prompt_parts.append("""
---

Por favor, analise o problema acima e forneça:
1. **Possíveis Causas** - Lista das causas mais prováveis
2. **Comandos de Diagnóstico** - Comandos para investigar (específicos para o fabricante/versão)
3. **Solução Recomendada** - Passos para resolver o problema
4. **Verificação** - Como confirmar que o problema foi resolvido
""")
        
        return "".join(prompt_parts)
    
    def gerar_script_ia(
        self,
        descricao_tarefa: str,
        fabricante: str,
        versao: str,
        tipo_script: str = "configuracao"
    ) -> Dict:
        """
        Usa a IA para gerar scripts de configuração.
        
        Além dos templates pré-definidos, podemos pedir para
        a IA gerar scripts customizados para tarefas específicas.
        
        Parâmetros:
        -----------
        descricao_tarefa : str
            O que o script deve fazer
            Ex: "Configurar OSPF na interface GigabitEthernet0/0"
        
        fabricante : str
            Fabricante do roteador
        
        versao : str
            Versão do sistema
        
        tipo_script : str
            Tipo de script: configuracao, backup, diagnostico, rollback
        
        Retorna:
        --------
        Dict
            - sucesso: bool
            - script: str (o script gerado)
            - explicacao: str (o que cada parte faz)
            - erro: str (se houver)
        """
        if not self.model:
            return {
                "sucesso": False,
                "script": "",
                "explicacao": "",
                "erro": "IA não configurada."
            }
        
        try:
            # Monta prompt específico para geração de scripts
            prompt = f"""{self.system_prompt}

---

**TAREFA:** Gerar script de {tipo_script}

**Equipamento:** {fabricante.title()}
**Versão:** {versao}

**O que o script deve fazer:**
{descricao_tarefa}

---

Por favor, gere:
1. **Script completo** pronto para copiar e colar
2. **Comentários** explicando cada seção/comando
3. **Avisos** sobre riscos ou pré-requisitos
4. **Comandos de verificação** para confirmar que funcionou

Formate o script em bloco de código apropriado.
"""
            
            resposta = self.chat.send_message(prompt)
            
            return {
                "sucesso": True,
                "script": resposta.text,
                "explicacao": "",  # Já está incluída na resposta
                "erro": ""
            }
            
        except Exception as e:
            return {
                "sucesso": False,
                "script": "",
                "explicacao": "",
                "erro": f"Erro ao gerar script: {str(e)}"
            }
    
    def chat_livre(self, mensagem: str) -> Dict:
        """
        Permite conversa livre com a IA sobre temas de rede.
        
        Usado pelo chat do dashboard para perguntas gerais.
        Mantém o contexto da conversa.
        
        Parâmetros:
        -----------
        mensagem : str
            Mensagem do usuário
        
        Retorna:
        --------
        Dict
            - sucesso: bool
            - resposta: str
            - erro: str
        """
        if not self.model:
            return {
                "sucesso": False,
                "resposta": "",
                "erro": "IA não configurada. Verifique a API key no arquivo .env"
            }
        
        try:
            # Adiciona contexto se for a primeira mensagem
            if not self.chat_history:
                mensagem_completa = f"{self.system_prompt}\n\n---\n\nUsuário: {mensagem}"
            else:
                mensagem_completa = mensagem
            
            resposta = self.chat.send_message(mensagem_completa)
            
            # Atualiza histórico
            self.chat_history.append({"role": "user", "content": mensagem})
            self.chat_history.append({"role": "assistant", "content": resposta.text})
            
            return {
                "sucesso": True,
                "resposta": resposta.text,
                "erro": ""
            }
            
        except Exception as e:
            return {
                "sucesso": False,
                "resposta": "",
                "erro": f"Erro no chat: {str(e)}"
            }
    
    def limpar_historico(self):
        """
        Limpa o histórico de conversa.
        
        Útil quando queremos começar um novo troubleshooting
        sem o contexto da conversa anterior.
        """
        self.chat_history = []
        
        # Reinicia a sessão de chat também
        if self.model:
            self.chat = self.model.start_chat(history=[])
        
        print("🧹 Histórico de conversa limpo!")
    
    def obter_historico(self) -> List[Dict]:
        """
        Retorna o histórico da conversa atual.
        
        Retorna:
        --------
        List[Dict]
            Lista de mensagens com role e content
        """
        return self.chat_history.copy()
