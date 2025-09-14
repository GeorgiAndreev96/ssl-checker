# 🔒 SSL Checker

A simple **SSL certificate checker** with a FastAPI backend and a React frontend.  
It allows you to check SSL/TLS expiration and details for any domain.

---

## 🚀 Features
- ✅ Check SSL certificate validity for a given domain
- ✅ View expiry date, issuer, and validity period
- ✅ REST API built with FastAPI
- ✅ Frontend built with React (served by Nginx)
- ✅ Deployment-ready with systemd + Nginx
- ✅ Optional MySQL (RDS) integration via SQLAlchemy

---

## 📂 Project Structure

ssl-checker/
│── backend/ # FastAPI backend
│ ├── app/
│ │ ├── main.py # FastAPI entrypoint
│ │ ├── routes/ # API routes
│ │ └── services/ # SSL logic
│ ├── requirements.txt
│ └── setup_sslchecker.sh
│
│── frontend/ # React frontend (Vite)
│ ├── src/
│ ├── public/
│ └── package.json
│
└── README.md


## 🛠️ Installation (Manual)

### 1. Clone the repo
```bash
git clone https://github.com/GeorgiAndreev96/ssl-checker.git
cd ssl-checker

cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000

cd frontend
npm install
npm run dev
```
⚙️ Deployment (Ubuntu + Nginx)

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
📦 Environment Variables
If using a database (optional):

env
Copy code
DATABASE_URL=mysql+pymysql://<user>:<password>@<rds-endpoint>:3306/sslchecker




