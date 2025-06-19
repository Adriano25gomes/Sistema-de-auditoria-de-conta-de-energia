from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
import sys

# Adicionar o diretório src ao path para importar os módulos
sys.path.append(os.path.dirname(__file__))
from src.regras_auditoria import RegrasAuditoria
from src.extrator_dados import ExtratorDados

auditoria_bp = Blueprint('auditoria', __name__)

# Configurações para upload de arquivos
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# Instanciar classes de processamento
regras_auditoria = RegrasAuditoria()
extrator_dados = ExtratorDados()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auditoria_bp.route('/upload', methods=['POST'])
def upload_conta():
    """Endpoint para upload de conta de energia"""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if file and allowed_file(file.filename):
        # Criar diretório de upload se não existir
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Salvar arquivo com nome seguro
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Processar a conta com as regras de auditoria
        resultado_auditoria = processar_conta(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'resultado': resultado_auditoria
        })
    
    return jsonify({'error': 'Tipo de arquivo não permitido'}), 400

def processar_conta(filepath):
    """Função para processar a conta de energia com regras de auditoria"""
    try:
        # Extrair dados da conta
        dados_conta = extrator_dados.extrair_dados_ocr(filepath)
        
        # Validar dados extraídos
        problemas_extracao = extrator_dados.validar_dados_extraidos(dados_conta)
        
        # Realizar auditoria
        resultado_auditoria = regras_auditoria.auditar_conta(dados_conta)
        
        # Gerar recomendações
        recomendacoes = regras_auditoria.gerar_recomendacoes(dados_conta)
        
        # Adicionar dados extraídos e recomendações ao resultado
        resultado_auditoria['dados_extraidos'] = dados_conta
        resultado_auditoria['recomendacoes'] = recomendacoes
        resultado_auditoria['problemas_extracao'] = problemas_extracao
        resultado_auditoria['arquivo'] = os.path.basename(filepath)
        
        return resultado_auditoria
        
    except Exception as e:
        return {
            'status': 'erro',
            'arquivo': os.path.basename(filepath),
            'data_processamento': datetime.now().isoformat(),
            'erro': f'Erro durante processamento: {str(e)}',
            'irregularidades': [],
            'resumo': {
                'total_irregularidades': 0,
                'impacto_financeiro': 0.0,
                'status_geral': 'Erro no Processamento'
            }
        }

@auditoria_bp.route('/historico', methods=['GET'])
def obter_historico():
    """Endpoint para obter histórico de auditorias"""
    # Placeholder - será implementado com dados do banco
    return jsonify({
        'auditorias': [
            {
                'id': 1,
                'data': '2025-06-19T14:30:00',
                'arquivo': 'conta_energia_maio_2025.pdf',
                'status': 'Conforme',
                'irregularidades': 0
            }
        ]
    })

@auditoria_bp.route('/relatorio/<int:auditoria_id>', methods=['GET'])
def gerar_relatorio(auditoria_id):
    """Endpoint para gerar relatório detalhado de auditoria"""
    # Placeholder - será implementado com dados reais
    return jsonify({
        'id': auditoria_id,
        'data_auditoria': '2025-06-19T14:30:00',
        'arquivo_original': 'conta_energia_maio_2025.pdf',
        'dados_extraidos': {
            'consumo_kwh': 1500,
            'valor_total': 450.75,
            'tarifa_aplicada': 'B3',
            'bandeira_tarifaria': 'Verde'
        },
        'irregularidades': [],
        'recomendacoes': [
            'Verificar possibilidade de migração para tarifa branca',
            'Analisar padrão de consumo para otimização'
        ]
    })

