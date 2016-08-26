"""
  driver.py

  This is a driver for the grab and conversion process. It calls other python
  files.

  The process is:
    buildWget.py - process a file of file names to create a shell file
    pdf2textFile.py - process all pdf files in the local dir, convert each to txt
    summarize.py - use gensim to create:
        doc summary, doc keywords, latent topics for the document
    inject2mongo.py - process each txt file and inject info into mongodb

  for each file
    use gensim to find the key words for the file
    use gensim to find the latent topics in the file
    use gensim to create a 100 word summary of the file
    use gensim to create a list of the top 20 similar files to this one
    inject these plus the file name and raw text for the file into mongodb

  depends on wget and mudraw and bash

"""
import os, sys
import subprocess
import nltk
import gensim

import nltk
import gensim
import itertools
import pickle
import json

from gensim.summarization import keywords
from gensim.similarities import MatrixSimilarity, SparseMatrixSimilarity, Similarity
from pymongo import MongoClient


from buildWget import buildWget
from pdf2textFile import pdf2txt
from summarize import summaryPlusKeywords


""" ---------------------- define text processing class ---------------------"""

def iter_docs(fn, stoplist):
    fin = open(fn, 'rb')
    text = fin.read()
    fin.close()
    yield (x for x in
        gensim.utils.tokenize(text, lowercase=True, deacc=True,
                              errors="ignore")
        if x not in stoplist)

class MyCorpus(object):

    def __init__(self, fileName, stoplist):
        self.fn = fileName
        self.stoplist = stoplist
        self.dictionary = gensim.corpora.Dictionary(iter_docs(fileName, stoplist))

    def __iter__(self):
        for tokens in iter_docs(self.fn, self.stoplist):
            yield self.dictionary.doc2bow(tokens)
""" -------------------------- main program code --------------------------"""


# handle input arguments

if len(sys.argv) <= 2:
    print 'usage: driver.py in_filename out_filename'
    sys.exit(2)
infile = sys.argv[1]
outfile = sys.argv[2]

client = MongoClient()
db = client.fas

""" this try/catch will create a bash script to pull files from the GAIN site. """
try:
    print "Step 1: Get files from gain site"
    r = buildWget(infile, outfile)

except:
    print 'build wget cmd: {}'.format(sys.exc_info()[0])

""" run the bash script """
try:
    st = ["bash", outfile]
    print "Step 2: Running wget to gather files: {}".format(st)
    r = subprocess.check_output(st)
except:
    print "getting files: {}".format(sys.exc_info()[0])

"""
transform the files in the pdfs dir into txt files
"""
try:
    print "Step 3: convert pdf files to txt files"
    r = pdf2txt()
    st = ["bash", "cmd.sh"]
    r = subprocess.check_output(st)
except:
    print "convert pdf files to text files: error: ".format(sys.exc_info()[0])

"""
gensim operations:
    document summary, document keywords, latent topics
"""
summ = ''
print 'Step 4: gather doc summaries'
numSimilar2Show = 20
# first load the basic models
MODELS_DIR = "models"

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',  level=logging.ERROR)
dictionary = gensim.corpora.Dictionary.load(os.path.join(MODELS_DIR, "mtsamples.dict"))
corpus = gensim.corpora.MmCorpus(os.path.join(MODELS_DIR, "mtsamples.mm"))
# generate a tfidf model from the set of all articles
tfidf = gensim.models.TfidfModel(corpus, normalize=True)
corpus_tfidf = tfidf[corpus]
# then generate a LSI model from the set of all articles
lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)

# now, create a dense index from the set of all articles
index_dense = MatrixSimilarity(lsi[corpus])
# load the file list
file_list = pickle.load( open('models/file_list.p', 'rb'))

try:
    os.chdir('./txt')
    for title in os.listdir('.'):
        summ, keyw = summaryPlusKeywords(title)
        """
         do latent topics for this file
        """
        stoplist = set(nltk.corpus.stopwords.words("english"))
        stoplist.add('mt')
        stoplist.add('production')
        stoplist.add('food')
        stoplist.add('products')
        stoplist.add('mmt')
        stoplist.add('metric')

        NUM_TOPICS = 10
        num2show = 1
        lat_corpus = MyCorpus(title, stoplist)
        lda = gensim.models.LdaModel(lat_corpus, id2word=lat_corpus.dictionary, num_topics=NUM_TOPICS)
        topics = lda.print_topic(num2show)

        # print '{}\n{}\n{}'.format(summ, keyw, topics)
        """
        Step 5: load large gensim data base and create similar docs list

            This whole section assumes that bow_model.py and iter_docs.py
            have been run
        """
        print 'Step 5 similar article processing'
        try:
            # pull in the doc and tokenize it
            fi = open(title, 'r')
            body = fi.read()
            fi.close()

            # now, transform the text
            bow_text = dictionary.doc2bow(gensim.utils.tokenize(body, lowercase=True, deacc=True))

            # let's use the input file and translate it into the lsi space.
            vec_lsi = lsi[bow_text]
            # compute the similarity index
            sims = index_dense[vec_lsi]
            # print the raw vector numbers (debug info)
            # print (list(enumerate(sims)))
            # now, sort by similarity number and print the highest similar articles to the query
            sims = sorted(enumerate(sims), key=lambda item: -item[1])
            # print (sims)
            similarList = []
            # just use the top numshow similar docs
            for i in range(numSimilar2Show):
                ind = sims[i][0]
                # print the strength and filename
                #print '{:1.2f} {}'.format(sims[i][1], file_list[ind])
                similarList.append(file_list[ind])
        except:
            print 'error in step 5: {}\n{}'.format(fn, sys.exc_info()[0])
            sys.exit(2)
        """ ---- time to insert computed data in mongodb! ----------- """
        article = {}
        article['title'] = title
        article['keywords'] = keyw
        article['summary'] = summ
        article['body'] = body
        article['latentTopics'] = topics
        article['similarList'] = similarList
        r = db.fas.insert_one(article)
        print r
except TypeError, ex:
    print "error {}: {}".format(sys.exc_info()[0], ex)
