"""
Módulo para extração de dados de contas de energia elétrica
Utiliza OCR e processamento de texto para extrair informações relevantes
"""

import re
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

class ExtratorDados:
    """Classe para extrair dados de contas de energia elétrica"""
    
    def __init__(self):
        # Padrões regex para extração de dados
        self.padroes = {
            'consumo_kwh': [
                r'consumo.*?(\d+(?:,\d+)?)\s*kwh',
                r'energia\s+consumida.*?(\d+(?:,\d+)?)',
                r'(\d+(?:,\d+)?)\s*kwh'
            ],
            'valor_total': [
                r'total\s+a\s+pagar.*?r\$\s*(\d+(?:,\d+)?)',
                r'valor\s+total.*?r\$\s*(\d+(?:,\d+)?)',
                r'total.*?(\d+,\d{2})'
            ],
            'valor_energia': [
                r'energia\s+elétrica.*?r\$\s*(\d+(?:,\d+)?)',
                r'consumo\s+de\s+energia.*?(\d+,\d{2})'
            ],
            'subgrupo': [
                r'subgrupo[:\s]*([AB]\d[A-Z]?)',
                r'classe[:\s]*([AB]\d[A-Z]?)',
                r'tarifa[:\s]*([AB]\d[A-Z]?)'
            ],
            'bandeira_tarifaria': [
                r'bandeira\s+(verde|amarela|vermelha)',
                r'adicional\s+bandeira\s+(verde|amarela|vermelha)'
            ],
            'icms': [
                r'icms.*?r\$\s*(\d+(?:,\d+)?)',
                r'imposto.*?icms.*?(\d+,\d{2})'
            ],
            'numero_instalacao': [
                r'instalação[:\s]*(\d+)',
                r'nº\s+instalação[:\s]*(\d+)'
            ],
            'mes_referencia': [
                r'referência[:\s]*(\d{2}/\d{4})',
                r'período[:\s]*(\d{2}/\d{4})'
            ]
        }

    def extrair_dados_simulado(self, filepath: str) -> Dict[str, Any]:
        """
        Simula extração de dados de uma conta de energia
        Em uma implementação real, usaria OCR para extrair texto do PDF/imagem
        """
        # Dados simulados para demonstração
        dados_simulados = {
            'consumo_kwh': 1250,
            'valor_total': 485.75,
            'valor_energia': 342.50,
            'subgrupo': 'B3',
            'tipo_consumidor': 'Poder Público',
            'tipo_ligacao': 'trifasico',
            'bandeira_tarifaria': 'verde',
            'valor_bandeira': 0.0,
            'icms': 121.44,
            'pis': 5.68,
            'cofins': 26.03,
            'numero_instalacao': '123456789',
            'mes_referencia': '05/2025',
            'historico_consumo': [1180, 1320, 1250],  # Últimos 3 meses
            'distribuidora': 'ENERGISA RONDÔNIA',
            'endereco': 'Rua das Palmeiras, 123 - Centro - Porto Velho/RO',
            'data_vencimento': '2025-06-15',
            'data_leitura': '2025-05-20'
        }
        
        # Adicionar variação baseada no nome do arquivo para simular diferentes contas
        filename = os.path.basename(filepath).lower()
        
        if 'alto' in filename or 'comercial' in filename:
            dados_simulados['consumo_kwh'] = 2500
            dados_simulados['valor_total'] = 950.00
            dados_simulados['bandeira_tarifaria'] = 'amarela'
            dados_simulados['valor_bandeira'] = 46.88
            
        elif 'baixo' in filename or 'residencial' in filename:
            dados_simulados['consumo_kwh'] = 180
            dados_simulados['valor_total'] = 95.50
            dados_simulados['subgrupo'] = 'B1'
            dados_simulados['tipo_consumidor'] = 'Residencial'
            dados_simulados['tipo_ligacao'] = 'monofasico'
            
        elif 'erro' in filename or 'problema' in filename:
            # Simular conta com problemas para testar auditoria
            dados_simulados['consumo_kwh'] = 1250
            dados_simulados['valor_energia'] = 500.00  # Valor incorreto
            dados_simulados['icms'] = 200.00  # ICMS incorreto
            dados_simulados['bandeira_tarifaria'] = 'vermelha_1'
            dados_simulados['valor_bandeira'] = 10.00  # Valor incorreto da bandeira
            
        return dados_simulados

    def extrair_dados_ocr(self, filepath: str) -> Dict[str, Any]:
        """
        Extrai dados usando OCR (implementação futura)
        Por enquanto, retorna dados simulados
        """
        # TODO: Implementar OCR real
        # 1. Converter PDF para imagem se necessário
        # 2. Aplicar pré-processamento na imagem
        # 3. Usar Tesseract OCR para extrair texto
        # 4. Aplicar regex patterns para extrair dados específicos
        
        return self.extrair_dados_simulado(filepath)

    def _extrair_campo(self, texto: str, campo: str) -> Optional[str]:
        """Extrai um campo específico do texto usando regex"""
        if campo not in self.padroes:
            return None
            
        texto_limpo = texto.lower().replace('\n', ' ')
        
        for padrao in self.padroes[campo]:
            match = re.search(padrao, texto_limpo, re.IGNORECASE)
            if match:
                return match.group(1)
                
        return None

    def _converter_valor_monetario(self, valor_str: str) -> float:
        """Converte string de valor monetário para float"""
        if not valor_str:
            return 0.0
            
        # Remove caracteres não numéricos exceto vírgula e ponto
        valor_limpo = re.sub(r'[^\d,.]', '', valor_str)
        
        # Converte vírgula para ponto (padrão brasileiro)
        valor_limpo = valor_limpo.replace(',', '.')
        
        try:
            return float(valor_limpo)
        except ValueError:
            return 0.0

    def _converter_consumo(self, consumo_str: str) -> float:
        """Converte string de consumo para float"""
        if not consumo_str:
            return 0.0
            
        # Remove caracteres não numéricos exceto vírgula
        consumo_limpo = re.sub(r'[^\d,]', '', consumo_str)
        
        # Converte vírgula para ponto
        consumo_limpo = consumo_limpo.replace(',', '.')
        
        try:
            return float(consumo_limpo)
        except ValueError:
            return 0.0

    def validar_dados_extraidos(self, dados: Dict[str, Any]) -> Dict[str, List[str]]:
        """Valida os dados extraídos e retorna lista de problemas encontrados"""
        problemas = {
            'criticos': [],
            'avisos': []
        }
        
        # Verificações críticas
        if not dados.get('consumo_kwh') or dados['consumo_kwh'] <= 0:
            problemas['criticos'].append('Consumo em kWh não encontrado ou inválido')
            
        if not dados.get('valor_total') or dados['valor_total'] <= 0:
            problemas['criticos'].append('Valor total não encontrado ou inválido')
            
        if not dados.get('subgrupo'):
            problemas['criticos'].append('Subgrupo tarifário não identificado')
            
        # Verificações de aviso
        if not dados.get('numero_instalacao'):
            problemas['avisos'].append('Número da instalação não encontrado')
            
        if not dados.get('mes_referencia'):
            problemas['avisos'].append('Mês de referência não identificado')
            
        if not dados.get('bandeira_tarifaria'):
            problemas['avisos'].append('Bandeira tarifária não identificada')
            
        return problemas

