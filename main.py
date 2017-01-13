#!/usr/bin/env python

from api import *
from parser import *
import getpass

#initial page number of feed
page_number = 1

#check if user wants to quit
want_to_quit = False

#initial login state
user_logged_in = False

#check if user in rant details
in_rant_page = False

#check if user wants to login
want_to_login = raw_input("Do you want to login? You need to be logged on to post and vote.(y/n): ")
if want_to_login.startswith("y"):
	username = raw_input("Username / E-mail: ")
	password = getpass.getpass("Password: ")
	while user_logged_in is False:
		authorization = login(username, password)
		if authorization is not False:
			print("Successfully logged in!")
			user_logged_in = True
		else:
			print("Something went wrong, probably wrong username/password combination.")
else:
	print "It's OK, you can still enjoy devRant!"

#parsing 1st page of feed
parse_feed()

while want_to_quit is False:
	if user_logged_in:
		nav_prompt = "V for next page, Y for previous page, Q to exit, S <term> to search, R <rant ID> to browse a rant, U <rant ID> to upvote, D <rant ID> to downvote\n"
	if user_logged_in is False:
		nav_prompt = "V for next page, Y for previous page, Q to exit, S <term> to search, R <rant ID> to browse a rant\n" 
	if in_rant_page is True and user_logged_in is False:
		nav_prompt = "Q to exit, S <term> to search, R <rant ID> to browse a rant, B to back\n"
	if in_rant_page is True and user_logged_in is True:
		nav_prompt = "Q to exit, S <term> to search, U <rant ID> to upvote, D <rant ID> to downvote, A <comment> to add comment, B to back\n"
	nav_option = raw_input(nav_prompt)

	if nav_option == "v" or nav_option == "V":
		page_number += 1
		parse_feed("feed", "a", page_number)

	if nav_option == "y" or nav_option == "Y":
		page_number -= 1
		if page_number == 0:
			page_number = 1
		parse_feed("feed", "a", page_number)

	if nav_option == "q" or nav_option == "Q":
		want_to_quit = True

	if nav_option =="b" or nav_option == "B":
		parse_feed("feed", "a", page_number)
		in_rant_page = False

	if nav_option.startswith("s") or nav_option.startswith("S"):
		search_term = nav_option.split()[1]
		parse_feed("search", nav_option)


	if nav_option.startswith("r") or nav_option.startswith("R"):
		rant_id = nav_option.split()[1]
		parse_rant(rant_id)
		in_rant_page = True

	if nav_option.startswith("u") or nav_option.startswith("U"):
		post_id = nav_option.split()[1]
		if in_rant_page:
			vote_post(post_id, authorization['token_key'], authorization['token_id'], authorization['user_id'], "1")
		else:
			vote_rant(post_id, authorization['token_key'], authorization['token_id'], authorization['user_id'], "1")

	if nav_option.startswith("d") or nav_option.startswith("D"):
		post_id = nav_option.split()[1]
		if in_rant_page:
			vote_post(post_id, authorization['token_key'], authorization['token_id'], authorization['user_id'], "1")
		else:
			vote_rant(post_id, authorization['token_key'], authorization['token_id'], authorization['user_id'], "1")

	if nav_option.startswith("a") or nav_option.startswith("A"):
		comment = nav_option[2:]
		post_comment(rant_id, authorization['token_key'], authorization['token_id'], authorization['user_id'], comment)



print("Farewell!")
