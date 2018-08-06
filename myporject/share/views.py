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


# 首页
def index(request):
    ob = Upload.objects.all()
    # 分页
    paginator = Paginator(ob, 5)  # 设置每页显示5条数据
    p = int(request.GET.get('p', 1))
    file_list = paginator.page(p)

    context = {'content':file_list, 'p':p}

    return render(request,'content.html',context)
    # return render(request,'content.html',{"content":ob})


# 上传文件
def upload(request):
	file = request.FILES.get("file")
	name = file.name
    # 写入文件到静态文件夹
	with open('static/upload/' + name, 'wb') as f:
		f.write(file.read())
    # 给每个文件生成一个随机号
	code = ''.join(random.sample(string.digits, 8))
    # 实例化
	up = Upload()
    # 文件信息写入数据库
	up.path = 'static/upload/' + name  # 数据库内仅存储文件路径
	up.name = name
	up.Filesize = size
	up.code = code
	up.PCIP = str(request.META['REMOTE_ADDR'])

	up.save()

	return HttpResponsePermanentRedirect("/index/")  # 重定向到首页

# 搜索
def search(request):
    code = request.GET.get("kw")  # 获取关键字
    u = Upload.objects.filter(name__contains=str(code))  # 搜索范围(文件名)
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


