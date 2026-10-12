import json
from config import CONTACTS_FILE
import pywhatkit
def send_whatsapp(contact_name,message):
    try: contacts=json.loads(CONTACTS_FILE.read_text(encoding="utf-8"))
    except Exception as e: print("CONTACT ERROR:",e); return False
    phone=next((n for name,n in contacts.items() if name.lower()==contact_name.lower()),None)
    if not phone: print("Contact not found."); return False
    try:
        pywhatkit.sendwhatmsg_instantly(phone,message,wait_time=15,tab_close=True); return True
    except Exception as e: print("WHATSAPP ERROR:",e); return False
