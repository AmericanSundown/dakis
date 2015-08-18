from django.conf import settings
from django.conf.urls import url, include

from dakis.website import views

slug = r'[a-z0-9-]+'
event = r'(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>%s)' % slug

urlpatterns = [
    url(r'^$', views.index, name='index'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
