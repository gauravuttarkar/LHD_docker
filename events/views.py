from django.shortcuts import render, redirect
from predicthq import Client
from django.http import HttpResponse
import requests
from events.models import SafeLocation, DangerLocation, HelpLocation, Event\
							,UserComments
from newsapi import NewsApiClient							
from django.contrib.auth.models import User
# Create your views here.

def index(request):
	url = "https://api.predicthq.com/v1/events/"
	ACCESS_TOKEN = "_Kr6HjOROBxnjng15d3Z5hU2f1OqVszKVOwJYXpf"
	payload={
	'sort':'rank',
	'count':'50',
	'category' : 'disasters',
	'labels' : ['disaster','fire']
	}
	headers={
	'Accept': 'application/json',
	'Authorization': "Bearer " + ACCESS_TOKEN
	}
	r = requests.get(url, params=payload,headers=headers)
	# phq = Client(access_token=ACCESS_TOKEN)
	results = r.json()['results']
	#print(results)
	count = 0
	for i in results:
		if 'vehicle-accident' in i['labels']:
			results.pop(count)	
		count = count + 1

	for i in results:
		print(i)
		print("*"*100)	
	# for event in phq.events.search(category="disasters",state="active"):
	#     print(event.description, event.category, event.title, event.start.strftime('%Y-%m-%d'))
	return render(request,'listOfEvents.html',{'events':results})

def eventDetail(request,eventId):
	url = "https://api.predicthq.com/v1/events/"
	ACCESS_TOKEN = "_Kr6HjOROBxnjng15d3Z5hU2f1OqVszKVOwJYXpf"
	payload={
	'id' : eventId
	}
	headers={
	'Accept': 'application/json',
	'Authorization': "Bearer " + ACCESS_TOKEN
	}
	r = requests.get(url, params=payload,headers=headers)
	#print(eventId)
	results = r.json()['results']
	#print(results)
	results = results[0]
	longi = results['location'][0]
	lat = results['location'][1]
	api = "147b79daa29884e1dab8fac91b7526d6"
	#print(type(lat))
	url = "http://api.openweathermap.org/data/2.5/weather?lat="+str(lat)+"&lon="+str(longi)+"&appid="+api;
	response = requests.get(url)
	#print(type(response))
	#print(response.text)
	res = response.json()
	#print(lat,longi)
	#print(data)
	temp = res['main']['temp']
	pressure = res['main']['pressure']
	humidity = res['main']['humidity']
	temp_min = res['main']['temp_min']
	temp_max = res['main']['temp_max']
	windspeed = res['wind']['speed']
	try:
		winddeg = res['wind']['deg']
	except:
		winddeg = None	
	mainweather	= res['weather'][0]['main']
	description = res['weather'][0]['description']

	# print(temp)
	# print(mainweather)
	# print(description)
	safeLocation = []
	dangerLocation = []
	helpLocation = []

	safeObj = SafeLocation.objects.all().filter(eventId=eventId)
	safeList = []
	for i in safeObj:
		di = {}
		di['latitude'] = float(i.latitude)
		di['longitude'] = float(i.longitude)
		# userObj = User.objects.get(id=i.userName)
		di['userName'] = i.userName.username
		safeList.append(di)
	#print(safeList)	


	dangerObj = DangerLocation.objects.all().filter(eventId=eventId)
	dangerList = []
	for i in dangerObj:
		di = {}
		di['latitude'] = float(i.latitude)
		di['longitude'] = float(i.longitude)
		#userObj = User.objects.get(id=i.userName)
		di['userName'] = i.userName.username
		safeList.append(di)
	#print(dangerList)	

	helpObj = HelpLocation.objects.all().filter(eventId=eventId)
	helpList = []
	for i in helpObj:
		di = {}
		di['latitude'] = float(i.latitude)
		di['longitude'] = float(i.longitude)
		#userObj = User.objects.get(id=i.userName)
		di['userName'] =  i.userName.username
		safeList.append(di)
	#print(helpList)	
	

	try:
		obj = Event.objects.get(eventId=eventId)
	except:
		obj = Event.objects.create(eventId=eventId)
		obj.save()

	comments = UserComments.objects.all().filter(eventId=eventId)
	#print(type(comments))
	newsapi = NewsApiClient(api_key='e24ec206782a42b281d998e51d1dc9ac')

	query = results['title'].split('-')

	queries = query[0]+' AND ' + query[-1]
	print(queries)
	new_query = query[1:-1]

	sources = ''
	string = ""
	for q in new_query:
		string = string + str(q)


	# if len(query) == 4:
	# 	if string.replace(' ','') == "United-Kingdom":
	# 		sources = "the-guardian-uk"
	# 		country= "gb"		
	# 	if string.replace(' ','') == "Australia":
	# 		sources = "the-guardian-au"
	# 		country = "au"	
	# 	if query[-1].replace(' ','') == "India":
	# 		sources = "the-times-of-india"
	# 		country = "in"
	# 	if query[-1].replace(' ','')	== "China":
	# 		sources = "xinhua-net"
	# 		country = "cn"	


	all_articles = newsapi.get_everything(q=queries,
                                      sources='bbc-news,reddit-r-all,the-new-york-times,al-jazeera-english,the-times-of-india,the-hindu,google-news',
                                      language='en',
                                      sort_by='relevancy',
                                      )
	print(type(all_articles))
	print(all_articles)
	#print(all_articles)
	
	
	print(results['id'])
	ACCESS_TOKEN = "AAAAAAAAAAAAAAAAAAAAANkH9AAAAAAAorENrW%2Bt7Y4uQwZMJr43ZcWTIaY%3DXWlT3Xuacow4mmAvkKEC4EPdjY0TTL9VClG3PU8vHSR5nBj0v9"
	url = "https://api.twitter.com/1.1/search/tweets.json"
	headers={
	'Accept': 'application/json',
	'Authorization': "Bearer " + ACCESS_TOKEN,
	#'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8.',
	
	}
	payload={
	'grant_type':'client_credentials',
	'q':'#disaster',
	'geocode': str(lat)+","+str(longi)+",50mi"
	}
	# r = requests.get(url,headers=headers,params=payload)
	# tweets = r.json()
	# #print(tweets)
	# tweets = tweets['statuses']
	# #print(tweets)
	# tweetList = []
	# print(longi,lat)
	# for i in tweets:
	# 	di = {}
	# 	di['created_at'] = i['created_at']
	# 	di['text'] = i['text']
	# 	di['user'] = i['user']['name']
	# 	tweetList.append(di)
	# 	#print(i)
	# 	#print(100*'-')
	# print(tweetList)	

	return render(request,'eventDetail.html',{'event':results,
											  'weather':[mainweather,description],
											  'temp':temp,
											  'pressure':pressure,
											  'humidity':humidity,
											  'windspeed':windspeed,
											  'winddeg': winddeg,
											  'safeLocation':safeList,
											  'dangerLocation': dangerObj,
											  'helpLocation': helpObj,
											  'comments': comments,
											  'articles': all_articles,
											  #'tweets': tweetList
												})

