import nltk.corpus
import nltk.tokenize
from nltk.stem.snowball import SnowballStemmer
import string

# Get default English stopwords and extend with punctuation
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)
stopwords.append('')

# Create tokenizer and stemmer
stemmer = SnowballStemmer('english')

def is_ci_stem_stopword_set_match(a, b):
    """Check if a and b are matches."""
    tokens_a = [token.lower().strip(string.punctuation) for token in nltk.word_tokenize(a) \
                    if token.lower().strip(string.punctuation) not in stopwords]
    tokens_b = [token.lower().strip(string.punctuation) for token in nltk.word_tokenize(b) \
                    if token.lower().strip(string.punctuation) not in stopwords]
    stems_a = [stemmer.stem(token) for token in tokens_a]
    stems_b = [stemmer.stem(token) for token in tokens_b]

    # Calculate Jaccard similarity
    ratio = len(set(stems_a).intersection(stems_b)) / float(len(set(stems_a).union(stems_b)))
    return ratio
