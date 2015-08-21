from rest_framework import routers

from django.conf import settings
from django.conf.urls import url, include

from dakis.api.views import ExperimentViewSet


router = routers.DefaultRouter()
router.register(r'experiments', ExperimentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
