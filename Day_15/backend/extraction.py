from sklearn.feature_extraction.text import TfidfVectorizer


def extract_keywords(text, top_n=5):
    """
    Extract top keywords from cleaned text using TF-IDF.
    """

    if not text:
        return ""

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform([text])

    feature_names = vectorizer.get_feature_names_out()

    scores = tfidf_matrix.toarray()[0]

    word_scores = list(zip(feature_names, scores))

    sorted_words = sorted(
        word_scores,
        key=lambda x: x[1],
        reverse=True
    )

    keywords = [word for word, score in sorted_words[:top_n]]

    return ", ".join(keywords)

if __name__ == "__main__":

    sample = """
    openai launches gpt powerful reasoning developers ai models
    """

    print(extract_keywords(sample))