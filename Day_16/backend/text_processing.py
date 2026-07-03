import re
import string
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def clean_text(text):

    # Handle None values
    if text is None:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Split sentence into words
    words = text.split()

    # Remove stopwords
    filtered_words = [
        word for word in words
        if word not in stop_words
    ]

    # Join back into sentence
    cleaned_text = " ".join(filtered_words)

    return cleaned_text

if __name__ == "__main__":

    sample = """
    OpenAI launches GPT-5 in 2025!
    It is one of the most powerful AI models.
    """

    print(clean_text(sample))