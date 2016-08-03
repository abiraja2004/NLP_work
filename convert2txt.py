import os


"""
  converts all files in the pdfs dir into txt files

  input: file.txt is ls -1 > files.txt
  output: dos cmd file

  each line of the output file calls mutool with the -o file.txt and *.pdf

  the output file is a DOS cmd file!!

"""

prgPath = '\\Users\\muguiraj\\Downloads\\mupdf-1.9a-windows\\mupdf-1.9a-windows\\mutool.exe draw -F txt '
outputPath = '\"txt\\'
inputPath = '\"pdfs\\'
inFilePath = '.'
outFilePath = '../cmd.cmd'

ofile = open(outFilePath, 'w')

files = os.listdir(inFilePath)
n = 0
for fileName in files:
    leng = os.stat(fileName).st_size

    if leng <= 0:
        print 'found zero len file: {}'.format(fileName)
        continue

    fn = fileName.split('.pdf')
    str = prgPath + '-o ' + outputPath + fn[0] + '.txt\" ' + inputPath + fn[0] + '.pdf\"'
    print '.'
    ofile.write(str + '\n')
    n += 1


print 'processed {} files'.format(n+1)
