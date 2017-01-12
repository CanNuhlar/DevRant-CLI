#!/usr/bin/env python
from __future__ import print_function
import urllib2
import os
from bs4 import BeautifulSoup, Comment
from img2ascii import *

page_number = 1
want_to_quit = False
def get_terminal_width():
	columns = os.popen('stty size', 'r').read().split()[1]
	return int(columns)

def parse_content(url_type="feed", url_arg="", page_number=1):
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
		print("ID: " + post_id_stripped)
		print(post_text.get_text())
		if len(tags.get_text()) > 1:
			print("Tags: " + tags.get_text().strip().replace("\n", ", "))
		if result.img != None:
			#print(result.img['src'])
			print_ascii_from_url(result.img['src'])
		for i in range(0, get_terminal_width()):
			print("=",end='')
		print("")

parse_content()

while want_to_quit is False:
	navigation_key = raw_input("V for next page, Y for previous page, Q to exit\n")

	if navigation_key == "v" or navigation_key == "V":
		page_number += 1
		parse_content("feed", "a", page_number)
	if navigation_key == "y" or navigation_key == "Y":
		page_number -= 1
		if page_number == 0:
			page_number = 1
		parse_content("feed", "a", page_number)
	if navigation_key == "q" or navigation_key == "Q":
		want_to_quit = True
	#else:
		#parse_content("search", navigation_key)

print("Farewell!")
