"""
  similar_doc.py - take a file name and return a list of top most aligned articles from the 
      gain/FAS dataset.

  input: a file name
  output: "percent alignment" , "article title"
  parameters:
    If no parameters are given show just the top 5
    -a or --all says "show all articles
"""

import logging
import os
import nltk
import gensim
import itertools
import pickle
import sys, getopt
from gensim.similarities import MatrixSimilarity, SparseMatrixSimilarity, Similarity

def main(argv):

    print "not finished yet!!!"
    
    if len(sys.argv) <= 1:
        print 'usage: similar_doc [-ha --help --all] document name'
        sys.exit(2)

    num2show = 20
    doc = sys.argv[1]
    
    try:
        opts, args = getopt.getopt(argv, "ha:", ["all"])
    except getopt, GetoptError:
        print 'similar_doc.py [-a --all] "document name"'
        sys.exit(2)
        

    for opt, arg in opts:
        if opt == '-h':
            print 'similar_doc.py [-a --all] "document name"'
            sys.exit(0)
        elif opt in ("-a", "--all"):
            num2show = 0
            doc = sys.argv[2]
        else:
            print 'similar_doc.py [-a --all] "document name"'
            sys.exit(2)
            
    # encode this sentence into semantic space
    # text = "Rice wheat and barley are all important feed crops."
    # text = "Brazil issues with industrial pollution"



    # first load the basic models
    MODELS_DIR = "models"
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',  level=logging.ERROR)
    dictionary = gensim.corpora.Dictionary.load(os.path.join(MODELS_DIR, "mtsamples.dict"))
    corpus = gensim.corpora.MmCorpus(os.path.join(MODELS_DIR, "mtsamples.mm"))

    # pull in the doc and tokenize it
    fi = open(doc, 'r')
    text = fi.read()
    fi.close()
    
    # now, transform the text
    bow_text = dictionary.doc2bow(gensim.utils.tokenize(text, lowercase=True, deacc=True))
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

    if num2show != 0:
        numshow = 20
    else:
        numshow = len(sims)
    
    for i in range(numshow):
        ind = sims[i][0]
        # print the strength and filename
        print '{:1.2f} {}'.format(sims[i][1], file_list[ind])
    
if __name__ == "__main__":
    main(sys.argv[1:])
