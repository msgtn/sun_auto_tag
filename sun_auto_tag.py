import io
from PIL import Image
import pexif
# import exifread
# import piexif
import os
from bs4 import BeautifulSoup as bs
import urllib2

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
womens_bball_url = 'http://www.cornellbigred.com/roster.aspx?path=wbball&'
req = urllib2.Request(womens_bball_url, headers=hdr)
page = urllib2.urlopen(req)
soup = bs(page.read(), 'html.parser')
roster_num = soup.find_all('td', {'class':'roster_dgrd_no'})
roster_name = soup.find_all('td', {'class':'roster_dgrd_full_name'})
nums = []
names = []
for i in range(0,len(roster_num)):
	try:
		cur_num = str(roster_num[i].text)
		cur_num = cur_num[:cur_num.find(' ')]
		cur_name = str(roster_name[i].text)
		nums.append(cur_num)
		names.append(cur_name)
	except:
		pass
print nums

files = os.listdir(os.getcwd())
print files
files = files[1:]
# files = os.listdir(input('Enter Directory'))

for file in files:
	print file
	im = pexif.JpegFile.fromFile(file)
	image_desc = im.exif.primary.ImageDescription
	# f = piexif.load(f)
	# image_desc = f['0th'].values()[2]
	# f = open(f, 'rb')
	# tags = exifread.process(f)
	# image_desc = tags['Image ImageDescription'].values
	num_start_idx = image_desc.find('*')
	num_end_idx = image_desc.find('*', num_start_idx+1)
	num = int(image_desc[num_start_idx+1:num_end_idx])
	num_idx = nums.index(str(num))
	name = names[num_idx]
	new_image_desc = image_desc[:num_start_idx] + name + image_desc[num_end_idx+1:]
	im.exif.primary.ImageDescription = new_image_desc
	im.writeFile('newfile.jpg')