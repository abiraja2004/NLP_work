import os

files = os.listdir('.')
n = 0
for fileName in files:
    leng = os.stat(fileName).st_size

    if leng <= 0:
        print 'found zero len file: {}'.format(fileName)
        continue
    n += 1

print 'processed {} files'.format(n+1)
