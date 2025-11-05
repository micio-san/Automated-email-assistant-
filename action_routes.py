import os   
from Logging.logger import logger
from dotenv import load_dotenv
from mail_actions.forward_mail import forward_mail
from mail_actions.email_writer import send_answer
from mail_actions.move_folder import move_mail

load_dotenv()
SUPPORT_MAIL=os.getenv("SUPPORT_MAIL")
MANAGER_MAIL=os.getenv("MANAGER_MAIL")

def action_router(ai_summary, sender, original_mail):
    logger.info("into routing file")
    #- "intent": one of ["meeting_request", "support_request", "complaint", "newsletter", "personal", "spam", "other"]
    why=ai_summary.get("intent")
    logger.info(f"{sender} || {why}")
    """ai summaty summary || intent' || 'needs_reply' ||'suggested_reply'}
       sender
       ogmail sender subject  body date"""
    match why:
        case "meeting_request" | "personal":
            send_answer(ai_summary, sender) if ai_summary.get("needs_reply") else logger.info(f"no need reply from {sender} ")
        case "support_request":
            forward_mail(ai_summary, SUPPORT_MAIL, original_mail)
        case  "complaint":
            forward_mail(ai_summary, MANAGER_MAIL, original_mail)
        case "newsletter"  | "spam":
            move_mail(original_mail["uid"], why)
        case _:
            pass