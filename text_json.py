import logging
import os
import nltk
import gensim
import itertools
import pickle
import sys, getopt
import json
from gensim.similarities import MatrixSimilarity, SparseMatrixSimilarity, Similarity


def main(argv):

    if len(sys.argv) != 2:
        print 'usage: text_exp sentence'
        sys.exit(2)
        
    # encode this sentence into semantic space
    # text = "Rice wheat and barley are all important feed crops."
    # text = "Brazil issues with industrial pollution"

    text = sys.argv[1]

    # first load the basic models
    MODELS_DIR = "models"
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',  level=logging.ERROR)
    dictionary = gensim.corpora.Dictionary.load(os.path.join(MODELS_DIR, "mtsamples.dict"))
    corpus = gensim.corpora.MmCorpus(os.path.join(MODELS_DIR, "mtsamples.mm"))

    # now, transform the text
    bow_text = dictionary.doc2bow(gensim.utils.tokenize(text))
    # show me the transformed text
    # print([(dictionary[id], count) for id, count in bow_text])

    # generate a tfidf model from the set of all articles
    tfidf = gensim.models.TfidfModel(corpus, normalize=True)
    corpus_tfidf = tfidf[corpus]
    # then generate a LSI model from the set of all articles
    lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)

    # now, create a dense index from the set of all articles
    index_dense = MatrixSimilarity(lsi[corpus])

    # finally, let's use the input query and translate it into the lsi space.
    vec_lsi = lsi[bow_text]
    # compute the similarity index
    sims = index_dense[vec_lsi]
    # print the raw vector numbers 
    # print (list(enumerate(sims)))

    # now, sort by similarity number and print the highest similar articles to the query
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    # print (sims)

    # load the file list
    file_list = pickle.load( open('models/file_list.p', 'rb'))

    # use it to show the article names

    dictSimilars = {}
    for i in range(len(sims)):
        ind = sims[i][0]
        dictSimilars[str(sims[i][1])] = file_list[ind]

    js = json.dumps(dictSimilars)
    return js

    
if __name__ == "__main__":
    main(sys.argv[1:])
