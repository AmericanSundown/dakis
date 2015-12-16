from rest_framework import serializers, viewsets
from rest_framework import filters

from django.contrib.auth.models import User

from dakis.core.models import Experiment, Algorithm, Problem, Task


class ExperimentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)

    class Meta:
        model = Experiment
        exclude = ('author',)

    def create(self, data):
        user = self.context['request'].user
        if user.is_authenticated():
            data['author'] = user
        return super(ExperimentSerializer, self).create(data)


class AlgorithmSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)

    class Meta:
        model = Algorithm
        exclude = ('author',)


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)

    class Meta:
        model = Problem
        exclude = ('author',)


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)

    class Meta:
        model = Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer


class AlgorithmViewSet(viewsets.ModelViewSet):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_fields = ('experiment', 'func_cls', 'func_id', 'status')
    filter_backends = (filters.DjangoFilterBackend,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
