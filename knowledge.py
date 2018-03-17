from chatterbot import ChatBot 
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import os

def teach(msg_array):
    chatbot.set_trainer(ListTrainer)
    chatbot.train(msg_array)

def ask(msg):
    global chatbot
    return chatbot.get_response(msg)

def update_database():
    file_writer = open("knowledgebase.txt", "w")
    knowledge_string = ''.join([x + "\n" for x in knowledgebase])
    file_writer.write(knowledgebase)
    file_writer.close()

knowledgebase = []
if os.path.isfile("knowledgebase.txt"):
    print("Knowledge base found")
    file_reader = open("knowledgebase.txt", "r")
    for line in file_reader.readlines():
        knowledgebase.append(line)
    file_reader.close()
else:
    update_database()
    

chatbot = ChatBot("Jeff2")
