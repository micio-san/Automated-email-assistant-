import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from Logging.logger import logger

load_dotenv()
SMTP_SERVER=os.getenv("SMTP_SERVER")
SMTP_PORT=int(os.getenv("SMTP_PORT"))  
MAIL=os.getenv("MAIL")
PASSWORD=os.getenv("PASSWORD")


def send_answer(resp, sender):
    print(f"ass{resp} || {sender}")
    msg = MIMEMultipart()
    msg["From"]=MAIL
    msg["To"]= sender
    msg["Subject"]= f"Re: {resp["intent"]}"
    msg.attach(MIMEText(resp["suggested_reply"], "plain"))
    try:
        #open server
        with smtplib.SMTP(host=SMTP_SERVER,port=SMTP_PORT,timeout=1000) as server:
            #Puts the connection to the SMTP server into TLS mode.
            server.starttls()
            server.login(MAIL, PASSWORD)
            server.send_message(msg)
            logger.info(f"OK!! mail sent with txt {msg}")
    except Exception as err:
        logger.error(err)
