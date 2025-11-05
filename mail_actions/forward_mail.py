import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Logging.logger import logger
from dotenv import load_dotenv

load_dotenv()
SMTP_SERVER=os.getenv("SMTP_SERVER")
SMTP_PORT=int(os.getenv("SMTP_PORT"))  
MAIL=os.getenv("MAIL")
PASSWORD=os.getenv("PASSWORD")

def forward_mail(aisummary, forward_addy, og_mail):
    logger.info("into forward mails")
    msg = MIMEMultipart()
    msg["From"]= og_mail["sender"]
    msg["To"]=forward_addy
    msg["Subject"]= f"FWD: {aisummary["intent"]}"
    body = f"Forwarded message:\n\nFrom: { og_mail["sender"]}\n\n{og_mail['body']}"
    msg.attach(MIMEText(body, "plain"))
    try:
     with smtplib.SMTP(host=SMTP_SERVER,port=SMTP_PORT, timeout=1000) as server:
         server.starttls()
         server.login(MAIL, PASSWORD)
         server.send_message(msg)
         print(f"Forwarded to {forward_addy} originally sent by {og_mail["sender"]}")
    except Exception as e:
       logger.error(f"Failure is sending to {forward_addy} (?saving somewhere for scheduled op later??)")