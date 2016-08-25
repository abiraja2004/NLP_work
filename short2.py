# Source: lsi_model.py
import logging
import os
import gensim

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
                    level=logging.INFO)

MODELS_DIR = "models"

# work with these variables from now on!

dictionary = gensim.corpora.Dictionary.load(os.path.join(MODELS_DIR, 
                                            "mtsamples.dict"))
corpus = gensim.corpora.MmCorpus(os.path.join(MODELS_DIR, "mtsamples.mm"))

tfidf = gensim.models.TfidfModel(corpus, normalize=True)
corpus_tfidf = tfidf[corpus]

