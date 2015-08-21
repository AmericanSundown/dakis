from rest_framework import serializers, viewsets

from dakis.core.models import Experiment, Task


class ExperimentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Experiment

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
