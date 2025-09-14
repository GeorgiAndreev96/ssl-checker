from sqlalchemy import Column, Integer, String, DateTime, Text
from .db import Base
import datetime

class CertCheck(Base):
    __tablename__ = "cert_checks"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), nullable=False, index=True)
    port = Column(Integer, default=443)
    expiry = Column(DateTime)
    last_checked = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), nullable=False)
    error_message = Column(Text, nullable=True)
