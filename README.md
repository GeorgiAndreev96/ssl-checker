# 🔒 SSL Checker

A simple **SSL certificate checker** with a FastAPI backend and a JS frontend.  
It allows you to check SSL/TLS expiration and details for any domain.

---

## 🚀 Features
- ✅ Check SSL certificate validity for a given domain
- ✅ View expiry date, issuer, and validity period
- ✅ REST API built with FastAPI
- ✅ Frontend built with JS (served by Nginx)
- ✅ Deployment-ready with systemd + Nginx
- ✅ Optional MySQL (RDS) integration via SQLAlchemy

---

## 📂 Project Structure

```
ssl-checker/
│── backend/ # FastAPI backend
│ ├── app/
│ │ ├── main.py  # FastAPI entrypoint
│ │ ├── db.py  # DB Config file
│ │ ├── __init__.py  # empty file
│ │ ├── models.py  # DB import
│ │ ├── setup_sslchecker.sh  #SSL Checker installation
│ │ └── ssl_checker.py  # Main app file
│ └── requirements.txt  # Requiered packages install
│
│── frontend/ # JS frontend
│ ├── app.js
│ └── index.html
│
└── README.md
```

## 🛠️ Installation (Manual)

### 1. Clone the repo
git clone https://github.com/GeorgiAndreev96/ssl-checker.git

cd backend

python3.11 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --host 0.0.0.0 --port 8000

cd frontend
npm install
npm run dev

## ⚙️ Deployment (Ubuntu + Nginx)

Copy backend to /opt/sslchecker/backend

Copy frontend build (npm run build) to /opt/sslchecker/frontend

Setup systemd service for backend:

```
[Unit]
Description=SSL Checker FastAPI
After=network.target

[Service]
User=root
WorkingDirectory=/opt/sslchecker/backend
ExecStart=/opt/sslchecker/backend/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

systemctl daemon-reload

systemctl enable sslchecker

systemctl start sslchecker

```
server {
    listen 80;
    server_name _;

    # Frontend
    location / {
        root /opt/sslchecker/frontend;
        index index.html;
        try_files $uri /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
systemctl restart nginx



## 📦 Environment Variables

If using a database:

Update /opt/sslchecker/backend/app/db.py:

DATABASE_URL=mysql+pymysql://<user>:<password>@<rds-endpoint>:3306/sslchecker




