import os
from dotenv import load_dotenv
import imaplib, email
from email.header import decode_header
from Logging.logger import logger

load_dotenv()
username = os.getenv("MAIL")
pwd = os.getenv("PASSWORD")
server = os.getenv("SERVER")
port = int(os.getenv("PORT"))

def fetch_unread_emails(single=True):
    logger.critical("Starting connection with IMAP server")
    try:
        conn = imaplib.IMAP4_SSL(server, port)
        conn.login(username, pwd)
        logger.info("Auth OK, selecting inbox for unread mails")
        conn.select("INBOX")

        typ, msgnums = conn.uid('search', None, 'SEEN')
        allmails = []

        for num in msgnums[0].split():
            result, msg_data = conn.uid('fetch', num, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            # Decode subject properly
            subject, encoding = decode_header(msg["subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            full_mail = {
                "uid":num.decode(),
                "sender": msg["from"],
                "subject": subject,
                "body": None,
                "date": msg["date"],
            }
            body = None
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_dispo = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_dispo:
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")
                full_mail["body"] = body
            allmails.append(full_mail)

            if single:
                break  # Fetch only the first unread mail if requested
        conn.logout()
        return allmails

    except ConnectionError as e:
        logger.critical(f"Connection error: {e}")
    except Exception as err:
        logger.error(f"Unexpected error: {err}")
    finally:
        try:
            conn.close()
            conn.logout()
        except:
            pass
