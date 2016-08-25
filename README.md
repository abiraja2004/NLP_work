# NLP_work
Capture my current topic modeling work

The initial work here was created to build a processing pipe line to take pdfs from the USDA FAS/GAIN web site.

Dependes on:
pdftotext to convert the pdf docs to txt files
unix wget


Pipeline:
copy / paste file names from the web page into a text doc called FAS_GAIN_DATA.txt
run suck_current_from_gain.py
cd to the pdfs dir
run convert2txt.py - creates a bash script that runs pdftotext

Now we can run NLP code
python bow_model.py first
python lsi_model.py OR lda_model.py

Then you visualize:
python num_topics.py to use kmean clustering on all files in the txt dir
python viz_topics.py to see a scatter plot of clusters
python wcloud.py (depends on lda_model) to see a word cloud of topics
       of files in file "final_topics.txt"
