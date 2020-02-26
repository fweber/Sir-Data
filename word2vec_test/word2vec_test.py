# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 11:39:34 2016

@author: Chris
"""

# Explore Google's huge Word2Vec model.

import gensim
import logging
from gensim.parsing.preprocessing import remove_stopwords

# Logging code taken from http://rare-technologies.com/word2vec-tutorial/
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Load Google's pre-trained Word2Vec model.
# model = gensim.models.Word2Vec.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True)
model = gensim.models.KeyedVectors.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True)

vocab = model.vocab.keys()
wordsInVocab = len(vocab)

words = ["Hackathon","programming"]
for word in words:
    print(model.most_similar_cosmul(positive="Felix", topn=10))
    print("Close to %s:")
    print(model.most_similar(positive=word))

pairs = [("book","lexicon"),("lunch","dinner"),("food","eat"),("cat","dog"),("umbrella","reading"),("umbrella","umbrella")]
for a,b in pairs:
    print("Similarity between %s and %s"%(a,b))
    print (model.similarity(a, b))


sentences = [
    ("Paris is a wonderful city","The capital of France is beautiful"),
    ("the horse raced past the barn fell","a horse runs near a farm and falls"),
    ("hey freaks","dear ladies and gentlemen"),
    ("nearby there is a great sushi place",("very close one can order delicious japanese food"))]
for sentence_a,sentence_b in sentences:

        print("compare sentences")
        print(sentence_a)
        print(sentence_b)

        # vmdistance
        print("vmdistance")
        print(model.wmdistance(sentence_a, sentence_b))


        sentence_a = remove_stopwords(sentence_a)
        sentence_b = remove_stopwords(sentence_b)
        lst_a = sentence_a.split(" ")
        lst_b = sentence_b.split(" ")


        print("n_similarity")
        print(model.n_similarity(lst_a,lst_b))

# sum_a = 0
# for word in lst_a:
#     vector = model[word]
#     sum_a += vector
#
# sum_b = 0
# for word in lst_b:
#     vector = model[word]
#     print(type(vector))
#     sum_b += vector

# print("distance between \nsentence a: %s \nsentence b: %s "%(sentence_a, sentence_b))
# print(type(sum_a))
# print(sum_a)
# print(model.similarity(sum_a,sum_b))

#print(sum_b - sum_a)

# Does the model include stop words?
#print("Does it include the stop words like \'a\', \'and\', \'the\'? %d %d %d" % ('a' in model.vocab, 'and' in model.vocab, 'the' in model.vocab))

# # Retrieve the entire list of "words" from the Google Word2Vec model, and write
# # these out to text files so we can peruse them.
# vocab = model.vocab.keys()
#
# fileNum = 1
#
# wordsInVocab = len(vocab)
# wordsPerFile = int(100E3)
#
# # Write out the words in 100k chunks.
# for wordIndex in range(0, wordsInVocab, wordsPerFile):
#     # Write out the chunk to a numbered text file.
#     with open("vocabulary/vocabulary_%.2d.txt" % fileNum, 'w') as f:
#         # For each word in the current chunk...
#         for i in range(wordIndex, wordIndex + wordsPerFile):
#             # Write it out and escape any unicode characters.
#             f.write(vocab[i].encode('UTF-8') + '\n')
#             fileNum += 1
