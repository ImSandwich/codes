from gensim import corpora, models, similarities
from nltk.corpus import stopwords
from collections import defaultdict
from pprint import pprint
import nltk
from nltk.tokenize import TreebankWordTokenizer
import string
import os
from similarity import is_ci_stem_stopword_set_match
os.chdir(os.path.dirname(__file__))
documents = open("lsi_data.txt", "r").read().splitlines()
stop_words = stopwords.words('english')
tokenizer = TreebankWordTokenizer()
word_list = [[x.lower() for x in tokenizer.tokenize(sentence) if (x not in stop_words and x not in string.punctuation)] for sentence in documents]
print(word_list)

frequency=defaultdict(int)
for sent in word_list:
    for token in sent:
        frequency[token] += 1

word_list = [[x for x in sent if frequency[x] > 1] for sent in word_list]
pprint(word_list)

dictionary = corpora.Dictionary(documents=word_list)

dictionary.save("LSA/doc1.dict")
print(dictionary.token2id)
corpus = [dictionary.doc2bow(sent) for sent in word_list]
corpora.MmCorpus.serialize("LSA/doc1.mm", corpus)

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
if (os.path.exists("LSA/doc1.index")):
    index = similarities.MatrixSimilarity.load("LSA/doc1.index")
else:
    index = similarities.MatrixSimilarity(lsi[corpus])
    index.save("LSA/doc1.index")

while True:
    user_input = input("Q: ")
    vec_bow = dictionary.doc2bow([x.lower() for x in tokenizer.tokenize(user_input)])
    vec_lsi = lsi[vec_bow]
    sims = index[vec_lsi]
    sims = [(x[0], x[1] * is_ci_stem_stopword_set_match(user_input, documents[x[0]])) for x in enumerate(sims)]
    sims = sorted(sims, key=lambda x:abs(x[1]), reverse=True)
    sims = sims[:1]
    sims = [documents[x[0]] for x in sims]
    for sim in sims:
        pprint("A: " + sim)