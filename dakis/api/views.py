import json
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

    def save(self):
        if self.validated_data.get('details'):
            self.validated_data['details'] = json.loads(self.validated_data['details'].replace("'", '"'))
        super(AlgorithmSerializer, self).save()


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)

    class Meta:
        model = Problem
        exclude = ('author',)

    def save(self):
        if self.validated_data.get('input_params'):
            self.validated_data['input_params'] = json.loads(self.validated_data['input_params'].replace("'", '"'))
        if self.validated_data.get('result_display_params'):
            self.validated_data['result_display_params'] = json.loads(self.validated_data['result_display_params'].replace("'", '"'))
        super(ProblemSerializer, self).save()


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)

    class Meta:
        model = Task
        exclude = ('version',)

    def save(self):
        if self.validated_data.get('input_values'):
            self.validated_data['input_values'] = json.loads(self.validated_data['input_values'].replace("'", '"'))
        if self.validated_data.get('output_values'):
            self.validated_data['output_values'] = json.loads(self.validated_data['output_values'].replace("'", '"'))
        super(TaskSerializer, self).save()


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
    filter_fields = ('experiment', 'status')
    filter_backends = (filters.DjangoFilterBackend,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
