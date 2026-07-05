from sklearn.feature_extraction.text import TfidfVectorizer

import re

def extract_keywords(text, top_n=5):

    if not text:
        return ""

    # Find capitalized words (company names, people, places, etc.)
    words = re.findall(r"\b[A-Z][A-Za-z0-9&.-]*\b", text)

    stop_words = {
        "The", "A", "An", "This", "That", "These", "Those",
        "Today", "Breaking", "Latest", "New", "How", "Why",
        "What", "When"
    }

    keywords = []

    for word in words:
        if word not in stop_words and word not in keywords:
            keywords.append(word)

    return ", ".join(keywords[:top_n])

if __name__ == "__main__":

    sample = """
    openai launches gpt powerful reasoning developers ai models
    """

    print(extract_keywords(sample))