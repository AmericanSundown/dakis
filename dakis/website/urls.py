from django.conf import settings
from django.conf.urls import url, include

from dakis.website import views


slug = r'[a-z0-9-]+'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^exp/(?P<exp_id>\d+)/', views.exp_details, name='exp-summary'),
    url(r'^create-gkls-tasks/(?P<exp_id>\d+)/', views.create_gkls_tasks, name='experiment-create-gkls-tasks'),

    url(r'^api/', include('dakis.api.urls')),
    url(r'^api/(?P<exp_id>\d+)/next_task/', views.get_next_task, name='get-next-task')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
