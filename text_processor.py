import re
import nltk

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

def clean_text(text):
    """
    Clean and normalize sales-call notes.
    """

    # Convert text to lowercase
    text = text.lower()

    # Remove unnecessary characters
    text = re.sub(r"[^a-zA-Z0-9\s.,!?]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove spaces from the beginning and end
    text = text.strip()

    return text


def process_text(text):
    """
    Clean the text and perform sentence and word tokenization.
    """

    # First clean the text
    cleaned_text = clean_text(text)

    # Split text into sentences
    sentences = nltk.sent_tokenize(cleaned_text)

    # Split text into words
    words = nltk.word_tokenize(cleaned_text)

    return cleaned_text, sentences, words
