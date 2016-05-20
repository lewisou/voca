from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^list/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$', views.list, name='list'),
	url(r'^check/(?P<id>[0-9]+)/$', views.check, name="check"),
	url(r'^done/(?P<id>[0-9]+)/$', views.done, name="done"),
	url(r'^bad/(?P<id>[0-9]+)/$', views.markBad, name="bad"),
	url(r'^new/$', views.new, name="new"),
	url(r'^create/$', views.create, name="create"),
	url(r'^download_voice/(?P<id>[0-9]+)/$', views.downloadVoice, name="downloadVoice"),
]
