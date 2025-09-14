#!/bin/bash
set -ex

LOGFILE=/tmp/setup.log

# Update system
apt update >> $LOGFILE 2>&1
apt upgrade -y >> $LOGFILE 2>&1

# Install dependencies
apt install -y software-properties-common >> $LOGFILE 2>&1
add-apt-repository ppa:deadsnakes/ppa -y >> $LOGFILE 2>&1
apt update >> $LOGFILE 2>&1
apt install -y python3.11 python3.11-venv python3-pip git nginx >> $LOGFILE 2>&1

# Setup project
if [ -d /opt/sslchecker ]; then
    echo "/opt/sslchecker exists, pulling latest changes..." >> $LOGFILE
    cd /opt/sslchecker
    git reset --hard >> $LOGFILE
    git pull >> $LOGFILE
else
    git clone https://github.com/GeorgiAndreev96/ssl-checker.git /opt/sslchecker >> $LOGFILE
    cd /opt/sslchecker >> $LOGFILE
fi

# Create virtualenv and install requirements
python3.11 -m venv /opt/sslchecker/venv >> $LOGFILE
source /opt/sslchecker/venv/bin/activate
cd /opt/sslchecker/backend
pip install --upgrade pip >> $LOGFILE
pip install -r requirements.txt >> $LOGFILE

# Setup systemd service
cat <<EOT > /etc/systemd/system/sslchecker.service
[Unit]
Description=SSL Checker FastAPI
After=network.target

[Service]
User=root
WorkingDirectory=/opt/sslchecker/backend
ExecStart=/opt/sslchecker/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOT

systemctl daemon-reload
systemctl enable sslchecker
systemctl start sslchecker

# Setup nginx
cat <<EOT > /etc/nginx/nginx.conf
user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout 65;

    server {
        listen 80;
        server_name _;

        # Frontend
        location / {
            root /opt/sslchecker/frontend;
            index index.html;
            try_files \$uri /index.html;
        }

        # Backend API
        location /api/ {
            proxy_pass http://127.0.0.1:8000/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOT

systemctl restart nginx
