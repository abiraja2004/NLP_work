import os, sys


"""
  converts all files in the pdfs dir into txt files in the txt dir

  input: file.txt is ls -1 > files.txt
  output: bash script
  usage:
    cd into the dir with the pdf files
    python ../convert2txt.py
    cd ..

  each line of the output file calls pdftotext

  the output file is a bash script!!

"""

# prgPath = '\\Users\\muguiraj\\Downloads\\mupdf-1.9a-windows\\mupdf-1.9a-windows\\mutool.exe draw -F txt '
prgPath = 'pdftotext '
outputPath = '\"txt/'
inputPath = '\"pdfs/'
inFilePath = '.'
outFilePath = '../cmd.sh'

def pdf2txt():
    os.chdir('./pdfs')
    ofile = open(outFilePath, 'w')

    files = os.listdir(inFilePath)
    n = 0
    for fileName in files:
        leng = os.stat(fileName).st_size

        if leng <= 0:
            print 'found zero len file: {}'.format(fileName)
            continue

        fn = fileName.split('.pdf')
        #str = prgPath + '-o ' + outputPath + fn[0] + '.txt\" ' + inputPath + fn[0] + '.pdf\"'
        str = prgPath + inputPath + fileName + "\" " + outputPath + fn[0] + ".txt\""
        print '.'
        ofile.write(str + '\n')
        n += n + 1

    print 'processed {} files'.format(n)
    os.chdir('..')
    return 0

if __name__ == "__main__":
    pdf2txt()
