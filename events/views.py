from django.shortcuts import render, redirect
from predicthq import Client
from django.http import HttpResponse
import requests
from events.models import SafeLocation, DangerLocation, HelpLocation, Event\
							,UserComments
from newsapi import NewsApiClient							
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from . import text2info , audio2text
import googlemaps
# Create your views here.

def index(request):
	url = "https://api.predicthq.com/v1/events/"
	ACCESS_TOKEN = "ZFzePtaHlBI8Vskwq1e5bLVauSyc6f"
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
	#print(r)
	# phq = Client(access_token=ACCESS_TOKEN)
	results = r.json()['results']
	#print(results)
	count = 0
	for i in results:
		if 'vehicle-accident' in i['labels']:
			results.pop(count)	
		count = count + 1

	#for i in results:
		#print(i)
		#print("*"*100)	
	# for event in phq.events.search(category="disasters",state="active"):
	#     print(event.description, event.category, event.title, event.start.strftime('%Y-%m-%d'))
	return render(request,'listOfEvents.html',{'events':results})

def eventDetail(request,eventId):
	url = "https://api.predicthq.com/v1/events/"
	ACCESS_TOKEN = "ZFzePtaHlBI8Vskwq1e5bLVauSyc6f"
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

	return render(request, 'eventDetail.html', {'event':results,
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
											  #'donations':receiver,
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

def audio_submit(request,converted_text, eventId):
    res = text2info.get_info(converted_text)
    print("here ", res)
    gmaps = googlemaps.Client(key='AIzaSyC5C381MWOwCKW4Y-CP0KVptAcY4FqryAU')
    
    geocode_result = gmaps.geocode(res['Address'])
    print(geocode_result)
    # print(geocode_result)
    Address = res['Address']
    x = geocode_result[0]['geometry']['location']['lat']
    y = geocode_result[0]['geometry']['location']['lng']
    # intensity = res['Intensity']
    # Remarks = res['Remark']
    eventObj = Event.objects.get(eventId=eventId)
    DangerLocation.objects.create(userName=request.user,eventId=eventObj,latitude=x,longitude=y)
    # map.save() 


def audio(request,eventId):
    if request.method == 'POST' and request.FILES['myfile']:
        print("Inside audio upload")
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        converted_text = audio2text.get_text_from_audio(uploaded_file_url)
        audio_submit(request,converted_text, eventId)
        # file_path = os.path.join(BASE_DIR, uploaded_file_url)
        # pass_file_path(file_path)
        # index()
        print(uploaded_file_url)
        return redirect("/events/"+eventId)
        # return render(request, 'NLP/index.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })
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
	print(r)
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







