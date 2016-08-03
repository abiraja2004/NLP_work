# Source: lda_model.py
import logging
import os
import gensim

from settings import Settings

MODELS_DIR = Settings.MODELS_DIR
NUM_TOPICS = 10

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
#                    level=logging.INFO)

dictionary = gensim.corpora.Dictionary.load(os.path.join(MODELS_DIR, 
                                            "mtsamples.dict"))
corpus = gensim.corpora.MmCorpus(os.path.join(MODELS_DIR, "mtsamples.mm"))

ofile = open(Settings.FINAL_TOPICS_FILENAME, 'w')

# Project to LDA space
lda = gensim.models.LdaModel(corpus, id2word=dictionary, num_topics=NUM_TOPICS)


for n in range(NUM_TOPICS):
    ofile.write(lda.print_topic(n) + '\n')
    
ofile.close()

for n in range(NUM_TOPICS):
    print lda.print_topic(n) + '\n'



