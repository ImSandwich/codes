import time
import os
import pickle

from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message
from thesaurus_machine import fancy_synonyms
from wikipedia_custom import search
from datetime import datetime
from dateutil.parser import parser
from knowledge import ask, teach

driver = WhatsAPIDriver(client="Chrome")
print("Waiting for QR")
driver.wait_for_login()

print("Bot started")


threshold = 0

if os.path.isfile("reminder.pickle"):
    print("Reminder file found")
    file_reader = open("reminder.pickle","rb")
    reminder_array = pickle.load(file_reader)
    file_reader.close()
else:
    reminder_array = []
    file_writer = open("reminder.pickle","wb")
    pickle.dump(reminder_array,file_writer)
    file_writer.close()

while True:
    time.sleep(1)
    if threshold > 0:
        threshold -= 1
    if threshold < 0:
        threshold = 0

    
    for i in range(len(reminder_array)-1, -1, -1):   
        t, msg, contact_name = reminder_array[i]
        if datetime.now() >= t:
            for contact in driver.get_all_chats():
                if contact_name == contact.name:
                    contact.send_message(msg)
                    del reminder_array[i]
        


    print('Checking for more messages')
    for contact in driver.get_unread(include_me=True):
        for message in contact.messages:
            if isinstance(message, Message): # Currently works for text messages only.
                print(str(message.safe_content))
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
                    msg = message_safe[9:]
                    reply = fancy_synonyms(msg.lower())
                    contact.chat.send_message(reply)
                    triggered = True
                elif ("/help" == message_safe[:5]):
                    help_file = open("help.txt", "r")
                    contact.chat.send_message(help_file.read())
                    help_file.close()
                elif ("/whatis" == message_safe[:7]):
                    print("ASK triggered")
                    msg = message_safe[8:]
                    contact.chat.send_message(search(msg))
                    triggered = True
                elif ("/remind" == message_safe[:7]):
                    arguments = message_safe[8:].split(' ')
                    custom_parser = parser()
                    _time = custom_parser.parse(arguments[0])
                    msg = "*Reminder for {}*: {}".format(str(message.sender.short_name),arguments[1])
                    contact.chat.send_message("Msg {} set for {}".format(msg, _time))
                    reminder_array.append((_time,msg, str(contact.chat.name)))
                    file_writer = open("reminder.pickle","wb")
                    pickle.dump(reminder_array,file_writer)
                    file_writer.close()
                    triggered = True   

                elif ("/teach" == message_safe[:6]):
                    contact.chat.send_message("Jeff: I have learned to speak better by analyzing contents of this conversation")
                    msg_array = []
                    for msg in driver.get_all_messages_in_chat(contact.chat, include_me=True):
                        if (isinstance(msg, Message)):
                            try:
                                msg_array.append(str(msg.safe_content))
                            except Exception:
                                pass 
                                
                    teach(msg_array)
                    triggered = True

                elif ("/jeff" == message_safe[:5]):
                    msg = message_safe[6:]
                    reply = "*Jeff* to {}*: {}".format(str(message.sender.short_name), str(ask(msg)))
                    contact.chat.send_message(reply)
                    triggered = True


                if (triggered):
                    threshold += 8
                if threshold >= 32:
                    contact.chat.send_message("*Jeff* gonna take a 30s break.")
                    threshold = 64
                    

                
                    
                
                    


#https://github.com/mukulhase/WebWhatsAPI