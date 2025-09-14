from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import db, models, ssl_checker
import datetime

# Create tables if they don't exist
models.Base.metadata.create_all(bind=db.engine)

app = FastAPI(title="SSL Checker API")

class CheckRequest(BaseModel):
    url: str

@app.post("/check")
def check_cert(request: CheckRequest):
    hostname = request.url.replace("http://", "").replace("https://", "").split("/")[0]
    result = ssl_checker.check_ssl_cert(hostname)

    session: Session = db.SessionLocal()
    cert_check = models.CertCheck(
        domain=hostname,
        expiry=result["expiry"],
        last_checked=datetime.datetime.utcnow(),
        status=result["status"],
        error_message=result["error_message"],
    )
    session.add(cert_check)
    session.commit()
    session.refresh(cert_check)
    session.close()

    return {
        "id": cert_check.id,
        "domain": cert_check.domain,
        "expiry": cert_check.expiry,
        "status": cert_check.status,
        "error": cert_check.error_message,
    }


@app.get("/domains")
def list_domains():
    session: Session = db.SessionLocal()
    rows = session.query(models.CertCheck).order_by(models.CertCheck.expiry.asc()).all()
    session.close()
    return [
        {
            "id": row.id,
            "domain": row.domain,
            "expiry": row.expiry,
            "status": row.status,
        }
        for row in rows
    ]
