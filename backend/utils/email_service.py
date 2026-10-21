"""
VisionEdge — Email Service Helper
==================================
General notification email service (optional).
Authentication no longer requires OTP or email verification.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_EMAIL = os.getenv("SMTP_EMAIL", os.getenv("SMTP_USER", ""))
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", os.getenv("SMTP_PASS", ""))

def send_notification_email(to_email: str, subject: str, message_body: str) -> bool:
    """
    Sends a general notification email using SMTP if configured.
    Returns True if sent, False otherwise.
    """
    if not SMTP_PASSWORD or not SMTP_EMAIL:
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"VisionEdge Eyewear <{SMTP_EMAIL}>"
        msg["To"] = to_email

        part = MIMEText(message_body, "html")
        msg.attach(part)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"[Email Service Notice] Could not deliver email: {e}")
        return False
