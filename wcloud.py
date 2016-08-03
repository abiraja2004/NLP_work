import os
from wordcloud import *
import matplotlib.pyplot as plt

MODELS_DIR = "models"

wc = WordCloud()
final_topics = open(os.path.join(MODELS_DIR, "final_topics.txt"), 'rb')
curr_topic = 0
for line in final_topics:
    line_plus = line.strip().split('+')
    freqs = []
    for it in line_plus:
        scores_a = it.strip().split('*')
        freqs.append( (scores_a[1], float(scores_a[0])) )

    elements = wc.fit_words(freqs)
    plt.imshow(wc)
    name = 'fig' + str(curr_topic) + '.png'
    plt.savefig(name)
    curr_topic += 1


"""
wordcloud = WordCloud().generate(words)
plt.imshow(wordcloud)
plt.axis('off')
"""
