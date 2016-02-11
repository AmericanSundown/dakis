from django.conf import settings
from django.conf.urls import url, include

from dakis.website import views


slug = r'[a-z0-9-]+'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^exp/(?P<exp_id>\d+)/$', views.exp_details, name='exp-summary'),
    url(r'^exp/(?P<exp_id>\d+)/edit/$', views.exp_edit, name='exp-edit'),
    url(r'^exp/compare/$', views.compare_exps, name='compare-exps'),

    url(r'^fork-exp/(?P<exp_id>\d+)/', views.fork_exp, name='fork-exp'),

    url(r'^api/', include('dakis.api.urls')),
    url(r'^api/exp/(?P<exp_id>\d+)/update-params/', views.update_params, name='exp-update-params'),
    url(r'^api/exp/(?P<exp_id>\d+)/next-task/', views.get_next_task, name='get-next-task'),
    url(r'^api/exp/(?P<exp_id>\d+)/run/', views.run_worker_view, name='run-worker'),
    url(r'^api/exp/(?P<exp_id>\d+)/add-property/', views.add_property, name='add-exp-property'),
    url(r'^api/exp/(?P<exp_id>\d+)/remove-property/(?P<prop_id>\d+)/', views.remove_property, name='remove-exp-property'),
    url(r'^api/exp/(?P<exp_id>\d+)/start/', views.start_worker_view, name='start-worker'),
    url(r'^api/exp/(?P<exp_id>\d+)/reset-tasks/(?P<task_status>\w{1})/', views.reset_exp_tasks, name='reset-exp-tasks'),
    url(r'^api/exp/(?P<exp_id>\d+)/cls/(?P<func_cls>\d+)/reset-tasks/(?P<task_status>\w{1})/', views.reset_cls_tasks, name='reset-cls-tasks'),
    url(r'^api/exp/(?P<exp_id>\d+)/toggle-status/', views.toggle_exp_status, name='toggle-exp-status'),
    url(r'^api/exp/(?P<exp_id>\d+)/add-threads/', views.add_threads, name='exp-add-threads'),
]

urlpatterns += [
    url(r'^accounts/', include('dakis.accounts.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
