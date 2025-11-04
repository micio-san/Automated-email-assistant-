import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
SMTP_SERVER=os.getenv("SMTP_SERVER")
SMTP_PORT=int(os.getenv("SMTP_PORT"))  
MAIL=os.getenv("MAIL")
PASSWORD=os.getenv("PASSWORD")


def send_answer(resp):
    pass