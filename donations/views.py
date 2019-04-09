from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from events.models import Event
from django.core.files.storage import FileSystemStorage
from . models import Receiver
# Create your views here.

def index(request):
	return HttpResponse("Done")  

def donor(request,eventId):
	print(eventId)
	eventObj = Event.objects.get(eventId=eventId)
	receiverObjs = Receiver.objects.all().filter(eventId = eventObj)
	listOfReceivers = []
	for obj in receiverObjs:
		di = {}
		di['userName'] = obj.userName.username
		di['comments'] = obj.comments
		listOfReceivers.append(di)
	print(listOfReceivers)
	return render(request,"donor.html",{'listOfReceivers':listOfReceivers,'eventId':eventId})

def receiver(request,eventId):
	print(eventId)
	eventObj = Event.objects.get(eventId=eventId)
	print(eventObj)
	return render(request,"receiver.html",{'eventId':eventId})

def receiverSubmit(request,eventId):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        bank = request.POST.get('bank')
        comments = request.POST.get('comments')
        print(uploaded_file_url)
        print(bank)
        print(comments)
        eventObj = Event.objects.get(eventId=eventId)
        Receiver.objects.create(eventId=eventObj,userName=request.user,fileName=filename,bankDetails=bank,comments=comments)



    return redirect('/events/'+eventId)
