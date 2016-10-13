import string
import requests
import sys
import re

company = raw_input('Insert Company name: \n')
company = company.replace(' ', '%20')
results = ""
totalresults = ""
server = "www.google.com"
userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
quantity = "100"
limit = int(raw_input('Insert limit of search: \n'))
counter = 0

while (counter < limit):
	try:
		urly="http://"+ server + "/search?num=100&start=" + str(counter) + "&hl=en&meta=&q=site%3Alinkedin.com/in%20" + company
	except Exception, e:
		print e
	try:
		r = requests.get(urly, headers = {'User Agent ' : userAgent})
	except Exception,e:
		print e
	results = r.content
	totalresults += results
	counter += 100
	print "\tSearching " + str(counter) + " results.."
	
reg_people = re.compile('">[a-zA-Z0-9._ -,]* \| LinkedIn')
reg_position = re.compile('<div class="f slp">(.*?)</div>')
reg_urls = re.compile('<cite>(.*?)</cite>')

reg_resultado = re.compile('<div class="g">(.*?)<span class="st">')
tmp_resultados = reg_resultado.findall(totalresults)

		
list_empleados = []

for x in tmp_resultados:
	y = string.replace(x, '<b>', '')
	y = string.replace(y, '</b>', '')		

	tmp_people = reg_people.findall(y)
	tmp_urls = reg_urls.findall(y)
	tmp_position = reg_position.findall(y)
	
	#Me aseguro que existan todas las keys
	empleado = {}
	empleado['url'] = 'N/A'
	empleado['Name'] = 'N/A'
	empleado['Office_Location'] = 'N/A'
	empleado['Title'] = 'N/A'
	empleado['Current_Company'] = 'N/A'
	
	for x in tmp_urls:
		y = string.replace(x, '/url?q=', '')
		y = string.replace(y, 'https://', '')
		y = string.replace(y, 'http://', '')
		y = string.replace(y, 'www.', '')
		empleado['url'] = y
	
	for x in tmp_people:
		y = string.replace(x, ' | LinkedIn', '')
		y = string.replace(y, ' profiles ', '')
		y = string.replace(y, 'LinkedIn', '')
		y = string.replace(y, '"', '')
		y = string.replace(y, '>', '')
		#if y != " ":
		empleado['Name'] = y
		
	for x in tmp_position:
		y = string.replace(x, '&nbsp;', '')
		y = string.replace(y, '&nbsp', '')
		tmpa = y.split('-')
		try:
			empleado['Office_Location'] = tmpa[0]
		except Exception, e:
			empleado['Office_Location'] = 'N/A'
		try:
			empleado['Title'] = tmpa[1]
		except Exception, e:
			empleado['Title'] = 'N/A'
		try:
			empleado['Current_Company'] = tmpa[2]
		except Exception, e:
			empleado['Current_Company'] = 'N/A'

	list_empleados.append(empleado)

f = open('Results.txt', 'w')
f.write('Name; Title; Office Location ; Current Company; URL;  \n')


for x in list_empleados:
	if str(x['Name']) != 'N/A' :
		f.write(str(x['Name']) + ';' + str(x['Title']) + ';' + str(x['Office_Location'])+ ';' + str(x['Current_Company'])+ ';'  + str(x['url']) + '\n')
f.close()

print('Ready')