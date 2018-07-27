from django.shortcuts import render
from django.http import HttpResponse
from .models import Upload
from django.http import HttpResponsePermanentRedirect
from django.core.paginator import Paginator
import os
import time
import random
import string
import json


def index(request):
    ob = Upload.objects.all()
    # 分页
    paginator = Paginator(ob, 5)
    p = int(request.GET.get('p', 1))
    file_list = paginator.page(p)

    context = {'content':file_list, 'p':p}

    return render(request,'content.html',context)
    # return render(request,'content.html',{"content":ob})


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
    # print('code', code)
    # code = str(code)
    u = Upload.objects.filter(name__contains=str(code))
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
            # print(data)
    return HttpResponse(json.dumps(data),content_type="application/json")


