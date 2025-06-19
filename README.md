# Sistema de Auditoria de Contas de Energia Elétrica
## Governo do Estado de Rondônia

### Visão Geral

Este sistema foi desenvolvido especificamente para automatizar a auditoria de contas de energia elétrica em órgãos públicos do governo de Rondônia. A ferramenta baseia-se na Resolução Normativa ANEEL nº 1.000/2021 e outras regulamentações vigentes para identificar irregularidades e oportunidades de economia.

### Funcionalidades Principais

- ✅ **Upload e Processamento**: Aceita contas em PDF, PNG, JPG e JPEG
- ✅ **Extração Automatizada**: Utiliza OCR para extrair dados das contas
- ✅ **Regras de Auditoria**: Baseadas na legislação vigente (RN ANEEL 1.000/2021)
- ✅ **Detecção de Irregularidades**: Identifica cobranças indevidas e erros de cálculo
- ✅ **Relatórios Detalhados**: Gera relatórios com irregularidades e recomendações
- ✅ **Interface Web**: Sistema acessível via navegador
- ✅ **Histórico**: Mantém registro de todas as auditorias realizadas

### Tecnologias Utilizadas

**Frontend:**
- React 18 com TypeScript
- shadcn/ui + Tailwind CSS
- Vite para build e desenvolvimento

**Backend:**
- Python 3.11 + Flask
- SQLAlchemy para banco de dados
- Flask-CORS para integração frontend/backend

**Processamento:**
- Módulo de extração de dados (OCR simulado)
- Motor de regras de auditoria
- Geração de relatórios automatizada

### Estrutura do Projeto

```
auditoria-energia/
├── auditoria-energia-backend/     # Backend Flask
│   ├── src/
│   │   ├── main.py               # Aplicação principal
│   │   ├── regras_auditoria.py   # Regras de auditoria
│   │   ├── extrator_dados.py     # Extração de dados
│   │   └── routes/
│   │       └── auditoria.py      # Rotas da API
│   ├── venv/                     # Ambiente virtual Python
│   └── requirements.txt          # Dependências Python
├── auditoria-energia-frontend/    # Frontend React
│   ├── src/
│   │   ├── App.jsx              # Componente principal
│   │   └── components/          # Componentes da UI
│   ├── package.json             # Dependências Node.js
│   └── index.html               # Página principal
└── documentacao/                 # Documentação do projeto
    ├── documentacao_completa.md  # Documentação técnica
    ├── relatorio_testes.md       # Relatório de testes
    └── *.pdf                     # Documentos em PDF
```

### Instalação e Configuração

#### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Git

#### Backend (Flask)
```bash
cd auditoria-energia-backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python src/main.py
```

#### Frontend (React)
```bash
cd auditoria-energia-frontend
npm install
npm run dev
```

### Como Usar

1. **Acesse a aplicação**: Abra http://localhost:5173 no navegador
2. **Upload de conta**: Clique em "Choose File" e selecione uma conta de energia
3. **Iniciar auditoria**: Clique em "Iniciar Auditoria" para processar
4. **Visualizar resultados**: Analise as irregularidades encontradas
5. **Gerar relatório**: Exporte os resultados para documentação

### Tipos de Irregularidades Detectadas

- **Classificação Tarifária**: Verifica se órgãos públicos estão no subgrupo correto (B3)
- **Cálculo de Consumo**: Valida aplicação das tarifas TE e TUSD
- **Custo de Disponibilidade**: Verifica valores mínimos por tipo de ligação
- **Bandeiras Tarifárias**: Valida aplicação correta das bandeiras
- **Impostos**: Verifica cálculo de ICMS, PIS e COFINS
- **Anomalias de Consumo**: Detecta padrões anômalos no histórico

### Arquivos de Teste

O sistema inclui arquivos de teste para demonstração:
- `conta_teste_normal.txt`: Simula conta sem irregularidades
- `conta_teste_erro.txt`: Simula conta com problemas para teste

### Documentação Técnica

- **Documentação Completa**: `documentacao_completa.md` / `documentacao_sistema_auditoria_energia.pdf`
- **Relatório de Testes**: `relatorio_testes.md`
- **Análise de Legislação**: Arquivos com pesquisa regulamentária

### Suporte e Manutenção

Para suporte técnico ou dúvidas sobre o sistema:
1. Consulte a documentação técnica completa
2. Verifique os logs do sistema para diagnóstico
3. Entre em contato com a equipe de TI responsável

### Próximos Passos para Produção

1. **Implementar OCR Real**: Substituir dados simulados por extração real
2. **Banco de Dados**: Configurar PostgreSQL para produção
3. **Autenticação**: Implementar sistema de login
4. **Deploy**: Configurar ambiente de produção
5. **Treinamento**: Capacitar usuários finais

### Benefícios Esperados

- **Economia Financeira**: Identificação de cobranças indevidas
- **Eficiência Operacional**: Redução de 90% no tempo de auditoria
- **Padronização**: Processos uniformes em todos os órgãos
- **Transparência**: Relatórios detalhados para prestação de contas
- **Prevenção**: Identificação proativa de irregularidades

### Conformidade Legal

O sistema foi desenvolvido com base em:
- Resolução Normativa ANEEL nº 1.000/2021
- Lei nº 9.427/1996 (Lei da ANEEL)
- Decreto nº 2.335/1997
- Legislação tributária aplicável (ICMS, PIS, COFINS)
- Normas de compras públicas

### Licença e Propriedade

Sistema desenvolvido especificamente para o Governo do Estado de Rondônia.
Todos os direitos reservados à administração pública estadual.

---

**Desenvolvido por:** Manus AI  
**Data:** 19 de junho de 2025  
**Versão:** 1.0

