
from string import digits, punctuation, whitespace

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from pymystem3 import Mystem

stem = Mystem()
another_symbols = [  # noqa: WPS317
    '),', ');', '–', '—', '://', '); ', '.); ',
]
tags = ['li', 'ul', 'p', 'strong']

STOP_TOKENS = (
    *stopwords.words('russian'),
    *['д', 'т'],
    *stopwords.words('english'),
    *list(punctuation),
    *list(whitespace),
    *[''],
    *list(digits),
    *tags,
    *another_symbols,
)


def clean_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()


def preprocess_text(text):
    tokens = stem.lemmatize(text)
    return {token.upper() for token in tokens if (token not in STOP_TOKENS and token.strip() not in STOP_TOKENS)}  # noqa: WPS221, E501
