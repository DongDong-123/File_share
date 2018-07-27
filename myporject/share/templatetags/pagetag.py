from django import template
register = template.Library()

from django.utils.html import format_html

@register.simple_tag
def cheng(var1,var2):
    res = float(var1) * float(var2)
    return '%.2f'%res
    
@register.simple_tag
def PageShow(count,request):
    # 当前页码数,默认为1
    p = int(request.GET.get('p',1))
    begin = p - 4
    end = p + 5

    if p > count-5:
        begin = count - 9
        end = count

    if p < 5:
        begin = 1
        end = 10

    if count < 10:
        begin = 1
        end = count

    # 获取当前请求的url
    url = request.path
    # 获取当前请求中的参数 
    # <QueryDict: {'p': ['26'], 'b': ['2'], 'a': ['1']}>
    # &a=1&b=2
    # 去除参数中的p
    args = ''
    for k,v in request.GET.items():
        if k != 'p':
            args += '&'+k+'='+v
 
    s = ''
    # 首页
    s += '<li><a href="{url}?p={v}{args}">首页</a></li>'.format(v=1,url=url,args=args)
    # 判断上一页
    if p == 1:
        s += '<li><a href="{url}?p={v}{args}">上一页</a></li>'.format(v=1,url=url,args=args)
    else:
        s += '<li><a href="{url}?p={v}{args}">上一页</a></li>'.format(v=p-1,url=url,args=args)
    # 循环页码数
    for x in range(begin,end+1):
        if x == p:
            s += '<li class="am-active"><a href="{url}?p={v}{args}">{v}</a></li>'.format(v=x,url=url,args=args)
        else:
            s += '<li ><a href="{url}?p={v}{args}">{v}</a></li>'.format(v=x,url=url,args=args)
    # 判断下一页
    if p == count:
        s += '<li><a href="{url}?p={v}{args}">下一页</a></li>'.format(v=count,url=url,args=args)
    else:
        s += '<li><a href="{url}?p={v}{args}">下一页</a></li>'.format(v=p+1,url=url,args=args)
    # 尾页
    s += '<li><a href="{url}?p={v}{args}">尾页</a></li>'.format(v=count,url=url,args=args)

    # 总页数
    s += '<li>共{v}页</li>'.format(v=count)

    return format_html(s)




# def PageShow(count, request):
# 	p = int(request.GET.get('p', 1))
# 	begin = p - 4
# 	end = p + 5
# 	if p > count - 5:
# 		begin = count - 9
# 		end = count 

# 	if p < 5:
# 		begin = 1
# 		end = 10

# 	if count < 10:
# 		begin = 1
# 		end = count

# 	# args = ''
# 	for i in range(begin, end + 1):
# 		print(i)

# 	return i

