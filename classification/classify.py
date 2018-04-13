# TUTORIAL https://chatbotslife.com/text-classification-using-algorithms-e4d50dcba45
# use natural language toolkit
import sys
import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer

class Classifier(object):
    def __init__(self):
        # word stemmer
        self.stemmer = LancasterStemmer()
        self.training_data = []
        self.class_words = {}
        self.corpus_words = {}

    def process_training_data(self):
        # capture unique stemmed words in the training corpus
        self.corpus_words = {}
        self.class_words = {}
        # turn a list into a set (of unique items) and then a list again (this removes duplicates)
        classes = list(set([a['class'] for a in self.training_data]))
        for c in classes:
            # prepare a list of words within each class
            self.class_words[c] = []

        # loop through each sentence in our training data
        for data in self.training_data:
            # tokenize each sentence into words
            for word in nltk.word_tokenize(data['sentence']):
                # ignore a some things
                if word not in ["?", "'s"]:
                    # stem and lowercase each word
                    stemmed_word = self.stemmer.stem(word.lower())
                    # have we not seen this word already?
                    if stemmed_word not in self.corpus_words:
                        self.corpus_words[stemmed_word] = 1
                    else:
                        self.corpus_words[stemmed_word] += 1

                    # add the word to our words in class list
                        self.class_words[data['class']].extend([stemmed_word])

        # we now have each stemmed word and the number of occurances of the word in our training corpus (the word's
        # commonality)
        print("Corpus words and counts: %s \n" % self.corpus_words)
        # also we have all words in each class
        print("Class words: %s" % self.class_words)

    def read_training_data(self, file_name):
        with open(file=file_name, mode="r") as training:
            for line in training:
                category, sentence = line.split("\t")
                self.training_data.append({
                                         "class": category,
                                         "sentence": sentence
                                         })

        print("%s sentences of training data" % len(self.training_data))

    # calculate a score for a given class taking into account word commonality
    def calculate_class_score(self, sentence, class_name, show_details=True):
        score = 0
        # tokenize each word in our new sentence
        for word in nltk.word_tokenize(sentence):
            # check to see if the stem of the word is in any of our classes
            if self.stemmer.stem(word.lower()) in self.class_words[class_name]:
                # treat each word with relative weight
                score += (1 / self.corpus_words[self.stemmer.stem(word.lower())])

                if show_details:
                    print("   match: %s (%s)" % (
                        self.stemmer.stem(word.lower()), 1 / self.corpus_words[self.stemmer.stem(word.lower())]))
        return score


    # return the class with highest score for sentence
    def classify(self, sentence):
        high_class = None
        high_score = 0
        # loop through our classes
        for c in self.class_words.keys():
            # calculate score of sentence for each class
            score = self.calculate_class_score(sentence, c, show_details=False)
            # keep track of highest score
            if score > high_score:
                high_class = c
                high_score = score

        return high_class, high_score


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: python3 classify.py <sentence>")
        sys.exit(0)
        # sys args
    sentence = sys.argv[1]
    classfier = Classifier()
    classfier.read_training_data("test.csv")
    classfier.process_training_data()
    print(classfier.classify(sentence=sentence))
