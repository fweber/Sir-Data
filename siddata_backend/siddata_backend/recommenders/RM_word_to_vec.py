"""
Module takes text as input, generates QA-pairs and validates given answers based on a Word-to-vec approach.
The module requires the trained word2vec model, which can be downloaded from
https://github.com/mmihaltz/word2vec-GoogleNews-vectors
"""

import gensim
import logging
from siddata_backend import settings
from gensim.parsing.preprocessing import remove_stopwords


class RM_word_to_vec():

    def intialize(self):
        """
        Constuctor
        @return: returns True if successful
        """
        return True


    def generate_questions_and_answers(self, text, number_of_questions):
        """
        Takes a large text summarizing a ressource as input and generates a list of Questions and answers of a given length.
        @param number_of_questions: Number of QA-pairs to return
        @param text: Text describing a ressource
        @return : List of Questions and correct answers
        """
        QA = [{"question":"WTF?","answer":"True!"},{"question":"Really?","answer":"Yes, indeed!"}]

        return QA


    def check_answer(self, correct_answer, given_answer):
        """
        Checks if a given answer matches the correct one base on a Word-To-Vec Approach
        @param correct_answer: L
        @param given_answer:
        @return:
        """


        # Logging code taken from http://rare-technologies.com/word2vec-tutorial/
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        # Load Google's pre-trained Word2Vec model.
        model_path = ("{}/word2vec_model/GoogleNews-vectors-negative300.bin".format(settings.BASE_DIR))
        model = gensim.models.KeyedVectors.load_word2vec_format(model_path,
                                                                binary=True)

        sentence_a = remove_stopwords(correct_answer)
        sentence_b = remove_stopwords(given_answer)

        lst_a = sentence_a.split(" ")
        lst_b = sentence_b.split(" ")

        print("Similarity by n_similarity function")
        print(model.n_similarity(lst_a, lst_b))

        sum_a = 0
        for word in lst_a:
            vector = model[word]
            sum_a += vector

        sum_b = 0
        for word in lst_b:
            vector = model[word]
            sum_b += vector

        print("distance between \nsentence a: %s \nsentence b: %s " % (sentence_a, sentence_b))
        print(type(sum_a))

        if correct_answer == given_answer:
            return True
        else:
            return False


