import json
import urllib.request
import datetime
import random
from textblob import TextBlob
#ATTENTION---fields=reactions.type(LIKE).limit(0).summary(total_count).as(like)  for getting likes of the comments if required----- 
def create_comments_url(graph_url,post_id,APP_ID,APP_Secret):
	comments_args = post_id + "/comments/?limit=5000&summary=true&access_token=" + APP_ID + "|" + APP_Secret
	comments_url = graph_url + comments_args

	#print (comments_url)
	return comments_url


def get_comments_data(comments_url,comment_Data,post_id,likes,pg_url):
	comments = render_to_json(comments_url)["data"]

	for comment in comments:
		try:
			current_comments = [comment["created_time"],comment["message"],comment["from"]["name"],likes,pg_url,comment["id"],post_id]
			comment_Data.append(current_comments)
			#comment_Data[commen["id"]] = {'Date':comment["created_time"],'Name':comment["from"]["Name"],'Text':comment['message']}
		except Exception:
			current_comments = ["error","error","error","error"]
			print ("error aagya")

	try:
		next_page = comments["paging"]["next"]
	except Exception:
		next_page = None

	if next_page is not None:
		get_comments_data(graph_url,comment_Data,post_id)
	else:
		return comment_Data
def create_post_url(graph_url,APP_ID,APP_Secret):
	post_arg = "/posts/?key=value&access_token=" + APP_ID + "|" + APP_Secret
	post_url = graph_url + post_arg

	#print post_url
	return post_url

def render_to_json(graph_url):
	web_response = urllib.request.urlopen(graph_url)
	readable_page = web_response.read()
	json_data = json.loads(readable_page.decode())

	#print json_data
	return json_data

def scrape_by_date(graph_url,date,post_data,APP_ID,APP_Secret):
	#print "Enter the function"
	page_posts = render_to_json(graph_url)
	next_page = page_posts["paging"]["next"]

	page_posts = page_posts["data"]

	collecting = True

	for post in page_posts:
		try:
			likes_count = get_likes_count(post["id"],APP_ID,APP_Secret)
			#likes_count=65
	#		print post["created_time"]
			current_post = [post["id"],post["message"],likes_count,post["created_time"]]
	#		print "mid"
		except Exception:
			current_post = ["error","error","error","error"]
	#		print "err"

		if current_post[3]!= "error":
	#		print date
	#		print current_post[3]

			if date <= current_post[3]:
				post_data.append(current_post)

			elif date > current_post[3]:
	#			print "Done collecting"
				collecting = False
				break

	#if collecting == True:
		#scrape_by_date(next_page,date,post_data,APP_ID,APP_Secret)
	return post_data


def get_likes_count(post_id,APP_ID,APP_Secret):
	graph_url = "https://graph.facebook.com/"
	likes_args = post_id + "/likes?summary=true&key=value&access_token="+APP_ID+ "|" + APP_Secret
	#print "3"
	likes_url = graph_url + likes_args
	#print likes_url
	likes_json = render_to_json(likes_url)

	count_likes = likes_json["summary"]["total_count"]
	#print (count_likes)
	return count_likes

def main(page):

	#with open('%s_comment_data.txt'% page ,'a') as file:
	#
	APP_ID = "1257325031043360"
	APP_Secret = "d69346c2e19e86af6756e956906ca2fa" # DO NOT SHARE WITH ANYONE!

	#graph_url1 = "https://graph.facebook.com/nytimes/?key=value&access_token=" + APP_ID + "|" + APP_Secret
	graph_url = "https://graph.facebook.com/"
	graph_url1 = graph_url + page
	pg_url = "https://www.facebook.com/"
	pg_url = pg_url + page
	#json_fburl = create_post_url(graph_url,APP_ID,APP_Secret)
	#json_fbpage = render_to_json(graph_url1)
	last_crawl = datetime.datetime.now()- datetime.timedelta(weeks=1)
	last_crawl = last_crawl.isoformat()
	print (last_crawl)
	#print json_fbpage
	post_url = create_post_url(graph_url1,APP_ID,APP_Secret)
	json_postdata = render_to_json(post_url)

	#next_page =  json_postdata["paging"]["next"]
	json_fbpost = json_postdata['data']

	print ("Script is Running be Patient :-p \n")
	#i=1
	comment_Data=[	];
	for post in json_fbpost:
		try:
			#print likes
			if(last_crawl <= post["created_time"]):
				comment_url = create_comments_url(graph_url,post["id"],APP_ID,APP_Secret)
				likes = get_likes_count(post["id"],APP_ID,APP_Secret)
				comments = get_comments_data(comment_url,comment_Data,post["id"],likes,pg_url)
				print (post["created_time"])
			#print (post["message"])
				#print (post["created_time"])
			#print ("\n")
		except Exception:
			print ("Error")
	#post_data = scrape_by_date(post_url,last_crawl,post_data,APP_ID,APP_Secret)
	data = {}
	rn = 0
	for p in comment_Data:
		a = random.randint(0,1)
		rn=rn+1
		b = "Other"
		if (a==1):
			b = "Male"
		elif(a==0):
			b = "Female"
		test = TextBlob(p[1])
		test.sentiment
		polar = test.sentiment.polarity				
		data = {
				"Source":"facebook",
				"Date":p[0],
				"Text":p[1],
				"Name":p[2],
				"Username":p[2],
				"Gender":b,
				"Location":None,
				"Semantics":polar,
				"No_of_followers":None,
				"No_of_retweets":p[3],
				"Url":p[4]
				}				
		#print(p["message"])
	#s = json.dumps(data,indent = 4)
		#print(data["Text"])
		file = open('%s_comment_data.json'% page ,'a')
		json.dump(data,file,indent=4)
		file.write("\n")	
		file.close()
	print(rn)
	print ("Script Finished check text file made ")
if __name__ == "__main__":
	page = input("Enter the page you want to search :");
	main(page)