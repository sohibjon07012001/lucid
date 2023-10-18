import smtplib
from email.mime.text import MIMEText

from config import EMAIL


class SEND_EMAIL:        

    def send_emaill(self, message, send_to, subject):
        msg = MIMEText(message, "html")
        msg['Subject'] = subject
        msg['From'] = "Verification Service | zypl.ai"
        msg['To'] = send_to
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            try:
                smtp_server.login(EMAIL.LOGIN, EMAIL.PASSWORD)
                smtp_server.send_message(msg)
            except Exception as ex:
                print("Cannot send message! Error: ", ex.__str__())
                return False
            else:
                return True