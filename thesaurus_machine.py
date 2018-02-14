import nltk
import random
import string
from nltk.corpus import wordnet as wn

def fancy_antonyms(sentence):
    words = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)
    output = ""
    for i in range(len(words)):
        dispense = ""        
        word = words[i]
        pos = pos_tags[i]
        wn_pos = None
        if 'NN' in pos:
            wn_pos = wn.NOUN
        elif 'VB' in pos:
            wn_pos = wn.VERB
        elif 'RB' in pos:
            wn_pos = wn.ADV
        elif 'JJ' in pos:
            wn_pos = wn.ADJ
        if (wn_pos != None):
            synsets = wn.synsets(word,wn_pos)
            ant_array = []
            for ss in synsets:
                for l in ss.lemmas():
                    for a in l.antonyms():
                        ant_array.append(a.name())
            ant_array = list(set(ant_array))
            if (len(ant_array) == 0):
                dispense = word
            else:
                dispense = random.choice(ant_array)
        else:
            dispense = word
        if (dispense in string.punctuation):
            output += dispense
        else:
            output += " " + dispense
    return output


def fancy_synonyms(sentence):
    words = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)
    output = ""
    for i in range(len(words)):
        dispense = ""        
        word = words[i]
        pos = pos_tags[i]
        wn_pos = None
        if 'NN' in pos:
            wn_pos = wn.NOUN
        elif 'VB' in pos:
            wn_pos = wn.VERB
        elif 'RB' in pos:
            wn_pos = wn.ADV
        elif 'JJ' in pos:
            wn_pos = wn.ADJ
        if (wn_pos != None):
            synsets = wn.synsets(word,wn_pos)
            syn_array = []
            for ss in synsets:
                syn_array.append(ss.lemmas()[0].name())
                for synonyms in ss.similar_tos():
                    syn_array.append(synonyms.lemmas()[0].name())
            syn_array = list(set(syn_array))
            if word in syn_array and len(syn_array) > 1:
                syn_array.remove(word)
                dispense = random.choice(syn_array)
            elif(len(syn_array)==0):
                dispense = word
            else:
                dispense = random.choice(syn_array)
                

        else:
            dispense = word
        if (dispense in string.punctuation):
            output += dispense
        else:
            output += " " + dispense
    return output

