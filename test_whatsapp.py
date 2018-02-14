import time
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message
from thesaurus_machine import fancy_synonyms

threshold = 0
driver = WhatsAPIDriver(client="Chrome")
print("Waiting for QR")
driver.wait_for_login()

print("Bot started")

while True:
    time.sleep(1)
    if threshold > 0:
        threshold -= 1
    if threshold < 0:
        threshold = 0

    print('Checking for more messages')
    for contact in driver.get_unread(include_me=True):
        for message in contact.messages:
            if isinstance(message, Message): # Currently works for text messages only.
                if (threshold >= 32):
                    break

                message_safe = str(message.safe_content)
                triggered = False

                if ("/echo" == message_safe[:5]):
                    msg = message_safe[6:]
                    contact.chat.send_message(msg)
                    triggered = True
                elif ("/sleep" == message_safe[:6]):
                    contact.chat.send_message("Okay. zzz")
                    quit()
                elif ("/fancify" == message_safe[:8]):
                    print("Fancify triggered")
                    msg = message_safe[9:]
                    reply = fancy_synonyms(msg)
                    contact.chat.send_message(reply)
                    triggered = True
                
                if (triggered):
                    threshold += 8
                    if threshold >= 32:
                        contact.chat.send_message("Bot gonna take a 30s break.")
                        threshold = 64
                    
                
                    


#https://github.com/mukulhase/WebWhatsAPI