from __future__ import print_function
import urllib2
import os
from bs4 import BeautifulSoup, Comment
from img2ascii import *

def get_terminal_width():
	columns = os.popen('stty size', 'r').read().split()[1]
	return int(columns)

def parse_feed(url_type="feed", url_arg="", page_number=1):
	if url_type == "feed":
		response = urllib2.urlopen("http://devrant.io/feed/algo/" + str(page_number))
	if url_type == "search":
		response = urllib2.urlopen("https://www.devrant.io/search?term=" + url_arg)
	raw_html = response.read()
	soup = BeautifulSoup(raw_html)
	result_set = soup.find_all("li", class_="rant-comment-row-widget")
	for result in result_set:
		post_text = result.find("div", class_="rantlist-title-text")
		vote_count = result.find("div", class_="votecount")
		post_id_link = result.find("a", class_="rantlist-bglink")
		post_id_stripped = post_id_link.get("href")[-6:]
		timestamp = result.find(text=lambda text:isinstance(text, Comment))
		tags = result.find("div", class_="rantlist-tags")
		print("Vote Count: " + vote_count.get_text())
		print("Posted " + BeautifulSoup(timestamp.extract()).get_text() + " ago")
		print("Rant ID: " + post_id_stripped)
		print(post_text.get_text())
		if len(tags.get_text()) > 1:
			print("Tags: " + tags.get_text().strip().replace("\n", ", "))
		if result.img != None:
			#print(result.img['src'])
			print_ascii_from_url(result.img['src'])
		for i in range(0, get_terminal_width()):
			print("=",end='')
		print("")


def parse_rant(rant_id):
	response = urllib2.urlopen("https://www.devrant.io/rants/" + rant_id)
	raw_html = response.read()
	soup = BeautifulSoup(raw_html)
	result_set = soup.find_all("li", class_="reply-row rant-comment-row-widget")
	for result in result_set:
		post_text = result.find("div", class_="rantlist-title")
		vote_count = result.find("div", class_="votecount")
		print("Vote Count: " + vote_count.get_text())
		print("Posted by " + result.find("div", class_="rant-username").get_text() + " " + result.find("div", class_="timestamp").get_text() + " ago")
		print("Post ID: " + result.attrs['data-id'])
		if result.img != None:
			print_ascii_from_url(result.img['src'])
		print(post_text.get_text())

		for i in range(0, get_terminal_width()):
			print("=",end='')

