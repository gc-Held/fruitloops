from .models import PageActiveTime, BlackListedPages, UserDetails
from .serializers import PageActiveTimeSerializer, BlackListPagesSerializer, UserDetailsSerializer
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from webb import webb
from bs4 import BeautifulSoup
from io import BytesIO
from time import strftime
import urllib.parse
import json
import sys, time
import MySQLdb
import re
import hashlib


invalidTags = ['applet','base','basefont','bgsound','blink','button','dir','embed','fieldset','form','frame','frameset','ilayer','isindex','layer','legend','link','marquee','menu','meta','noframes','noscript','object','optgroup','param','plaintext','script','style','textarea','xml','img']
invalidTagsToReplace = ['nobr','a','div','p']
invalidAttrs = ['id','class','onclick','ondblclick','on*','accesskey','data','dynsrc','tabindex','aria-readonly','role','style']


@api_view(['GET'])
@csrf_exempt
def get_user_search_suggestions(request,search_str ,user, format=None):
	if request.method == 'GET':
		search_str = urllib.parse.unquote(search_str)
		search_str = re.sub(r"([=\(\)|\-!@~\"&/\\\^\$\='])", r"\\\1", search_str)
		# page_items = PageActiveTime.objects.filter(page_title__icontains= search_str,user_id = user, is_active=1, is_deleted=0).order_by('-cumulative_time')
		db=MySQLdb.connect(host="127.0.0.1",port=9306,passwd="",db="")
		cur = db.cursor()
		query = "SELECT page_title, cumulative_time FROM tart WHERE MATCH(\'@is_active 1 @user_id "+user+" @page_title \""+search_str+"\" \')  OPTION ranker=expr('sum(lcs*user_weight)*cumulative_time'), field_weights=(page_title=100) "
		print(query)
		cur.execute(query);
		rows = cur.fetchall()
		page_list = []
		suggestions_list = []
		for row in rows:
			if row[0] in suggestions_list:
				continue
			else:
				suggestions_list.append(row[0])
			page_obj = {}
			page_obj["pageTitle"] = row[0]
			page_list.append(page_obj)

		json_obj = {"lPageItems": page_list}
		json_string = json.dumps(json_obj, indent = 4*' ')
		return Response(json_string)

