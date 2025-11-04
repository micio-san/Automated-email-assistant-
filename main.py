from Logging.logger import logger
from email_reader import fetch_unread_emails
from email_summary import mail_support
from email_writer import send_answer

emails=fetch_unread_emails()
latest = fetch_unread_emails(False)
print(emails)

def main():
    logger.info("start")
    try: 
      print("qua arrivo")
      # for mail in emails:
      resp= mail_support(emails[0])
      if "error" not in resp and resp.needs_repl == True:
        send_answer(resp)
    except Exception as e:
       logger.critical(f"generic err: {e}")
 

if __name__ == "__main__":
    main()