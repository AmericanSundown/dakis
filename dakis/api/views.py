from rest_framework import serializers, viewsets

from django.contrib.auth.models import User

from dakis.core.models import Experiment, Task


class ExperimentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Experiment

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
