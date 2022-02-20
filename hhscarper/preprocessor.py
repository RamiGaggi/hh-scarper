from string import digits, punctuation, whitespace

from bs4 import BeautifulSoup
from django.conf import settings
from nltk.corpus import stopwords
from pymystem3 import Mystem

stem = Mystem(mystem_bin=settings.BASE_DIR / 'mystem')

STOP_TOKENS = (
    *stopwords.words('russian'),
    *['д', 'т'],
    *stopwords.words('english'),
    *list(whitespace),
    *[''],
    *list(digits),
)


def clean_text(text):
    if not text:
        return ''
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()


def preprocess_text(text):  # noqa: WPS231
    if not text:
        return ''
    tokens = stem.lemmatize(text)
    res = set()
    flag = True

    for token in tokens:
        for sym in (*punctuation, *['—', '–', '·', '»', '«']):
            if sym in token.strip():
                flag = False
                break

        if flag and (token not in STOP_TOKENS and token.strip() not in STOP_TOKENS):  # noqa: WPS221, E501
            res.add(token.upper())
        flag = True

    return list(res)
