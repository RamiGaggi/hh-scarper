
from string import digits, punctuation, whitespace

from nltk.corpus import stopwords
from pymystem3 import Mystem

stem = Mystem()
STOP_TOKENS = (
    *stopwords.words('russian'),
    *['д', 'т'],
    *stopwords.words('english'),
    *list(punctuation),
    *['),', ');', '–', '—', '://'],
    *list(whitespace),
    *[''],
    *list(digits),
)


def preprocess_text(text):
    tokens = stem.lemmatize(text)
    return {token.upper() for token in tokens if (token not in STOP_TOKENS and token.strip() not in STOP_TOKENS)}  # noqa: WPS221, E501