def mapMarker(request):
	lat = request.POST.get('lat')
	lng = request.POST.get('lng')
	eventId = request.POST.get('eventId')
	color = request.POST.get('colour')
	print(request.POST)
	print(request.user)
	if request.user:
		if color == '0':
			obj = Event.objects.get(eventId=eventId)
			obj = HelpLocation.objects.create(eventId=obj,
										latitude=lat,
										longitude=lng,
										userName=request.user)
			obj.save()
		if color == '1':
			print('Red')
			obj = Event.objects.get(eventId=eventId)
			obj = DangerLocation.objects.create(eventId=obj,
										latitude=lat,
										longitude=lng,
										userName=request.user
										)
			obj.save()
		if color == '2':
			obj = Event.objects.get(eventId=eventId)
			obj = SafeLocation.objects.create(eventId=obj,
										latitude=lat,
										longitude=lng,
										userName=request.user
										)
			obj.save()	
				
	#SafeLocation.objects.create()
	return redirect("/events/"+eventId)

def comments(requests):
	print(requests.POST)
	eventId = requests.POST.get('eventId')
	comment = requests.POST.get('comment')
	eventObj = Event.objects.get(eventId=eventId)

	commObj = UserComments.objects.create(userName=requests.user,eventId=eventObj,userComment=comment)
	commObj.save()
	return redirect("/events/"+eventId)

def twitter(request):
	print("Inside twitter")
	# eventId = request.POST.get('eventId')
	# base64 = "RDVZaDBCSjY3NHhtbkt1cXV0ajU5dk80dTphVFZNS2xxU2tZcmpEaFdBMDVYajliWG1vcUNxckhteGhyNm5oUGZqNnZ3OWlQeGhqUQ=="
	# url = "https://api.twitter.com/oauth2/token"
	# payload={
	# 'grant_type':'client_credentials',
	# }
	# headers={
	# 'Accept': 'application/json',
	# 'Authorization': "Basic " + base64,
	# 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8.',
	
	# }

	# r = requests.post(url,params=payload,headers=headers)
	ACCESS_TOKEN = "AAAAAAAAAAAAAAAAAAAAANkH9AAAAAAAorENrW%2Bt7Y4uQwZMJr43ZcWTIaY%3DXWlT3Xuacow4mmAvkKEC4EPdjY0TTL9VClG3PU8vHSR5nBj0v9"
	url = "https://api.twitter.com/1.1/search/tweets.json"
	headers={
	'Accept': 'application/json',
	'Authorization': "Bearer " + ACCESS_TOKEN,
	#'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8.',
	
	}
	payload={
	'grant_type':'client_credentials',
	'q':'#disaster',
	'geocode': "37.781157,-122.398720,100mi"
	}
	r = requests.get(url,headers=headers,params=payload)
	tweets = r.json()
	tweets = tweets['statuses']
	#print(tweets)
	tweetList = []
	for i in tweets:
		di = {}
		di['created_at'] = i['created_at']
		di['text'] = i['text']
		di['user'] = i['user']['name']
		tweetList.append(di)
		#print(i)
		#print(100*'-')
	for i in tweetList:
		print(i)
	return HttpResponse("Twitter")






