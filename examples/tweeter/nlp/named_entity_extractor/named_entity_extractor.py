from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk

def extract_named_entities(text):
    sentences = sent_tokenize(text)
    sentences = [word_tokenize(sent) for sent in sentences]
    sentences = [pos_tag(sent) for sent in sentences]
    result = []
    for sent in sentences:
        result += [word[0] for word, tag in ne_chunk(sent, binary=True).pos()
                   if tag == 'NE']
    return result

if __name__ == '__main__':
    text = "This is test. Mr. Foobar is a bad person."
    print extract_named_entities(text)