@api_view(['POST'])
@csrf_exempt
def register_new_user(request,format=None):
	if request.method == 'POST':
		data = request.data
		existing_users = UserDetails.objects.filter(email = data["email"])
		if(len(existing_users))!=0:
			print("User Exists")
			return Response("User Exists",  status=status.HTTP_400_BAD_REQUEST)
		hashobj = hashlib.md5()
		print(data["email"])
		hashobj.update(data["email"].encode('utf8'))
		data["user_id"] = str(hashobj.hexdigest())
		hashobj = hashlib.md5()
		hashobj.update(data["password"].encode('utf8'))
		data["password"] =str(hashobj.hexdigest())
		serializer = UserDetailsSerializer(data = data)
		print(str(data))
		if serializer.is_valid():
			serializer.save()
			json_obj = {}
			json_obj['email'] = data["email"]
			json_obj['userId'] = data["user_id"]
			json_string = json.dumps(json_obj, indent = 4*' ')
			return Response(json_string, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@csrf_exempt
def login_user(request,format=None):
	if request.method == 'PUT':
		data = request.data
		hashobj = hashlib.md5()
		hashobj.update(data["password"].encode('utf8'))
		password = str(hashobj.hexdigest())
		existing_users = UserDetails.objects.filter(email = data["email"], password = password)

		if(len(existing_users))==1:
			login_time = strftime("%Y-%m-%d %H:%M:%S")
			json_obj = {}
			json_obj['email'] = existing_users[0].email
			json_obj['userId'] = existing_users[0].user_id
			json_string = json.dumps(json_obj, indent = 4*' ')
			serializer = UserDetailsSerializer(existing_users[0], data = {'last_login' : login_time }, partial = True)
			if serializer.is_valid():
				serializer.save()
				
			return Response(json_string,  status=status.HTTP_202_ACCEPTED)

		return Response("Invalid Email/Password", status = status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@csrf_exempt
def get_collated_pages(request, user, domain, format=None):
	if request.method == 'GET':
		domain_items = PageActiveTime.objects.filter(base_url__icontains = domain, user_id= user, is_active=1, is_deleted=0).order_by('-cumulative_time')
		domain_items = domain_items.extra(
					where =[
					"UNIX_TIMESTAMP(now()) - UNIX_TIMESTAMP(fetchserver_pageactivetime.last_updated_timestamp) <=86400 ",
					" is_active = 1",
					" is_deleted= 0",
					])

		page_list = []
		for item in domain_items:
			page_obj = {}
			page_obj["pageId"] = item.page_id
			page_obj["userId"] = item.user_id
			page_obj["pageTitle"] = item.page_title
			page_obj["duration"] = item.cumulative_time
			page_obj["iconUrl"] = item.icon_url
			page_obj["baseUrl"] = item.base_url
			page_list.append(page_obj)

		json_obj = {"lPageItems": page_list}
		json_string = json.dumps(json_obj, indent = 4*' ')

		
	return Response(json_string)


@api_view(['GET'])
@csrf_exempt
def get_trending_pages(request, user, page, format=None):
	if request.method == 'GET':
		page_set = int(page) * 15
		most_viewed_pages = PageActiveTime.objects.filter(user_id = user, is_active=1, is_deleted=0)
		print(page_set)
		most_viewed_pages = most_viewed_pages.extra(
			where =[
			"UNIX_TIMESTAMP(now()) - UNIX_TIMESTAMP(fetchserver_pageactivetime.last_updated_timestamp) <=86400 ",
			" is_active = 1",
			" is_deleted= 0",
			],
			order_by = ['-cumulative_time']
			)[int(page_set): int(page_set)+15]

		page_list = []
		for item in most_viewed_pages:
			page_obj = {}
			page_obj["pageId"] = item.page_id
			page_obj["userId"] = item.user_id
			page_obj["pageTitle"] = item.page_title
			page_obj["duration"] = item.cumulative_time
			page_obj["iconUrl"] = item.icon_url
			page_obj["baseUrl"] = item.base_url
			page_list.append(page_obj)

		json_obj = {"lPageItems": page_list}
		json_string = json.dumps(json_obj, indent = 4*' ')

		
		return Response(json_string)
	


@api_view(['GET'])
@csrf_exempt
def search_links(request,user,page,search_str,format= None):
	if request.method == 'GET':
		page_set = int(page) * 15
		
		search_str = urllib.parse.unquote(search_str)
		search_items = PageActiveTime.objects.filter(page_title__icontains = search_str , user_id= user, is_active=1, is_deleted=0).order_by('-cumulative_time')[int(page_set): int(page_set)+15]
		if search_items.count() == 0:
			# search_str = search_str.replace(" ","|")
			search_str = "("+search_str+")"
			print(search_str)
			search_items = PageActiveTime.objects.filter(Q(page_title__iregex = r''+search_str +'+') | Q(page_content__iregex = r''+search_str +'+'),  user_id= user, is_active=1, is_deleted=0).order_by('-cumulative_time')[int(page_set): int(page_set)+15]

			# search_items = PageActiveTime.objects.filter(page_content__iregex = r''+search_str +'+', user_id= user, is_active=1, is_deleted=0).order_by('-cumulative_time')[int(page_set): int(page_set)+15]

		page_list = []
		for item in search_items:
			page_obj = {}
			page_obj["pageId"] = item.page_id
			page_obj["userId"] = item.user_id
			page_obj["pageTitle"] = item.page_title
			page_obj["duration"] = item.cumulative_time
			page_obj["iconUrl"] = item.icon_url
			page_obj["baseUrl"] = item.base_url
			page_list.append(page_obj)

		json_obj = {"lPageItems": page_list}
		json_string = json.dumps(json_obj, indent = 4*' ')

		
	return Response(json_string)



@api_view(['GET'])
@csrf_exempt
def get_notification_info(request,user ,format= None):
	if request.method == 'GET':
		most_viewed_page = PageActiveTime.objects.filter(user_id = user, is_active=1, is_deleted=0)
		most_viewed_page = most_viewed_page.extra(
			where =[
			"extract(epoch from now()) - extract( epoch from fetchserver_pageactivetime.last_updated_timestamp) <=86400 ",
			" is_active = 1",
			" is_deleted= 0",
			
			],
			order_by = ['-cumulative_time']

			)[:1]

		query_object =  most_viewed_page[0]
		print(query_object.page_title)
		page_obj = {}
		page_obj["pageId"] = query_object.page_id
		page_obj["userId"] = query_object.user_id
		page_obj["pageTitle"] = query_object.page_title
		page_obj["duration"] = query_object.cumulative_time
		page_obj["iconUrl"] = query_object.icon_url
		page_obj["baseUrl"] = query_object.base_url
		json_obj = {"lPageItems" : list(page_obj)}
		json_string = json.dumps(json_obj, indent = 4*' ')

		return Response(json_string, status.HTTP_202_ACCEPTED)


@api_view(['PUT'])
@csrf_exempt
def clear_user_pages(request, user,format=None):
	if request.method == 'PUT':
		data = request.data
		db=MySQLdb.connect(host="127.0.0.1",port=9306,passwd="",db="")
		cur = db.cursor()
		pages_cleared = PageActiveTime.objects.filter(user_id = data['user_id'])
		for page in pages_cleared:
			query = "DELETE FROM  tart WHERE id = "+str(page.id)+" "
			print(query)
			cur.execute(query)
		pages_cleared = PageActiveTime.objects.filter(user_id = data['user_id']).update(is_active=0, is_deleted=1)
		response = "User with id "+data['user_id']+",  "+ str(pages_cleared)+" rows have been cleared"
		return Response(response, status.HTTP_202_ACCEPTED)


@api_view(['PUT'])
@csrf_exempt
def update_black_listed_pages(request, format=None):

    if request.method == 'PUT':
        data = request.data
        db=MySQLdb.connect(host="127.0.0.1",port=9306,passwd="",db="")
        cur = db.cursor()
        print (data)
        baseUrl = data['base_url']
        print (baseUrl)
        print (data)
        blockedDomain = \
            BlackListedPages.objects.filter(user_id=data['user_id'],
                base_url=data['base_url'])[:1]

        if len(blockedDomain) != 0:
            response = 'Domain ' + baseUrl \
                + ' is already blacklist for user : ' + data['user_id']
            return Response(response, status=status.HTTP_202_ACCEPTED)
        else:
            response = 'Domain ' + baseUrl \
                + ' is being blacklisted for user : ' + data['user_id']
            print (response)
            serializer = BlackListPagesSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        userActivePages = \
            PageActiveTime.objects.filter(user_id=data['user_id'],
                base_url=data['base_url'], is_active=1)
        for page in userActivePages:
            query = 'DELETE FROM  tart WHERE id = ' + str(page.id)
            print (query)
            cur.execute(query)

        userActivePages.update(is_active=0, is_deleted=1)
        resp = str(userActivePages) \
            + ' pages have been updated for user ' + data['user_id']
        return Response(resp, status=status.HTTP_202_ACCEPTED)



			


@api_view(['POST'])
@csrf_exempt
def update_user_details(request, format=None):
			if request.method == 'POST':
				db=MySQLdb.connect(host="127.0.0.1",port=9306,passwd="",db="")
				cur = db.cursor()
				data = request.data
				if data['user_id']  ==None or data['user_id'] =='' or data['new_id']  ==None or data['new_id'] =='':
					resp = "Invalid Details"
					print (resp)
					return Response(resp , status=status.HTTP_400_BAD_REQUEST)
				page_items = PageActiveTime.objects.filter(user_id = data['user_id'], is_active=1, is_deleted=0)
				for page in page_items:
					query = "REPLACE INTO tart (id,user_id) VALUES (\'"+str(page.id)+"\',\'"+data['new_id']+"\')"
					print(query)
					cur.execute(query)
				page_items = PageActiveTime.objects.filter(user_id = data['user_id'], is_active=1, is_deleted=0).update(user_id=data['new_id'])
				resp = "User details updated"
				return Response(resp, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@csrf_exempt
def update_page_active_time(request, format=None):
			if request.method == 'POST':
				data = request.data
				db=MySQLdb.connect(host="127.0.0.1",port=9306,passwd="",db="")
				cur = db.cursor()
				new_item = False
				query = ""
				if data['user_id']  ==None or data['user_id'] =='':
					resp = "Invalid Details"
					print (resp)
					return Response(resp , status=status.HTTP_202_ACCEPTED)
				if data['page_title'] =='' or data['page_title']== 'new tab' or data['page_id'] =='' or data['page_id'].startswith('chrome://'):
					resp = "Invalid Page"
					print (resp)
					return Response(resp , status=status.HTTP_202_ACCEPTED)

				if data['icon_url'] == None or data['icon_url'] == '':
					data['icon_url'] ="http://52.26.203.91:80/icon.png"
				else:
					data['icon_url'] = "http://www.google.com/s2/favicons?domain_url="+data['icon_url']

				baseUrl = data['page_id']
				if baseUrl.startswith("https://"):
					baseUrl = baseUrl.replace("https://", "",1)
					position = baseUrl.find("/")
					if position != -1:
						baseUrl = baseUrl[0:position]
				elif baseUrl.startswith("http://"):
					baseUrl = baseUrl.replace("http://", "",1)
					position = baseUrl.find("/")
					if position != -1:
						baseUrl = baseUrl[0:position]
				data['base_url'] = baseUrl

				isBlackListed = BlackListedPages.objects.filter(user_id= data['user_id'], base_url= data['base_url'] ).exists()

				if isBlackListed:
					print("Page with url :"+data['page_id']+" is black listed for user: "+ data['user_id'])
					response = "Domain is blacklisted --- Timer not Update"
					return Response(response, status=status.HTTP_202_ACCEPTED)
				else:
					print("Page "+data['page_id']+" is not on Blacklist  for user "+data['user_id']+"! ")



				page_content = webb.download_page(data['page_id'])

				soup = BeautifulSoup(page_content,"html5lib")
				soup = BeautifulSoup(soup.html.body.encode_contents())
				[tag.decompose() for tag in soup.find_all(attrs={'id' : re.compile(r'^MathJax_')})]
				html_exception = 0
				for tag in soup():
					for attribute in invalidAttrs:
				         try:
				         	del tag[attribute]
				         except:
				         	html_exception +=1
				         	

					if tag.name in invalidTags:
						tag.decompose()
					if tag.name in invalidTagsToReplace:
						tag.replaceWithChildren()	

				print("html parsing exceptions :"+ str(html_exception))
				page_content = str(soup.prettify().encode('utf-8'))
				page_content = re.sub('[^a-zA-Z0-9\.]', ' ', page_content)
				data['page_content'] = page_content

				pageItem = PageActiveTime.objects.filter(user_id = data['user_id'], page_id = data['page_id'], is_active=1, is_deleted=0)[:1]
				# print (pageItem)
				if len(pageItem) == 0:
					new_item = True
					serializer = PageActiveTimeSerializer(data = data)
					# query = "INSERT INTO tart (page_id, user_id, page_title, cumulative_time, icon_url, base_url, is_active) VALUES (\'"+data['page_id']+"\',\'"+data['user_id']+"\',\'"+data['page_title']+"\',\'"+str(data['cumulative_time'])+"\',\'"+data['icon_url']+"\',\'"+data['base_url']+"\',\'1\')"
					
				else:
					print ("Already exists")
					data['cumulative_time'] = pageItem[0].cumulative_time  + int(data['cumulative_time'])
					id = pageItem[0].id
					print(id)
					serializer = PageActiveTimeSerializer(pageItem[0],data = data)
					# query = "REPLACE INTO tart (id,  cumulative_time) VALUES (\'"+str(id)+"\',\'"+str(data['cumulative_time'])+"\')"
					query = "UPDATE tart SET cumulative_time = "+str(data['cumulative_time'])+" WHERE id ="+str(id)+" "
					cur.execute(query);
				

				if serializer.is_valid():
					serializer.save()
					if new_item:
						pageItem = PageActiveTime.objects.filter(user_id = data['user_id'], page_id = data['page_id'], is_active=1, is_deleted=0)[:1]
						id = pageItem[0].id
						query = "INSERT INTO tart (id, page_id, user_id, page_title, cumulative_time, icon_url, base_url,is_active, page_content) VALUES (\'"+str(id)+"\',\'"+data['page_id']+"\',\'"+data['user_id']+"\',\'"+data['page_title']+"\',\'"+str(data['cumulative_time'])+"\',\'"+data['icon_url']+"\',\'"+data['base_url']+"\',\'1\',\'"+page_content+"\')"
						print("here")
						cur.execute(query);

					return Response(serializer.data["page_id"], status=status.HTTP_201_CREATED)
				print ("invalid serializer")
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@csrf_exempt
def search_links_sphinx(request,user,search_str,page,format= None):
	if request.method == 'GET':
		page_set = int(page) * 15
		page_list = []
		search_str = urllib.parse.unquote(search_str)
		search_str = re.sub(r"([=\(\)|\-!@~\"&/\\\^\$\='])", r"\\\1", search_str)
		db=MySQLdb.connect(host="127.0.0.1",port=9306,passwd="",db="")
		cur = db.cursor()
		query = "SELECT cumulative_time, base_url, icon_url, user_id, page_id, page_title FROM tart WHERE MATCH(\'@is_active 1 @user_id "+user+" @page_title \"^"+search_str+"$\" \')  OPTION ranker=expr('sum(lcs*user_weight)*cumulative_time') ,field_weights=(page_title=100) "
		print(query)
		cur.execute(query);
		rows = cur.fetchall()
		print(len(rows))
		if len(rows)==1:
			for row in rows:
				page_obj = {}
				page_obj["duration"] = row[0]
				page_obj["baseUrl"] = row[1]
				page_obj["iconUrl"] = row[2]
				page_obj["userId"] = row[3]
				page_obj["pageId"] = row[4]
				page_obj["pageTitle"] = row[5]

				# page_obj["duration"] = row[2]
				# page_obj["baseUrl"] = row[3]
				# page_obj["iconUrl"] = row[4]
				# page_obj["userId"] = row[5]
				# page_obj["pageId"] = row[6]
				# page_obj["pageTitle"] = row[7]

				page_list.append(page_obj)


		else:
			
			search_str = search_str.replace("  "," ")
			search_str = search_str.strip()
			# search_str = search_str.replace(" ","|")
			query = "SELECT cumulative_time, base_url, icon_url, user_id, page_id, page_title FROM tart WHERE MATCH(\'@is_active 1 @user_id "+user+" @(page_title,page_content) "+search_str+"\') OPTION  max_matches=50,ranker=expr('sum(lcs*user_weight)*cumulative_time') ,field_weights=(page_title=100, page_content=20) "
			print(query)
			cur.execute(query);
			rows = cur.fetchall()
			for row in rows[int(page_set) : int(page_set)+15]:
				page_obj = {}
				# page_obj["duration"] = row[2]
				# page_obj["baseUrl"] = row[3]
				# page_obj["iconUrl"] = row[4]
				# page_obj["userId"] = row[5]
				# page_obj["pageId"] = row[6]
				# page_obj["pageTitle"] = row[7]

				page_obj["duration"] = row[0]
				page_obj["baseUrl"] = row[1]
				page_obj["iconUrl"] = row[2]
				page_obj["userId"] = row[3]
				page_obj["pageId"] = row[4]
				page_obj["pageTitle"] = row[5]


				page_list.append(page_obj)

		json_obj = {"lPageItems": page_list}
		json_string = json.dumps(json_obj, indent = 4*' ')
			
			
		return Response(json_string)
