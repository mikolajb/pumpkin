from nltk import wordpunct_tokenize
from nltk.corpus import stopwords

def detect_language(text):

    words = [word.lower() for word in wordpunct_tokenize(text)]
    result = (None, -1)

    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)
        ratio = float(len(common_elements)) / len(stopwords_set)

        if ratio > result[1]:
            result = (language, ratio)

    return result[0]

if __name__=='__main__':

    text = "This is a test."
    language = detect_language(text)

    print language
