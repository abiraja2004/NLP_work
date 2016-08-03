# Source: lsi_model.py
import logging
import os
import gensim

from settings import Settings

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
                    level=logging.INFO)

MODELS_DIR = Settings.MODELS_DIR

# work with these variables from now on!

dictionary = gensim.corpora.Dictionary.load(os.path.join(MODELS_DIR, 
                                                         Settings.DICTIONARY_FILENAME))
corpus = gensim.corpora.MmCorpus(os.path.join(MODELS_DIR, Settings.CORPUS_FILENAME))

tfidf = gensim.models.TfidfModel(corpus, normalize=True)
corpus_tfidf = tfidf[corpus]

# project to 2 dimensions for visualization
lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)

# write out coordinates to file
fcoords = open(os.path.join(MODELS_DIR, Settings.COORDS_FILENAME), 'wb')
for vector in lsi[corpus]:
    for item in vector:
        
        if len(item) != 2:
            continue
        fcoords.write("%6.4f\t%6.4f\n" % (item[0], item[1]))
fcoords.close()
