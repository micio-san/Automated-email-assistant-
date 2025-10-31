from Logging.logger import logger
from email_reader import fetch_unread_emails
from emailSummarize import analyze_mail

emails=fetch_unread_emails()
latest = fetch_unread_emails(False)
print(emails)

def main():
    logger.info("start")
    try: 
      for mail in emails:
        resp=  analyze_mail(mail)
        print(resp)
    except Exception as e:
      print(e)

if __name__ == "__main__":
    main()