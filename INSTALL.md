# Guia de Instalação e Deploy
## Sistema de Auditoria de Contas de Energia Elétrica

### Ambiente de Desenvolvimento

#### 1. Configuração do Backend

```bash
# Clone ou acesse o diretório do projeto
cd auditoria-energia-backend

# Criar ambiente virtual Python
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar servidor de desenvolvimento
python src/main.py
```

O backend estará disponível em: http://localhost:5000

#### 2. Configuração do Frontend

```bash
# Acessar diretório do frontend
cd auditoria-energia-frontend

# Instalar dependências
npm install

# Executar servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em: http://localhost:5173

### Ambiente de Produção

#### 1. Preparação do Servidor

**Requisitos do Sistema:**
- Ubuntu 20.04+ ou CentOS 7+
- Python 3.11+
- Node.js 18+
- Nginx
- PostgreSQL 12+

**Instalação de Dependências:**
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e pip
sudo apt install python3.11 python3.11-venv python3-pip -y

# Instalar Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Instalar Nginx
sudo apt install nginx -y

# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib -y
```

#### 2. Configuração do Banco de Dados

```bash
# Acessar PostgreSQL
sudo -u postgres psql

# Criar banco de dados e usuário
CREATE DATABASE auditoria_energia;
CREATE USER auditoria_user WITH PASSWORD 'senha_segura';
GRANT ALL PRIVILEGES ON DATABASE auditoria_energia TO auditoria_user;
\q
```

#### 3. Deploy do Backend

```bash
# Criar diretório da aplicação
sudo mkdir -p /opt/auditoria-energia
sudo chown $USER:$USER /opt/auditoria-energia

# Copiar arquivos do backend
cp -r auditoria-energia-backend /opt/auditoria-energia/

# Configurar ambiente virtual
cd /opt/auditoria-energia/auditoria-energia-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar variáveis de ambiente
cat > .env << EOF
DATABASE_URL=postgresql://auditoria_user:senha_segura@localhost/auditoria_energia
FLASK_ENV=production
SECRET_KEY=chave_secreta_muito_segura
EOF

# Criar serviço systemd
sudo tee /etc/systemd/system/auditoria-backend.service > /dev/null << EOF
[Unit]
Description=Sistema de Auditoria - Backend
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/auditoria-energia/auditoria-energia-backend
Environment=PATH=/opt/auditoria-energia/auditoria-energia-backend/venv/bin
ExecStart=/opt/auditoria-energia/auditoria-energia-backend/venv/bin/python src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Habilitar e iniciar serviço
sudo systemctl daemon-reload
sudo systemctl enable auditoria-backend
sudo systemctl start auditoria-backend
```

#### 4. Deploy do Frontend

```bash
# Build da aplicação React
cd auditoria-energia-frontend
npm run build

# Copiar arquivos para Nginx
sudo cp -r dist/* /var/www/html/auditoria-energia/

# Configurar Nginx
sudo tee /etc/nginx/sites-available/auditoria-energia > /dev/null << EOF
server {
    listen 80;
    server_name seu-dominio.com;
    
    root /var/www/html/auditoria-energia;
    index index.html;
    
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Habilitar site
sudo ln -s /etc/nginx/sites-available/auditoria-energia /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. Configuração SSL (Opcional)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obter certificado SSL
sudo certbot --nginx -d seu-dominio.com

# Configurar renovação automática
sudo crontab -e
# Adicionar linha:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

### Configurações de Segurança

#### 1. Firewall

```bash
# Configurar UFW
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

#### 2. Backup Automático

```bash
# Criar script de backup
sudo tee /opt/backup-auditoria.sh > /dev/null << EOF
#!/bin/bash
DATE=\$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/auditoria"

# Criar diretório de backup
mkdir -p \$BACKUP_DIR

# Backup do banco de dados
pg_dump -h localhost -U auditoria_user auditoria_energia > \$BACKUP_DIR/db_\$DATE.sql

# Backup dos arquivos
tar -czf \$BACKUP_DIR/files_\$DATE.tar.gz /opt/auditoria-energia

# Manter apenas últimos 7 backups
find \$BACKUP_DIR -name "*.sql" -mtime +7 -delete
find \$BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
EOF

sudo chmod +x /opt/backup-auditoria.sh

# Configurar cron para backup diário
sudo crontab -e
# Adicionar linha:
# 0 2 * * * /opt/backup-auditoria.sh
```

### Monitoramento

#### 1. Logs do Sistema

```bash
# Visualizar logs do backend
sudo journalctl -u auditoria-backend -f

# Visualizar logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

#### 2. Verificação de Status

```bash
# Status dos serviços
sudo systemctl status auditoria-backend
sudo systemctl status nginx
sudo systemctl status postgresql

# Verificar conectividade
curl http://localhost:5000/api/health
```

### Manutenção

#### 1. Atualização do Sistema

```bash
# Parar serviços
sudo systemctl stop auditoria-backend

# Backup antes da atualização
/opt/backup-auditoria.sh

# Atualizar código
cd /opt/auditoria-energia/auditoria-energia-backend
git pull origin main  # se usando Git
source venv/bin/activate
pip install -r requirements.txt

# Reiniciar serviços
sudo systemctl start auditoria-backend
sudo systemctl restart nginx
```

#### 2. Limpeza de Arquivos Temporários

```bash
# Criar script de limpeza
sudo tee /opt/cleanup-auditoria.sh > /dev/null << EOF
#!/bin/bash
# Limpar arquivos temporários de upload (mais de 24h)
find /tmp/uploads -type f -mtime +1 -delete

# Limpar logs antigos
find /var/log -name "*.log" -mtime +30 -delete
EOF

sudo chmod +x /opt/cleanup-auditoria.sh

# Executar limpeza diariamente
sudo crontab -e
# Adicionar linha:
# 0 3 * * * /opt/cleanup-auditoria.sh
```

### Solução de Problemas

#### 1. Backend não inicia

```bash
# Verificar logs
sudo journalctl -u auditoria-backend -n 50

# Verificar dependências
cd /opt/auditoria-energia/auditoria-energia-backend
source venv/bin/activate
pip check

# Testar manualmente
python src/main.py
```

#### 2. Frontend não carrega

```bash
# Verificar configuração do Nginx
sudo nginx -t

# Verificar logs do Nginx
sudo tail -f /var/log/nginx/error.log

# Verificar arquivos
ls -la /var/www/html/auditoria-energia/
```

#### 3. Problemas de Banco de Dados

```bash
# Verificar status do PostgreSQL
sudo systemctl status postgresql

# Testar conexão
psql -h localhost -U auditoria_user -d auditoria_energia

# Verificar logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

### Contatos de Suporte

- **Administrador do Sistema**: admin@rondonia.gov.br
- **Suporte Técnico**: ti@rondonia.gov.br
- **Documentação**: Consulte a documentação técnica completa

---

**Última atualização:** 19 de junho de 2025

