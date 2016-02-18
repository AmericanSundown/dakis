from autoslug import AutoSlugField
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from json_field import JSONField
from concurrency.fields import IntegerVersionField

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Algorithm(models.Model):
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    author = models.ForeignKey(User, null=True)

    algorithm_title = models.CharField(_('Algorithm title'), max_length=255, null=True, blank=True,
        help_text=_('Unique verbose name of this algorithm'))
    algorithm_description = models.TextField(_('Description'), null=True, blank=True,
        help_text=_('This algorithm description'))

    repository = models.CharField(_('Source code repository'), max_length=255, null=True, blank=True,
        help_text=_('Git of Mercurial repository, where source code is stored, e.g. http://github.com/niekas/dakis'))
    branch = models.CharField(_('Branch'), max_length=255, null=True, blank=True,
        help_text=_('Branch of source code repository, need only if its not master branch'))
    executable = models.CharField(_('Executable'), max_length=255, null=True, blank=True,
        help_text=_('Executable file in source code repository, e.g. main.out'))

    details = JSONField(_('Algorithm details'), null=True, blank=True, default='[]',
        help_text=_('Algorithm details in JSON format'))

    is_major = models.BooleanField(_('Is major'), default=False,
        help_text=_('Is this algorithm unique? And should it be used for comparison as its algorithm class representative?'))
    algorithm_parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    def __str__(self):
        return str(self.algorithm_title)

    def dublicate(self):
        return Algorithm.objects.create(
            algorithm_title=self.algorithm_title + ' (copy)',
            algorithm_description=self.algorithm_description,
            repository=self.repository,
            branch=self.branch,
            executable=self.executable,
            details=self.details,
            algorithm_parent=self.algorithm_parent,
        )


class Problem(models.Model):
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    author = models.ForeignKey(User, null=True)

    problem_title = models.CharField(_('Problem title'), max_length=255, null=True, blank=True,
                             help_text=_('Unique verbose name of this problem'))
    problem_description = models.TextField(_('Description'), null=True, blank=True, help_text=_('Problem description'))

    input_params = JSONField(_('Input parameters'), null=True, blank=True, default='[]',
            help_text=_('Parameters for each experiment task. Ranges available, e.g. 1..10. Nesting available.'))
    result_display_params = JSONField(_('Result display discribing parameters'), null=True, blank=True, default='[]',)
    problem_parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    def __str__(self):
        return str(self.problem_title)

    def dublicate(self):
        return Problem.objects.create(
            problem_title=self.problem_title,
            problem_description=self.problem_description,
            input_params=self.input_params,
            result_display_params=self.result_display_params,
            problem_parent=self.problem_parent,
        )


