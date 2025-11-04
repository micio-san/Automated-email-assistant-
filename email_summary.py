from dotenv import load_dotenv
import os 
from mistralai import Mistral, SDKError
from Logging.logger import logger
import json 
from ErrorAI import ServiceTier

load_dotenv

SDK_KEY = os.getenv("SDK_KEY")
client= Mistral(api_key=SDK_KEY)

def mail_support(mail):
    logger.info("Start calling ai")
    try:
       prompt=f"""
         You are an intelligent email assistant.
       Analyze the following email and respond in JSON format with:
       - "summary": a short summary of the email
       - "intent": one of ["meeting_request", "support_request", "complaint", "newsletter", "personal", "spam", "other"]
       - "needs_reply": true or false
       - "suggested_reply": a short, polite draft if a reply is needed
        Email sender: {mail["sender"]}
        Email subject: {mail["subject"]},
        Email body: {mail["body"]},
       """
       chat_response = client.chat.complete(
           model="mistral-small-latest",
           messages=[{"role": "user", "content": prompt}]
       )
       json_str = chat_response.strip('```json\n').strip('\n```')
       data = json.loads(json_str)
       return data
    except AttributeError as err:
        print("nasta")
        logger.error(f"{e}")
        return err
    except SDKError as err:
        logger.error(f"{err.body}")
        return err
    except Exception as e:
        import traceback
        traceback.print_exc()
        return e
