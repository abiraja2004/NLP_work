"""
buildWget.py

  read a file full of file names and create a bash script

  returns:
    0 if no ERROR
    1 if ERROR

"""
import os, sys

def buildWget(in_file, out_file):

    try:
        ifile = open(in_file, 'r')
        ofile = open(out_file, 'w')

        comd = 'wget -P ./pdfs '
        comURL = 'http://gain.fas.usda.gov/Recent GAIN Publications/'

        ofile.write("#!/bin/bash" + os.linesep)

        for line in ifile:
            # a line is formatted: title \t date & time
            # split and just use the title
            nl1, nl2 = line.split('\t')

            ofile.write(comd + " \"" + comURL + nl1 + '.pdf\"' + os.linesep)


        ifile.close()
        ofile.close()
        return 0
    except:
        print "{}".format(sys.exec_info()[0])
        return 1
