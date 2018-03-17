#Goal: Create word vectors froma game of thrones dataset
#and analyze them to see Semantic Similarity 

from __future__ import absolute_import, division, print_function
#for word encoding
import codecs
#regex
import glob 
import multiprocessing
import os
import pprint
import re 
import nltk
from nltk.tokenize import PunktSentenceTokenizer
import gensim.models.word2vec as w2v 
import sklearn.manifold
import numpy as np 
import matplotlib.pyplot as plt  
import pandas as pd 
import seaborn as sns 

#clean data 
os.chdir(os.path.join(os.path.dirname(__file__), "hp"))
book_filenames = sorted(glob.glob("*.txt"))
print(book_filenames)

corpus_raw = "" #A utf-8 corpus
for book_filename in book_filenames:
    print("Reading '{0}' ...".format(book_filename))
    
    with codecs.open(book_filename, "r", "utf-8", errors="ignore") as book_file:
        corpus_raw += book_file.read()
    print("Corpus is now {0} characters long".format(len(corpus_raw)))
    print()

ps = PunktSentenceTokenizer()
raw_sentences = ps.tokenize(corpus_raw)

def sentence_to_wordlist(raw):
    clean = re.sub("[^a-zA-Z]", " ", raw)
    words = clean.split()
    return words 

sentences = []
for raw_sentence in raw_sentences:
    if (len(raw_sentence)>0):
        sentences.append(sentence_to_wordlist(raw_sentence))

# word_count = sum([len(x) for x in sentences])
# print("There are a total of {0} tokens".format(word_count))

#Word2Vec
num_features = 500
min_word_count = 3
num_workers = multiprocessing.cpu_count()
context_size = 7
downsampling = 1e-3
seed = 2
thrones2vec = w2v.Word2Vec(
        seed = seed,
        sg=1,
        workers=num_workers,
        size=num_features,
        min_count=min_word_count,
        window=context_size,
        sample=downsampling
    )

    
def prepare_vec():
    global thrones2vec
    
    thrones2vec.build_vocab(sentences)

    print("Word2Vec vocabulary length:", len(thrones2vec.wv.vocab))
    thrones2vec.train(sentences, total_examples=thrones2vec.corpus_count, epochs=thrones2vec.epochs)

    if not os.path.exists("trained"):
        os.makedirs("trained")
    thrones2vec.save(os.path.join("trained", "potter2vec.w2v"))

if os.path.exists(os.path.join("trained", "potter2vec.w2v")):
    thrones2vec = w2v.Word2Vec.load(os.path.join("trained", "potter2vec.w2v"))
else:
    prepare_vec()

def find_relationship(start1, end1, end2):
    similarities = thrones2vec.most_similar_cosmul(
        positive=[end2, start1],
        negative=[end1]
    )
    start2 = similarities[0][0]
    print("{0} is related to {1}, as {2} is related to {3}".format(start1, end1, start2, end2))

def whatis(token):
    print(thrones2vec.most_similar(token))
    
while True:
    try:
        eval(input("Your command: "))
    except:
        pass
# tsne = sklearn.manifold.TSNE(n_components=2, random_state=0)
# all_word_vectors_matrix = thrones2vec.wv.syn0

# all_word_vectors_matrix_2d = tsne.fit_transform(all_word_vectors_matrix)

# points = pd.DataFrame(
#     [
#         (word, coords[0], coords[1])
#         for word, coords in [
#             (word, all_word_vectors_matrix_2d[thrones2vec.wv.vocab[word]])
#             for word in thrones2vec.wv.vocab]
#     ]
# )
# sns.set_context("poster")
# points.plot.scatter("x", "y", s=10, figsize=(20,12))

# def plot_region(x_bounds, y_bounds):
#     slice = points[
#         (x_bounds[0] <= points.x) &
#         (points.x <= x_bounds[1]) &
#         (y_bounds[0] <= points.y) &
#         (points.y <= y_bounds[1])
#     ]
#     ax = slice.plot.scatter("x", "y", s=35, figsize=(10,8))
#     for i, point in slice.interrows():
#         ax.text(point.x + 0.005, point.y+0.005, point.word, fontsize=11)
    
# plot_region(x_bounds=(4.0,4.2), y_bounds=(-0.5, -0.1))
