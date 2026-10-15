import os
import json
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_EMAIL = os.getenv("SMTP_EMAIL", os.getenv("SMTP_USER", "chaudharidevanshu1912@gmail.com"))
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", os.getenv("SMTP_PASS", ""))

def send_email_otp(to_email: str, otp_code: str, user_name: str = "Valued Customer") -> dict:
    """
    Dispatches Email OTP using PHP Mailer first (as requested by user),
    with Python smtplib fallback.
    Returns dict with success status, method, and message.
    """
    subject = f"VisionEdge - Your Login Verification Code is {otp_code}"
    
    # 1. Attempt using PHP Mailer
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        php_script = os.path.join(base_dir, 'utils', 'php_mailer.php')
        
        if os.path.exists(php_script):
            proc = subprocess.run(
                ['php', php_script, to_email, subject, otp_code, user_name],
                capture_output=True,
                text=True,
                timeout=12,
                cwd=base_dir
            )
            if proc.returncode == 0 and proc.stdout.strip():
                try:
                    res = json.loads(proc.stdout.strip())
                    if res.get('success'):
                        return {
                            "success": True,
                            "method": "php_mailer",
                            "message": "OTP delivered via PHP Mailer"
                        }
                except Exception:
                    pass
    except Exception as e:
        print(f"[PHP Mailer Notice] {e}")

    # 2. Attempt using Python smtplib if credentials configured
    if SMTP_PASSWORD and not SMTP_PASSWORD.startswith("your_"):
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"VisionEdge Eyewear <{SMTP_EMAIL}>"
            msg["To"] = to_email

            html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background: #f8fafc; padding: 24px; margin: 0;">
                <div style="max-width: 500px; margin: auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden;">
                    <div style="background: #0d6efd; color: #fff; padding: 24px; text-align: center;">
                        <h2 style="margin: 0;">VisionEdge</h2>
                        <p style="margin: 4px 0 0; opacity: 0.85;">Login Verification</p>
                    </div>
                    <div style="padding: 24px;">
                        <p>Hello <strong>{user_name}</strong>,</p>
                        <p>Your one-time login verification code is:</p>
                        <div style="text-align: center; margin: 24px 0;">
                            <span style="font-size: 32px; font-weight: bold; letter-spacing: 6px; color: #0d6efd; background: #f1f5f9; padding: 10px 24px; border-radius: 8px; border: 1px dashed #0d6efd;">{otp_code}</span>
                        </div>
                        <p style="font-size: 13px; color: #64748b;">This code will expire in 10 minutes. If you did not make this request, you can safely ignore this email.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            msg.attach(MIMEText(html, "html"))

            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
            if SMTP_PORT == 587:
                server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, [to_email], msg.as_string())
            server.quit()

            return {
                "success": True,
                "method": "smtp_python",
                "message": "OTP delivered via SMTP"
            }
        except Exception as e:
            print(f"[Python SMTP Notice] {e}")

    # 3. Attempt FormSubmit direct web relay
    try:
        import requests
        fs_res = requests.post(
            f"https://formsubmit.co/ajax/{to_email}",
            json={
                "name": "VisionEdge Eyewear",
                "_subject": f"VisionEdge Verification Code: {otp_code}",
                "verification_code": otp_code,
                "message": f"Hello {user_name}, your VisionEdge login verification code is {otp_code}. This code is valid for 10 minutes."
            },
            headers={
                "Referer": "http://localhost:8000/login.html",
                "User-Agent": "Mozilla/5.0"
            },
            timeout=8
        )
        if fs_res.status_code == 200 and fs_res.json().get("success") == "true":
            return {
                "success": True,
                "method": "formsubmit",
                "message": "OTP delivered via FormSubmit relay"
            }
    except Exception as e:
        print(f"[FormSubmit Notice] {e}")

    # Fallback to dev mode if no credentials configured yet
    return {
        "success": False,
        "method": "dev_mode",
        "message": "SMTP not configured; code provided via dev response"
    }
