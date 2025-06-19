"""
Módulo de regras de auditoria para contas de energia elétrica
Baseado na Resolução Normativa ANEEL nº 1.000/2021 e legislação aplicável
"""

import re
from datetime import datetime
from typing import Dict, List, Any, Optional

class RegrasAuditoria:
    """Classe que implementa as regras de auditoria para contas de energia elétrica"""
    
    def __init__(self):
        # Tarifas de referência (valores exemplo - devem ser atualizados com dados reais)
        self.tarifas_grupo_b = {
            'B1': {'TUSD': 0.27440, 'TE': 0.25141},  # Residencial
            'B1_BAIXA_RENDA': {'TUSD': 0.21623, 'TE': 0.25141},
            'B2_RURAL': {'TUSD': 0.20854, 'TE': 0.19107},
            'B2_COOPERATIVA': {'TUSD': 0.20854, 'TE': 0.19107},
            'B2_IRRIGACAO': {'TUSD': 0.18659, 'TE': 0.17096},
            'B3': {'TUSD': 0.27440, 'TE': 0.25141},  # Comercial/Industrial/Poder Público
            'B4A': {'TUSD': 0.27440, 'TE': 0.25141},  # Iluminação Pública
        }
        
        # Valores mínimos de disponibilidade por tipo de ligação
        self.custo_disponibilidade = {
            'monofasico': 30,  # kWh
            'bifasico': 50,    # kWh
            'trifasico': 100   # kWh
        }
        
        # Bandeiras tarifárias (valores em R$/kWh)
        self.bandeiras_tarifarias = {
            'verde': 0.0,
            'amarela': 0.01874,
            'vermelha_1': 0.03971,
            'vermelha_2': 0.09492
        }
        
        # Impostos aplicáveis
        self.impostos = {
            'ICMS': {'aliquota': 0.25, 'base_calculo': 'valor_total'},  # 25% sobre valor total
            'PIS': {'aliquota': 0.0165, 'base_calculo': 'energia_consumida'},  # 1,65%
            'COFINS': {'aliquota': 0.076, 'base_calculo': 'energia_consumida'},  # 7,6%
        }

    def auditar_conta(self, dados_conta: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza auditoria completa da conta de energia
        
        Args:
            dados_conta: Dicionário com dados extraídos da conta
            
        Returns:
            Resultado da auditoria com irregularidades encontradas
        """
        irregularidades = []
        resultado = {
            'status': 'processado',
            'data_auditoria': datetime.now().isoformat(),
            'irregularidades': irregularidades,
            'resumo': {
                'total_irregularidades': 0,
                'impacto_financeiro': 0.0,
                'status_geral': 'Conforme'
            }
        }
        
        try:
            # Verificar classificação tarifária
            irregularidades.extend(self._verificar_classificacao_tarifaria(dados_conta))
            
            # Verificar cálculo de consumo
            irregularidades.extend(self._verificar_calculo_consumo(dados_conta))
            
            # Verificar custo de disponibilidade
            irregularidades.extend(self._verificar_custo_disponibilidade(dados_conta))
            
            # Verificar bandeira tarifária
            irregularidades.extend(self._verificar_bandeira_tarifaria(dados_conta))
            
            # Verificar impostos
            irregularidades.extend(self._verificar_impostos(dados_conta))
            
            # Verificar histórico de consumo
            irregularidades.extend(self._verificar_historico_consumo(dados_conta))
            
            # Calcular impacto financeiro total
            impacto_total = sum(irreg.get('impacto_financeiro', 0) for irreg in irregularidades)
            
            resultado['irregularidades'] = irregularidades
            resultado['resumo'] = {
                'total_irregularidades': len(irregularidades),
                'impacto_financeiro': impacto_total,
                'status_geral': 'Não Conforme' if irregularidades else 'Conforme'
            }
            
        except Exception as e:
            resultado['erro'] = f"Erro durante auditoria: {str(e)}"
            
        return resultado

    def _verificar_classificacao_tarifaria(self, dados_conta: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica se a classificação tarifária está correta"""
        irregularidades = []
        
        subgrupo = dados_conta.get('subgrupo', '').upper()
        tipo_consumidor = dados_conta.get('tipo_consumidor', '').lower()
        
        # Verificar se órgão público está classificado corretamente
        if 'público' in tipo_consumidor or 'governo' in tipo_consumidor:
            if subgrupo not in ['B3', 'B4A']:
                irregularidades.append({
                    'tipo': 'Classificação Tarifária Incorreta',
                    'descricao': f'Órgão público classificado como {subgrupo}, deveria ser B3 ou B4A',
                    'severidade': 'Alta',
                    'impacto_financeiro': 0.0,
                    'recomendacao': 'Solicitar reclassificação para subgrupo adequado'
                })
        
        return irregularidades

    def _verificar_calculo_consumo(self, dados_conta: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica se o cálculo do consumo está correto"""
        irregularidades = []
        
        try:
            consumo_kwh = float(dados_conta.get('consumo_kwh', 0))
            valor_energia = float(dados_conta.get('valor_energia', 0))
            subgrupo = dados_conta.get('subgrupo', 'B3')
            
            if subgrupo in self.tarifas_grupo_b:
                tarifa_te = self.tarifas_grupo_b[subgrupo]['TE']
                tarifa_tusd = self.tarifas_grupo_b[subgrupo]['TUSD']
                
                valor_esperado = consumo_kwh * (tarifa_te + tarifa_tusd)
                diferenca = abs(valor_energia - valor_esperado)
                
                # Tolerância de 5% para diferenças de arredondamento
                tolerancia = valor_esperado * 0.05
                
                if diferenca > tolerancia:
                    irregularidades.append({
                        'tipo': 'Cálculo de Consumo Incorreto',
                        'descricao': f'Valor cobrado: R$ {valor_energia:.2f}, Valor esperado: R$ {valor_esperado:.2f}',
                        'severidade': 'Alta',
                        'impacto_financeiro': diferenca,
                        'recomendacao': 'Verificar aplicação das tarifas TE e TUSD'
                    })
                    
        except (ValueError, TypeError):
            irregularidades.append({
                'tipo': 'Dados Inconsistentes',
                'descricao': 'Não foi possível verificar o cálculo do consumo devido a dados inválidos',
                'severidade': 'Média',
                'impacto_financeiro': 0.0,
                'recomendacao': 'Verificar dados da conta manualmente'
            })
            
        return irregularidades

    def _verificar_custo_disponibilidade(self, dados_conta: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica se o custo de disponibilidade está sendo aplicado corretamente"""
        irregularidades = []
        
        try:
            consumo_kwh = float(dados_conta.get('consumo_kwh', 0))
            tipo_ligacao = dados_conta.get('tipo_ligacao', 'monofasico').lower()
            
            if tipo_ligacao in self.custo_disponibilidade:
                minimo_kwh = self.custo_disponibilidade[tipo_ligacao]
                
                if consumo_kwh < minimo_kwh:
                    # Deve ser cobrado o mínimo
                    subgrupo = dados_conta.get('subgrupo', 'B3')
                    if subgrupo in self.tarifas_grupo_b:
                        tarifa_total = self.tarifas_grupo_b[subgrupo]['TE'] + self.tarifas_grupo_b[subgrupo]['TUSD']
                        valor_minimo_esperado = minimo_kwh * tarifa_total
                        valor_cobrado = float(dados_conta.get('valor_energia', 0))
                        
                        if abs(valor_cobrado - valor_minimo_esperado) > valor_minimo_esperado * 0.05:
                            irregularidades.append({
                                'tipo': 'Custo de Disponibilidade Incorreto',
                                'descricao': f'Consumo {consumo_kwh} kWh abaixo do mínimo {minimo_kwh} kWh para {tipo_ligacao}',
                                'severidade': 'Média',
                                'impacto_financeiro': abs(valor_cobrado - valor_minimo_esperado),
                                'recomendacao': f'Verificar aplicação do custo mínimo de {minimo_kwh} kWh'
                            })
                            
        except (ValueError, TypeError):
            pass
            
        return irregularidades

    def _verificar_bandeira_tarifaria(self, dados_conta: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica se a bandeira tarifária está sendo aplicada corretamente"""
        irregularidades = []
        
        try:
            bandeira = dados_conta.get('bandeira_tarifaria', '').lower()
            consumo_kwh = float(dados_conta.get('consumo_kwh', 0))
            valor_bandeira = float(dados_conta.get('valor_bandeira', 0))
            
            if bandeira in self.bandeiras_tarifarias:
                valor_esperado = consumo_kwh * self.bandeiras_tarifarias[bandeira]
                diferenca = abs(valor_bandeira - valor_esperado)
                
                if diferenca > 0.01:  # Tolerância de R$ 0,01
                    irregularidades.append({
                        'tipo': 'Bandeira Tarifária Incorreta',
                        'descricao': f'Valor bandeira {bandeira}: R$ {valor_bandeira:.2f}, esperado: R$ {valor_esperado:.2f}',
                        'severidade': 'Média',
                        'impacto_financeiro': diferenca,
                        'recomendacao': 'Verificar aplicação da bandeira tarifária'
                    })
                    
        except (ValueError, TypeError):
            pass
            
        return irregularidades

    def _verificar_impostos(self, dados_conta: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica se os impostos estão sendo calculados corretamente"""
        irregularidades = []
        
        # Verificação básica de ICMS (implementação simplificada)
        try:
            valor_total = float(dados_conta.get('valor_total', 0))
            icms_cobrado = float(dados_conta.get('icms', 0))
            
            # ICMS é calculado sobre o valor total (incluindo ele mesmo)
            # Valor sem ICMS = Valor Total / (1 + alíquota)
            valor_sem_icms = valor_total / (1 + self.impostos['ICMS']['aliquota'])
            icms_esperado = valor_sem_icms * self.impostos['ICMS']['aliquota']
            
            diferenca = abs(icms_cobrado - icms_esperado)
            
            if diferenca > valor_total * 0.01:  # Tolerância de 1%
                irregularidades.append({
                    'tipo': 'ICMS Incorreto',
                    'descricao': f'ICMS cobrado: R$ {icms_cobrado:.2f}, esperado: R$ {icms_esperado:.2f}',
                    'severidade': 'Alta',
                    'impacto_financeiro': diferenca,
                    'recomendacao': 'Verificar cálculo do ICMS'
                })
                
        except (ValueError, TypeError):
            pass
            
        return irregularidades

    def _verificar_historico_consumo(self, dados_conta: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica padrões anômalos no histórico de consumo"""
        irregularidades = []
        
        try:
            historico = dados_conta.get('historico_consumo', [])
            if len(historico) >= 3:
                consumos = [float(h) for h in historico[-3:]]  # Últimos 3 meses
                media = sum(consumos) / len(consumos)
                consumo_atual = consumos[-1]
                
                # Verificar variação superior a 50%
                if consumo_atual > media * 1.5:
                    irregularidades.append({
                        'tipo': 'Consumo Anômalo',
                        'descricao': f'Consumo atual ({consumo_atual} kWh) 50% acima da média ({media:.1f} kWh)',
                        'severidade': 'Baixa',
                        'impacto_financeiro': 0.0,
                        'recomendacao': 'Verificar possível vazamento ou equipamento com defeito'
                    })
                elif consumo_atual < media * 0.5:
                    irregularidades.append({
                        'tipo': 'Consumo Anômalo',
                        'descricao': f'Consumo atual ({consumo_atual} kWh) 50% abaixo da média ({media:.1f} kWh)',
                        'severidade': 'Baixa',
                        'impacto_financeiro': 0.0,
                        'recomendacao': 'Verificar possível problema na medição'
                    })
                    
        except (ValueError, TypeError):
            pass
            
        return irregularidades

    def gerar_recomendacoes(self, dados_conta: Dict[str, Any]) -> List[str]:
        """Gera recomendações para otimização do consumo"""
        recomendacoes = []
        
        try:
            consumo_kwh = float(dados_conta.get('consumo_kwh', 0))
            subgrupo = dados_conta.get('subgrupo', '')
            
            # Recomendação para tarifa branca (se aplicável)
            if subgrupo == 'B3' and consumo_kwh > 250:
                recomendacoes.append(
                    'Considerar migração para tarifa branca se o consumo for concentrado fora do horário de ponta'
                )
            
            # Recomendação para eficiência energética
            if consumo_kwh > 1000:
                recomendacoes.append(
                    'Realizar auditoria energética para identificar oportunidades de economia'
                )
                
            # Recomendação para monitoramento
            recomendacoes.append(
                'Implementar sistema de monitoramento mensal do consumo para detectar anomalias'
            )
            
        except (ValueError, TypeError):
            pass
            
        return recomendacoes

