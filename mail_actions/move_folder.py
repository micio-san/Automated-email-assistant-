import imaplib
import os
from dotenv import load_dotenv
from Logging.logger import logger

load_dotenv()
SERVER=os.getenv("SERVER")
PORT=int(os.getenv("PORT"))  
MAIL=os.getenv("MAIL")
PASSWORD=os.getenv("PASSWORD")

def move_mail(email_uid, label_name):
    """
    Moves an email from INBOX to another folder/label using IMAP COPY + DELETE.
    Automatically creates the folder if it doesn't exist.
    """
    try:
        conn = imaplib.IMAP4_SSL(SERVER)
        conn.login(MAIL, PASSWORD)
        conn.select("INBOX")

        # check folder exists
        result, folders = conn.list()
        folder_exists = any(label_name.encode() in f for f in folders or [])

        if not folder_exists:
            #creates
            logger.warning(f"Folder '{label_name}' not found. Creating it...")
            create_res = conn.create(label_name)
            if create_res[0] != "OK":
                logger.error(f"Failed to create folder '{label_name}': {create_res}")
                conn.logout()
                return False
            else:
                logger.info(f"✅ Created folder '{label_name}'")

        #  copy  email
        logger.info(f"Copying email UID {email_uid} to {label_name}")
        result = conn.uid('copy', email_uid, label_name)
        if result[0] != "OK":
            logger.error(f"Failed to copy email {email_uid} to {label_name}: {result}")
            conn.logout()
            return False

        # deleted og
        conn.uid('store', email_uid, '+FLAGS', '\\Deleted')

        # remove deleted msgs
        conn.expunge()
        conn.logout()
        logger.info(f"✅ Moved email UID {email_uid} to {label_name}")
        return True

    except Exception as e:
        logger.error(f"Unexpected error while moving email: {e}")
        return False
