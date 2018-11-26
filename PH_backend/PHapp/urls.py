from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^puzzles/$', views.puzzles, name='puzzles'),
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]