from dotenv import load_dotenv
import os 
from mistralai import Mistral, SDKError
from Logging.logger import logger
import json 
from ErrorAI import ServiceTier
from json import JSONDecodeError
import traceback

load_dotenv()

SDK_KEY = os.getenv("SDK_KEY")
client= Mistral(api_key=SDK_KEY)

def mail_summary(mail):
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
       content = chat_response.choices[0].message.content
       json_str = content.strip("```json").strip("```").strip()
       data = json.loads(json_str)
       print(data)
       return data, mail["sender"]
    except JSONDecodeError as err:
        logger.error("Invalid JSON returned by AI")
        logger.error(f"Raw output: {content}")
        raise ServiceTier("AI returned malformed JSON") from err

    except SDKError as err:
        logger.error(f"Mistral SDK Error: {err.body}")
        raise ServiceTier(f"Mistral SDK Error: {err.body}")

    except Exception as e:
        traceback.print_exc()
        logger.error(f"Unexpected error: {e}")
        raise ServiceTier(f"Unexpected error during mail analysis: {e}")