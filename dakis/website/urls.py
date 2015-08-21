from django.conf import settings
from django.conf.urls import url, include

from dakis.website import views
from dakis.api.urls import urlpatterns as api_urlpatterns

slug = r'[a-z0-9-]+'
event = r'(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>%s)' % slug

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
urlpatterns += api_urlpatterns

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
