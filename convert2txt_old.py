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

ifile = open('files.txt', 'r')
ofile = open('cmd.cmd', 'w')

for filename in ifile:
    fn = filename.split('.pdf')
    str = prgPath + '-o ' + outputPath + fn[0] + '.txt\" ' + inputPath + fn[0] + '.pdf\"'
    # print str
    ofile.write(str + '\n')

print 'done'
