from rest_framework import routers

from django.conf import settings
from django.conf.urls import url, include

import dakis.api.views as api_views


router = routers.DefaultRouter()
router.register(r'experiments', api_views.ExperimentViewSet)
router.register(r'tasks', api_views.TaskViewSet)
router.register(r'users', api_views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
