import requests
import sys
from bs4 import BeautifulSoup

next = str(raw_input('Insert fotolog URL:\n'))
url = requests.get(next)
soup = BeautifulSoup(url.content, 'html.parser')

def proxImg(): 
	
	ret = soup.findAll("a", {"class" : "arrow_change_photo arrow_change_photo_right"})
	try:
		return str(ret[0].get('href'))
	except :	
		return ''

def linkImg():
	return soup.find(id="flog_img_holder").findAll('img')[0].get('src')

def descr():
	return soup.find(id="description_photo").text

i=0
while (next != ''):


		url = requests.get(next)
		soup = BeautifulSoup(url.content, 'html.parser')

		img = str(linkImg())
		print img
		try:
			g = open('image'+str(i)+'.jpg', 'w')
			g.write(requests.get(img).content)
			g.close()
		except exception:
			print('error writing imagen'+str(i)+'.jpg')
		try:
			f = open('description'+str(i)+'.txt', 'w')
			f.write(descr().encode('utf-8'))
			f.close()
		except exception:
			print('error writing description'+str(i)+'.txt\n')


		i += 1

		next = proxImg()

print('No more images')
sys.exit(0)

