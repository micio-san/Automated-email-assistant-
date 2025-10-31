from dotenv import load_dotenv
from openai import OpenAI
from Logging.logger import logger
import os

load_dotenv()

OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
client= OpenAI(api_key=OPEN_AI_KEY)

def analyze_mail(mail):
    logger.info("calling open ai")
    print()
    prompt=f"""
      You are an intelligent email assistant.
    Analyze the following email and respond in JSON format with:
    - "summary": a short summary of the email
    - "intent": one of ["meeting_request", "support_request", "complaint", "newsletter", "personal", "spam", "other"]
    - "needs_reply": true or false
    - "suggested_reply": a short, polite draft if a reply is needed
     Email sender: ${mail.sender}
     Email subject: ${mail.subject},
     Email body: ${mail.body}
"""
    try:
        response= client.chat.completions.create(
            model='gpt-5',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        result_text=response.choices[0].message.content
        logger.info(result_text)
    except Exception as err:
        print(err)
     
    return result_text
