from django.shortcuts import render
from django.http import HttpResponse
from .models import Upload
from django.http import HttpResponsePermanentRedirect
import os
import time
import random
import string
import json


def index(request):
    ob = Upload.objects.all()
    # return render(request, "index.html",{})
    return render(request,'content.html',{"content":ob})


def upload(request):
	file = request.FILES.get("file")
	# print(file,type(file))
	name = file.name
	# print(name, type(name))
	size = int(file.size) // 1024
	# print(size)
	with open('static/upload/' + name, 'wb') as f:
		f.write(file.read())
	code = ''.join(random.sample(string.digits, 8))

	up = Upload()
	up.path = 'static/upload/' + name
	up.name = name
	up.Filesize = size
	up.code = code
	up.PCIP = str(request.META['REMOTE_ADDR'])

	up.save()


	# return HttpResponse("upload")
	return HttpResponsePermanentRedirect("/index/")


def search(request):
    # return HttpResponse('search')
    code = request.GET.get("kw")
    print('code', code)
    u = Upload.objects.filter(name=str(code))
    data = {}
    if u :
        for i in range(len(u)):
            u[i].DownloadDocount +=1
            u[i].save()
            data[i]={}
            data[i]['download'] = u[i].DownloadDocount
            data[i]['filename'] = u[i].name
            data[i]['id'] = u[i].id
            data[i]['ip'] = str(u[i].PCIP)
            data[i]['size'] = u[i].Filesize
            data[i]['time'] = str(u[i].Datatime.strftime('%Y-%m-%d %H:%M:%S'))
            data[i]['key'] = u[i].code
            print(data)
    return HttpResponse(json.dumps(data),content_type="application/json")


# def display(request, code):



def upload_fuction(request):
	myfile = request.FILES.get("img", None)
	filename = str(time.time())+"."+myfile.name.split(".").pop()
	up = open("./static/public/img/"+filename,"wb+")
	for chunk in myfile.chunks():
		up.write(chunk)
	up.close()
	return "/static/upload/img/"+filename
