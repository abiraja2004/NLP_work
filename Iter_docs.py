# source iter_docs.py
import logging
import os
import nltk
import gensim
import pickle

def iter_docs(topdir):
    n = 0
    ln = {}
    for fn in os.listdir(topdir):
        ln[n] = fn
        n = n + 1
    pickle.dump(ln, open('models/file_list.p', 'wb'))

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
                    level=logging.INFO)

TEXTS_DIR = "txt"
MODELS_DIR = "models"


iter_docs(TEXTS_DIR)
file_list = pickle.load( open('models/file_list.p', 'rb'))

n = 1
for i in file_list.keys():
    print '{}, {}'. format(i, file_list[i])
    n = n+1