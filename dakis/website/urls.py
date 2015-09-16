from django.conf import settings
from django.conf.urls import url, include

from dakis.website import views


slug = r'[a-z0-9-]+'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^exp/(?P<exp_id>\d+)/', views.exp_details, name='exp-summary'),
    url(r'^create-gkls-tasks/(?P<exp_id>\d+)/', views.create_gkls_tasks, name='experiment-create-gkls-tasks'),

    url(r'^api/', include('dakis.api.urls')),
    url(r'^api/exp/(?P<exp_id>\d+)/next-task/', views.get_next_task, name='get-next-task'),
    url(r'^api/exp/(?P<exp_id>\d+)/run/', views.run_worker_view, name='run-worker'),
    url(r'^api/exp/(?P<exp_id>\d+)/start/', views.start_worker_view, name='start-worker'),
    url(r'^api/exp/(?P<exp_id>\d+)/toggle-status/', views.toggle_exp_status, name='toggle-exp-status'),
]

urlpatterns += [
    url(r'^accounts/', include('dakis.accounts.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
