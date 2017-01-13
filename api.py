import urllib2
import json

#TODO surround these functions within try catch block to catch Http errors, if else approach won't work obviously

def login(username, password):
	authorization = {} 
	request = urllib2.Request("https://www.devrant.io/api/users/auth-token", "username=" + username  + "&password=" + password  + "&plat=3&app=3")
	response = urllib2.urlopen(request)
	raw_json = response.read()
	json_object =  json.loads(raw_json)

	authorization['success'] = json_object['success']
	auth_token = json_object['auth_token']
	authorization['token_id'] = str(auth_token['id'])
	authorization['token_key'] = str(auth_token['key'])
	authorization['token_expiration_epoch'] = str(auth_token['expire_time'])
	authorization['user_id'] = str(auth_token['user_id'])

	if authorization['success']:
		return authorization
	else:
		return False

def post_comment(rant_id, token_key, token_id, user_id, comment):
	request = urllib2.Request("https://www.devrant.io/api/devrant/rants/" + rant_id + "/comments", "token_id=" + token_id + "&token_key=" + token_key + "&user_id=" + user_id + "&comment=" + comment + "&plat=3&app=3")
	response = urllib2.urlopen(request)
	raw_json = response.read()
	json_object =  json.loads(raw_json)

	if json_object['success']:
		return True
	else:
		return False

def delete_comment(post_id, token_key, token_id, user_id):
	request = urllib2.Request("https://www.devrant.io/api/comments/" + post_id + "?token_id=" + token_id + "&token_key=" + token_key + "&user_id=" + user_id + "&plat=3&app=3" ,"token_id=" + token_id + "&token_key=" + token_key + "&user_id=" + user_id + "&plat=3&app=3" )
	request.get_method = lambda: 'DELETE'
	raw_json = response.read()
	json_object =  json.loads(raw_json)

	if json_object['success']:
		return True
	else:
		return False

def vote_rant(rant_id, token_key, token_id, user_id, vote):
	#vote = 1 -> upvote, vote = -1 -> downvote, vote = 0 -> cancel vote
	request = urllib2.Request("https://www.devrant.io/api/devrant/rants/" + rant_id + "/vote", "token_id=" + token_id + "&token_key=" + token_key + "&user_id=" + user_id + "&vote=" + vote + "&plat=3&app=3")
	response = urllib2.urlopen(request)
	raw_json = response.read()
	json_object = json.loads(raw_json)
	
	if json_object['success']:
		return True
	else:
		return False

def vote_post(post_id, token_key, token_id, user_id, vote):
	#vote = 1 -> upvote, vote = -1 -> downvote, vote = 0 -> cancel vote
	request = urllib2.Request("https://www.devrant.io/api/comments/" + post_id + "/vote", "token_id=" + token_id + "&token_key=" + token_key + "&user_id=" + user_id + "&vote=" + vote + "&plat=3&app=3")
	response = urllib2.urlopen(request)
	raw_json = response.read()
	json_object = json.loads(raw_json)
	
	if json_object['success']:
		return True
	else:
		return False

#authorization = login("username", "password")

#post_comment("380308", authorization['token_key'], authorization['token_id'], authorization['user_id'], "Don't mind me, testing the devRant API")

#post_id_temp = raw_input("Post ID?\n")

#delete_comment(post_id_temp, authorization['token_key'], authorization['token_id'], authorization['user_id'])

#vote_post("380800", authorization['token_key'], authorization['token_id'], authorization['user_id'], "1")