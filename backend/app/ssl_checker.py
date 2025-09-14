import ssl
import socket
import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def check_ssl_cert(hostname: str, port: int = 443):
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    conn.settimeout(5.0)

    try:
        conn.connect((hostname, port))
        cert_bin = conn.getpeercert(True)
        cert = x509.load_der_x509_certificate(cert_bin, default_backend())
        expiry = cert.not_valid_after
        valid_from = cert.not_valid_before
        conn.close()
        return {
            "expiry": expiry,
            "valid_from": valid_from,
            "status": "valid",
            "error_message": None,
        }
    except Exception as e:
        return {
            "expiry": None,
            "valid_from": None,
            "status": "error",
            "error_message": str(e),
        }
