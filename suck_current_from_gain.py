"""
  From the USDA GAIN system, pull all current pdfs

  inputs: FAS_GAIN_DATA.txt, this is a page scrape of the document names
  output: a list of the files setup to run as a unix shell script

  depends on bash and wget
"""

import os
ifile = open('FAS_GAIN_DATA.txt', 'r')
ofile = open('FAS-o.txt', 'w')

comd = 'wget '
comURL = 'http://gain.fas.usda.gov/Recent GAIN Publications/'

for line in ifile:
    # a line is formatted: title \t date & time
    # split and just use the title
    nl1, nl2 = line.split('\t')

    ofile.write(comd + " \"" + comURL + nl1 + '.pdf\"' + os.linesep)


ifile.close()
ofile.close()
