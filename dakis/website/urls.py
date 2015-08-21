from django.conf import settings
from django.conf.urls import url, include

from dakis.website import views


slug = r'[a-z0-9-]+'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^exp/(?P<exp_id>\d+)/', views.exp_details, name='exp-summary'),
    url(r'^api/', include('dakis.api.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
