import schedule
import time
from Logging.logger import logger
from email_reader import fetch_unread_emails
from email_summary import mail_summary
from action_routes import action_router


def main():
    emails=fetch_unread_emails()
   # latest = fetch_unread_emails(False)
    logger.info("start")
    try: 
      # for mail in emails:
      resp, sender = mail_summary(emails[0])
      if "error" not in resp:
        action_router(resp, sender, emails[0])
    except Exception as e:
       logger.critical(f"generic err: {e}")

schedule.every(5).minutes.do(main)

while True:
   schedule.run_pending()
   time.sleep(1)
# if __name__ == "__main__":
#     main()