class Experiment(models.Model):
    STATUS_CHOICES = (
        ('C', 'Created'),
        ('R', 'Running'),
        ('P', 'Paused'),
        ('D', 'Done')
    )

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    author = models.ForeignKey(User, null=True)

    # Experiment fields
    description = models.TextField(_('Description'), null=True, blank=True,
        help_text=_('This experiment description'))

    algorithm = models.ForeignKey('Algorithm', null=True, help_text=_('Algorithm which is used for this experiment'))
    problem = models.ForeignKey('Problem', null=True, help_text=_('Problem which is solved in this experiment'))

    status = models.CharField(_('Status'), choices=STATUS_CHOICES, default='C', max_length=2)

    threads = models.IntegerField(_('Threads'), default=0, null=True,
        help_text=_('How many threads are currently running'))

    invalid = models.BooleanField(_('Not valid'), default=False,
        help_text=_('Is this experiment not valid? Its not valid if critical mistake was found.'))
    mistakes = models.TextField(_('Mistakes'), null=True, blank=True,
        help_text=_('Descriptions of mistakes, which were found in this experiment'))

    is_major = models.BooleanField(_('Is major'), default=False,
        help_text=_('Is this algorithm unique? And should it be used for comparison as its algorithm class representative?'))

    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    def __str__(self):
        if self.algorithm:
            title = self.algorithm.algorithm_title
            if self.problem:
                title += ' ' + self.problem.problem_title
            return title[:150]
        elif self.description:
            if len(self.description) > 50:
                return self.description[:50]
            return self.description
        else:
            return 'New experiment %d' % self.pk

    def get_absolute_url(self):
        return reverse('exp-summary', args=[self.pk])

    def dublicate(self):
        new_exp = Experiment.objects.create()
        new_exp.author = self.author
        new_exp.description = self.description
        new_exp.invalid = self.invalid
        new_exp.parent = self
        if self.algorithm:
            new_exp.algorithm = self.algorithm.dublicate()
        if self.problem:
            new_exp.problem = self.problem.dublicate()
        new_exp.save()
        return new_exp

    def range_to_list(self, rng):
        '''Converts string to element list.'''
        lst = []
        for e in rng.split(','):
            try:
                if '..' in e:
                    start, end = e.split('..')
                    for i in range(int(start), int(end) + 1):
                        lst.append(i)
                else:
                    lst.append(int(e))
            except ValueError:
                lst.append(e)
        return lst

    def pair_operator(self, tasks_input_params, name, value, operate_on=None):
        '''Adds separate value for each task'''
        ## iterate values same as for parameter (previously defined parameter).
        new_tasks_input_params = []
        value_list = self.range_to_list(value)
        for i, p in enumerate(tasks_input_params):
            new_p = p[:]
            new_p.append([name, value_list[i % len(value_list)]])
            new_tasks_input_params.append(new_p)
        return new_tasks_input_params

    def multiply_operator(self, tasks_input_params, name, value, operate_on=None):
        ## new tasks for each value of parameter (previously defined parameter).
        new_tasks_input_params = []
        for p in tasks_input_params:
            for v in self.range_to_list(value):
                new_p = p[:]
                new_p.append([name, v])
                new_tasks_input_params.append(new_p)
        return new_tasks_input_params

    operator_handlers = {
        'multiply': multiply_operator,
        'pair': pair_operator,
    }

    def create_tasks(self):
        '''self.problem.input_params is structured: [{'name': .., 'value': .., 'operator': .., 'operate_on': ..}, ..]'''
        tasks_input_params = [[]]

        ## Create parameter lists
        for param in self.problem.input_params:
            name = param.get('name')
            value = param.get('value')
            op = param.get('operator', 'multiply')
            operate_on = param.get('operate_on')
            tasks_input_params = self.operator_handlers[op](self, tasks_input_params, name, value, operate_on)

        ## Create tasks
        for p in tasks_input_params:   # Warning: check No spaces in name and value to prevent injection attack
            Task.objects.create(input_values=p, experiment=self)

    def update_tasks_input_values(self):
        static_params = {}
        for param in self.problem.input_params:
            name = param.get('name')
            value = param.get('value')
            if ',' not in value and '..' not in value:
                static_params[name] = value

        for task in self.tasks.all():
            for key in static_params:
                task.set_input_param(key, static_params[key])


    def get_tasks_grouped_by_input_param_value(self, param_name=None):
        if param_name is None:
            return [('Total:', self.tasks.all())]

        # Find unique values
        unique_values = []
        for task in self.tasks.order_by('pk'):
            value = None
            for p in task.input_values:
                if p[0] == param_name:
                    value = p[1]
            if value and value not in unique_values:
                unique_values.append(value)

        # Find task groups
        groups_of_tasks = []
        for value in unique_values:
            if type(value) == str:
                tasks = self.tasks.filter(input_values__contains='["%s", "%s"]' % (param_name, value))
            else:
                tasks = self.tasks.filter(input_values__contains='["%s", %s]' % (param_name, value))
            groups_of_tasks.append((value, tasks))
        return groups_of_tasks



class Task(models.Model):
    STATUS_CHOICES = (
        ('C', 'Created'),
        ('R', 'Running'),
        ('S', 'Suspended'),
        ('D', 'Done')
    )

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    version = IntegerVersionField()

    experiment = models.ForeignKey('Experiment', related_name='tasks', null=True,
                    help_text=_('ID of experiment to which this task is assigned to'))
    status = models.CharField(_('Status'), choices=STATUS_CHOICES, default='C', max_length=2)

    input_values = JSONField(_('Input parameters'), null=True, default='[]', help_text=_('Parameters for each experiment task.'))
    output_values = JSONField(_('Output parameters'), null=True, default='[]',)

    stdout = models.TextField(_('stdout'), null=True, help_text=_('Standard output stream'))
    stderr = models.TextField(_('stderr'), null=True, help_text=_('Standard error stream'))

    def get_input_param(self, name):
        '''Returns input parameter value.'''
        return dict(self.input_values).get(name)

    def set_input_param(self, name, value):
        '''Sets input parameter value.'''
        index = None
        if not self.input_values:
            self.input_values = []
        for i, (param_name, param_value) in enumerate(self.input_values):
            if param_name == name:
                index = i
                break
        if index is not None:
            self.input_values[index][1] = value
        else:
            self.input_values.append([name, value])
        return self.save()

    def remove_input_param(self, name):
        if not self.input_values:
            return
        index = None
        for i, (param_name, param_value) in enumerate(self.input_values):
            if param_name == name:
                index = i
                break
        if index is not None:
            return self.input_values.pop(index)
        return

    def get_output_param(self, name):
        '''Returns output parameter value.'''
        return dict(self.output_values).get(name)

    def set_output_param(self, name, value):
        '''Sets output parameter value.'''
        index = None
        if not self.output_values:
            self.output_values = []
        for i, (param_name, param_value) in enumerate(self.output_values):
            if param_name == name:
                index = i
                break
        if index is not None:
            self.output_values[index][1] = value
        else:
            self.output_values.append([name, value])
        return self.save()

    def remove_output_param(self, name):
        if not self.output_values:
            return
        index = None
        for i, (param_name, param_value) in enumerate(self.output_values):
            if param_name == name:
                index = i
                break
        if index is not None:
            return self.output_values.pop(index)
        return
