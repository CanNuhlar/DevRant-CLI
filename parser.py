from __future__ import print_function
import urllib2
import os
from bs4 import BeautifulSoup, Comment
import img2txt
import sys,urllib, cStringIO
import ansi
from PIL import Image

def get_terminal_width():
	columns = os.popen('stty size', 'r').read().split()[1]
	return int(columns)

#feed and search pages are almost identical so we use the same code for them
#sort_type params = algo, top, recent
def parse_feed(url_type="feed", url_arg="", page_number=1, sort_type="algo"):
	if url_type == "feed":
		response = urllib2.urlopen("http://devrant.io/feed/" + sort_type + "/" + str(page_number))
	if url_type == "search":
		response = urllib2.urlopen("https://www.devrant.io/search?term=" + url_arg + "&sort=" + sort_type)
	raw_html = response.read()
	soup = BeautifulSoup(raw_html, "lxml")
	result_set = soup.find_all("li", class_="rant-comment-row-widget")
	for result in result_set:
		post_text = result.find("div", class_="rantlist-title-text")
		vote_count = result.find("div", class_="votecount")
		post_id_link = result.find("a", class_="rantlist-bglink")
		post_id_stripped = post_id_link.get("href")[-6:] #post ids aren't fixed length, doesn't work on older posts. Gonna fix this.
		timestamp = result.find(text=lambda text:isinstance(text, Comment))
		tags = result.find("div", class_="rantlist-tags")
		print("Vote Count: " + vote_count.get_text())
		print("Posted " + BeautifulSoup(timestamp.extract(), "lxml").get_text() + " ago")
		print("Rant ID: " + post_id_stripped)
		print(post_text.get_text())
		if len(tags.get_text()) > 1:
			print("Tags: " + tags.get_text().strip().replace("\n", ", "))
		if result.img != None:
			#print(result.img['src'])
			img_parse(result.img['src'])
		for i in range(0, get_terminal_width()):
			print("=",end='')
		print("")


def parse_rant(rant_id):
	response = urllib2.urlopen("https://www.devrant.io/rants/" + rant_id)
	raw_html = response.read()
	soup = BeautifulSoup(raw_html, "lxml")
	result_set = soup.find_all("li", class_="reply-row rant-comment-row-widget")
	for result in result_set:
		post_text = result.find("div", class_="rantlist-title")
		vote_count = result.find("div", class_="votecount")
		print("Vote Count: " + vote_count.get_text())
		print("Posted by " + result.find("div", class_="rant-username").get_text() + " " + result.find("div", class_="timestamp").get_text() + " ago")
		print("Post ID: " + result.attrs['data-id'])
		if result.img != None:
			img_parse(result.img['src'], True)
		print(post_text.get_text())

		for i in range(0, get_terminal_width()):
			print("=",end='')
		print("")


def img_parse(img_url, avatar=False):
	file = cStringIO.StringIO(urllib.urlopen(img_url).read())
	remote_img = Image.open(file)
	if avatar is True:
		img = img2txt.load_and_resize_image(file, True, 20, 1.0)
	else:
		img = img2txt.load_and_resize_image(file, True,(get_terminal_width()/3)*2, 1.0)
	pixel = img.load()
	width, height = img.size
	sys.stdout.write("\x1b[49m")
	sys.stdout.write("\x1b[K")
	sys.stdout.write(ansi.generate_ANSI_from_pixels(pixel, width, height, None)[0])
	sys.stdout.write("\x1b[0m\n")