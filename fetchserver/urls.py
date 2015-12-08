from django.conf.urls import include
from django.conf.urls import url
from fetchserver import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
	url(r'^fetch/register/$', views.register_new_user, name="register-user"),
	url(r'^fetch/login/$', views.login_user, name="login-user"),
	url(r'^fetch/user/(?P<user>[\s\S]+)/search/(?P<search_str>[\s\S]+)/page/(?P<page>[0-9]+)$', views.search_links, name= 'search-links'),	
	url(r'^fetch/user/(?P<user>[\s\S]+)/sphinx/(?P<search_str>[\s\S]+)/page/(?P<page>[0-9]+)$', views.search_links_sphinx, name= 'sphinx-links'),
	url(r'^fetch/update/$', views.update_page_active_time, name="page-active"),
	url(r'^fetch/update/userdetails/$', views.update_user_details, name= 'update-details'),
	url(r'^fetch/blacklist/page/$', views.update_black_listed_pages, name = 'block-domain'),
	url(r'^fetch/user/(?P<user>[\s\S]+)/clear/$', views.clear_user_pages, name = 'clear_data'),
	url(r'^fetch/user/(?P<user>[\s\S]+)/notify$', views.get_notification_info, name= 'notify-user'),
	url(r'^fetch/user/(?P<user>[\s\S]+)/page/(?P<page>[0-9]+)$', views.get_trending_pages, name= 'trending-pages'),
	url(r'^fetch/user/(?P<user>[\s\S]+)/base/(?P<domain>[\s\S]+)$', views.get_collated_pages, name= 'domain-links'),
	url(r'^fetch/user/(?P<user>[\s\S]+)/suggest/(?P<search_str>[\s\S]+)$', views.get_user_search_suggestions, name= 'suggest-links'),

	
]

