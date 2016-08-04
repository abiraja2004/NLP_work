# Source: bow_model.py
import logging
import os, sys, getopt
import nltk
import gensim

from settings import Settings

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


#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
#                    level=logging.INFO)

def main(argv):

    usage = 'usage: doc2topics [-ha --help --all] "absolute file name"'

    if len(sys.argv) <= 1:
        print usage
        sys.exit(2)

    NUM_TOPICS = 10
    num2show = 1
    fileName = sys.argv[1]

    try:
        opts, args = getopt.getopt(argv, "ha:", ["help, all"])
    except getopt, GetoptError:
        print usage
        sys.exit(2)

    for opt, arg in opts:
        if opt in ['-h', '--help']:
            print usage
            sys.exit(0)
        elif opt in ("-a", "--all"):
            num2show = 5
            fileName = sys.argv[2]
        else:
            print usage
            sys.exit(2)

    stoplist = set(nltk.corpus.stopwords.words("english"))
    stoplist.add('mt')
    stoplist.add('production')
    stoplist.add('food')
    stoplist.add('products')
    stoplist.add('mmt')
    stoplist.add('metric')

    # print stoplist
    print "starting process"
    corpus = MyCorpus(fileName, stoplist)

    # corpus.dictionary.filter_extremes(no_below=5)

    corpus.dictionary.save(os.path.join(Settings.MODELS_DIR, Settings.DICTIONARY_FILENAME))
    gensim.corpora.MmCorpus.serialize(os.path.join(Settings.MODELS_DIR, Settings.CORPUS_FILENAME), corpus)
    lda = gensim.models.LdaModel(corpus, id2word=corpus.dictionary, num_topics=NUM_TOPICS)
    if num2show == 0:
        print lda.print_topic(num2show)
    else:
        for i in range(num2show):
            print lda.print_topic(i)
            
if __name__ == "__main__":
    main(sys.argv[1:])
