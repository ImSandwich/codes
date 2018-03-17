import wptools
import re
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer as Summarizer 
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

LANGUAGE = "english"
SENTENCES_COUNT = 4

def search(name):
    try:
        
        page = wptools.page(name)
        data = page.get_restbase('/page/summary/').data['exhtml']
        tagsGram = re.compile('<.*?>')
        data_clean = re.sub(tagsGram, '', data)
    
    except LookupError:
        data_clean = "No information could be gathered regarding " + str(name) 
    
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    document = PlaintextParser.from_string(data_clean, Tokenizer(LANGUAGE))

    data_summarized = ""
    
    for sentence in summarizer(document.document, SENTENCES_COUNT):
        data_summarized += str(sentence) + " "
        

    return data_summarized

