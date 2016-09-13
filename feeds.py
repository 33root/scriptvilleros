#!/usr/bin/python
import sys
from bs4 import BeautifulSoup

titulo = sys.argv[1] 
fileName = sys.argv[2]

data = open(fileName, 'r').read()

#soup = BeautifulSoup('xml', data)
soup = BeautifulSoup(data, 'xml')
content = soup.find('outline', title=titulo)
outlines = []

for out in content.find_all('outline'):
	l = (out.get('title'), out.get('htmlUrl'))
	outlines.append(l)

salida = open('feeds.txt', 'w+')
salida.write('Titulo,')
salida.write('htmlUrl')
salida.write('\n')
for l in outlines:
	salida.write((l[0]+','+l[1]+'\n').encode('utf8'))
#	print l[0]+','+l[1]+'\n'

salida.close()

print 'Fin'
