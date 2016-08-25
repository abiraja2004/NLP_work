"""
  grab2convert.py

  This is a driver for the grab and conversion process. It calls other python
  files.

  The process is:
    buildWget.py - process a file of file names to create a shell file
    convert2txt.py - process all pdf files in the local dir, convert each to txt
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
from gensim.summarization import keywords

from buildWget import buildWget
from pdf2textFile import pdf2txt
from summarize import summaryPlusKeywords

""" ---------------------- define functions --------------------------------"""

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




if len(sys.argv) <= 2:
    print 'usage: driver.py in_filename out_filename'
    sys.exit(2)
infile = sys.argv[1]
outfile = sys.argv[2]

try:
    print "Step 1: Get files from gain site"
    r = buildWget(infile, outfile)

except:
    print 'build wget cmd: {}'.format(sys.exc_info()[0])

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
Let's gather a summary of the docs in the pdfs dir
"""
summ = ''
print 'Step 4: gather doc summaries'
try:
    os.chdir('./txt')
    for fn in os.listdir('.'):
        summ, keyw = summaryPlusKeywords(fn)
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
        corpus = MyCorpus(fn, stoplist)
        lda = gensim.models.LdaModel(corpus, id2word=corpus.dictionary, num_topics=NUM_TOPICS)
        topics = lda.print_topic(num2show)

        print '{}\n{}\n{}'.format(summ, keyw, topics)

except:
    print "error {}".format(sys.exc_info()[0])
