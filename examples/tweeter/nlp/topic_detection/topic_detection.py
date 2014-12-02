from nltk.corpus import reuters, movie_reviews
from operator import itemgetter
import nltk, pickle


class TopicDetector:
    def __init__(self, path_to_data=None):
        self._load_vector(path_to_data)
        self.words = map(itemgetter(0), self.vector)
        self.topics = ["movies"]

    def _load_vector(self, path_to_data):
        if not path_to_data:
            path_to_data = '/tmp/stats.pickle'
        self.vector = None
        try:
            data_file = open(path_to_data, 'rb')
            self.vector = pickle.load(data_file)
        except IOError:
            data_file = open(path_to_data, 'wb')

            all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words() if len(w) > 3)
            all_words_r = nltk.FreqDist(w.lower() for w in reuters.words() if len(w) > 3)

            self.vector = []

            for word in all_words.keys():
                ratio = 0
                try:
                    ratio = all_words.freq(word) / all_words_r.freq(word)
                except ZeroDivisionError:
                    next
                self.vector.append((word, ratio))
                self.vector.sort(key=itemgetter(1), reverse=True)
                self.vector = self.vector[:200]

            pickle.dump(self.vector, data_file)
    def is_topic(self, topic, text):
        if topic not in self.topics:
            None # todo: more topics than movies

        words = set([word.lower() for word in nltk.wordpunct_tokenize(text)])
        print self.words
        inter = words.intersection(self.words)
        print inter
        return len(inter) > 1

if __name__ == '__main__':
    td = TopicDetector()
    print td.is_topic("movies", "What an amazing movie!")
    print td.is_topic("movies", "Great premiere.")
