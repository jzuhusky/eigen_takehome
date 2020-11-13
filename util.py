import errno
import logging
import string
import os

from nltk.tokenize import word_tokenize, sent_tokenize


logger = logging.getLogger(__name__)


def lower_text(text):
    return text.lower()


def remove_punctuation(text):
    return "".join([c for c in text if c not in string.punctuation])


def get_sentences(text):
    return sent_tokenize(text)


def word_tokenize_text(text):
    return word_tokenize(text)


def preprocess_text(text):
    """Preprocess text into tokenized sentences"""
    text = lower_text(text)
    sentences = get_sentences(text)
    sentences = [remove_punctuation(sent) for sent in sentences]
    tok_sentences = [word_tokenize_text(sent) for sent in sentences]
    return tok_sentences


def make_dir_if_not_exists(filename):
    """Make the entire path to this file if some directories don't exist"""
    if not os.path.exists(os.path.dirname(filename)):
        logger.info("File path: %s doesn't exist, creating necessary dirs", filename)
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def get_files_to_parse():
    """Get all absolute file paths for every file in the ./docs/ dir"""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    docs_dir = os.path.join(current_dir, "docs")
    return [os.path.join(docs_dir, fname) for fname in os.listdir(docs_dir)]
