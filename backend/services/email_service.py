import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config.settings import settings

class EmailService:
    def send_report(self, to_email: str, file_path: str):
        try:
            msg = MIMEMultipart()
            msg['From'] = settings.EMAIL_ADDRESS
            msg['To'] = to_email
            msg['Subject'] = "Your Dental Health Analysis Report"
            
            body = """
            Dear Patient,

            Thank you for using our dental health analysis service.
            Your AI-generated report is attached to this email.

            Please remember this report is for educational purposes only.
            For a professional diagnosis, consult a qualified dentist.

            Sincerely,
            The Dental App Team
            """
            msg.attach(MIMEText(body, 'plain'))

            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= dental_report.pdf",
            )
            msg.attach(part)
            
            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
                server.sendmail(settings.EMAIL_ADDRESS, to_email, msg.as_string())

            print(f"Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False