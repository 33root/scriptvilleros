#!/bin/bash
import re
from urlparse import urlparse
deb = 1
folderTxt = './PDFs/txt/'
folder = './PDFs/'
reurls = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

def pdf2txt(path):
	rsrcmgr = PDFResourceManager()
	retstr = StringIO()
	codec = 'utf-8'
	laparams = LAParams()
	device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
	fp = open(path, 'r+')
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	password = ""
	maxpages = 0
	caching = True
	pagenos=set()
	for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
		interpreter.process_page(page)
	text = retstr.getvalue()
	fp.close()
	device.close()
	retstr.close()
	return text

urls = []
from os import listdir
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


i = 0
for file in listdir(folder):
	if not(file.endswith('.pdf')):
		continue
	path = folder + file
	if deb:
		print 'Path:' + path
	i = i+1
	try:
		print 'Parseando PDF a texto...'
		namear = folderTxt + 'salida' + str(i) + '.txt'
		ar = open(namear, 'w')
		ar.write(pdf2txt(path))
		ar.close()
		print 'Archivo ' + path + ' parseado: ' + namear + ' creado exitosamente'
	except ValueError:
		print 'estaba asi cuando llegue'

for file in listdir(folderTxt):
	print 'Buscando URLs...'
        archivo = open(folderTxt + file, 'r')
        content = archivo.read()
        archivo.close()
        urls = reurls.findall(content)

output = []
count_domains = dict()

for u in urls:
	domain = urlparse(u).netloc.replace('www.', "").replace("https://", "").replace("http://","")
	result = (u, domain)
	count_domains[domain] = count_domains.get(domain, 0) + 1
	output.append(result)
fout = open(folder+ 'results.txt', 'w')
fout.write("URLs,Domains,Count\n")

print 'Escribiendo archivo de resultados...'
for out in output:
	iteraciones = count_domains.get(out[1], 0)
	fout.write(out[0]+','+out[1]+','+str(iteraciones)+'\n')

print 'Fin'

