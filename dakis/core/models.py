from autoslug import AutoSlugField
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from json_field import JSONField

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Algorithm(models.Model):
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    author = models.ForeignKey(User, null=True)

    title = models.CharField(_('Algorithm title'), max_length=255, null=True,
        help_text=_('Unique verbose name of this algorithm'))
    description = models.TextField(_('Description'), null=True,
        help_text=_('This algorithm description'))

    repository = models.CharField(_('Source code repository'), max_length=255, null=True,
        help_text=_('Git of Mercurial repository, where source code is stored, e.g. http://github.com/niekas/dakis'))
    branch = models.CharField(_('Branch'), max_length=255, null=True,
        help_text=_('Branch of source code repository, need only if its not master branch'))
    executable = models.CharField(_('Executable'), max_length=255, null=True,
        help_text=_('Executable file in source code repository, e.g. main.out'))

    # What should be stored in this field? Ok the description parameters. And they surely should be copied from
    # experiment.
    details = JSONField(_('Algorithm details'), null=True, default='',
        help_text=_('Algorithm details in JSON format'))

    is_major = models.BooleanField(_('Is major'), default=False,
        help_text=_('Is this algorithm unique? And should it be used for comparison as its algorithm class representative?'))
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    def __str__(self):
        return str(self.title)


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
    description = models.TextField(_('Description'), null=True,
        help_text=_('This experiment description'))

    status = models.CharField(_('Status'), choices=STATUS_CHOICES, default='C', max_length=2)

    threads = models.IntegerField(_('Threads'), null=True,
        help_text=_('How many threads are currently running'))

    invalid = models.BooleanField(_('Not valid'), default=False,
        help_text=_('Is this experiment not valid? Its not valid if critical mistake was found.'))
    mistakes = models.TextField(_('Mistakes'), null=True,
        help_text=_('Descriptions of mistakes, which were found in this experiment'))

    is_major = models.BooleanField(_('Is major'), default=False,
        help_text=_('Is this algorithm unique? And should it be used for comparison as its algorithm class representative?'))

    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    # Fields migrated to Algorithm model
    algorithm = models.ForeignKey('Algorithm', null=True, help_text=_('Algorithm which is used for experiment'))

    algorithm_title = models.CharField(_('Algorithm'), max_length=255, null=True,
        help_text=_('Unique verbose name of this algorithm'))

    repository = models.CharField(_('Source code repository'), max_length=255, null=True,
        help_text=_('Git of Mercurial repository, where source code is stored, e.g. http://github.com/niekas/dakis'))
    branch = models.CharField(_('Branch'), max_length=255, null=True,
        help_text=_('Branch of source code repository, need only if its not master branch'))
    executable = models.CharField(_('Executable'), max_length=255, null=True,
        help_text=_('Executable file in source code repository, e.g. main.out'))

    details = JSONField(_('Algorithm details'), null=True, default='',
        help_text=_('Algorithm details in JSON format'))

    # Deprecated fields
    # max_duration = models.FloatField(_('Max one execution duration in seconds'), null=True)

    def __str__(self):
        return self.algorithm_title

    def get_absolute_url(self):
        return reverse('exp-summary', args=[self.pk])

    def dublicate(self):
        new_exp = Experiment.objects.create()
        # General purpose fields
        new_exp.author = self.author
        new_exp.description = self.description
        new_exp.algorithm = self.algorithm + ' (copy)'
        new_exp.repository = self.repository
        new_exp.branch = self.branch
        new_exp.executable = self.executable
        new_exp.max_duration = self.max_duration
        # Algorithm specific fields
        new_exp.details = self.details
        new_exp.invalid = self.invalid
        new_exp.parent = self
        new_exp.save()
        return new_exp

    def move_data_to_details_field(self):
        if type(self.details) is not list:
            self.details = []
        self.details.append(('Neighbours', self.neighbours))
        self.details.append(('Subregion selection', self.subregion_selection))
        self.details.append(('Lipschitz estimation', self.lipschitz_estimation))
        self.details.append(('Subregion', self.subregion))
        self.details.append(('Subregion division', self.subregion_division))
        self.details.append(('Stopping criteria', self.stopping_criteria))
        self.details.append(('Stopping accuracy', self.stopping_accuracy))
        self.details.append(('Inner problem accuracy', self.inner_problem_accuracy))
        self.details.append(('Inner problem iters', self.inner_problem_iters))
        self.details.append(('Inner problem division', self.inner_problem_division))
        self.save()



# Input and output parameters.
#   Each parameter should have name, type, default value (which can be range).
#   Parameter nesting only has meaning when using value ranges, which means for each in range use this range.

# class ProblemType(models.Model):
#     created = CreationDateTimeField()
#     modified = ModificationDateTimeField()
#     # What Task parameters should be and how they should change.
#     # Parameter name, type, range. <- some kind of language is needed (python ranges).
#     # Some associated code should also be here.
#     input_params = JSONField(_('Input parameters'), null=True, default='',
#             help_text=_('Parameters for each experiment task. Ranges available, e.g. 1..10. Nesting available.'))
#     output_params = JSONField(_('Output parameters'), null=True, default='',)
#     description = models.TextField(_('Description'), null=True, help_text=_('Problem description'))
#
#
# class Problem(models.Model):
#     created = CreationDateTimeField()
#     modified = ModificationDateTimeField()
#     ForeignKey(ProblemType)
#     params = JSONField(_('Parameters'), null=True, default='',
#             help_text=_('Parameters for each experiment task. Ranges available, e.g. 1..10. Nesting available.'))


class Task(models.Model):
    STATUS_CHOICES = (
        ('C', 'Created'),
        ('R', 'Running'),
        ('S', 'Suspended'),
        ('D', 'Done')
    )

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    duration = models.FloatField(_('Duration'), null=True, help_text=_('Task execution duration in seconds'))
    experiment = models.ForeignKey('Experiment', related_name='tasks', null=True,
                    help_text=_('ID of experiment to which this task is assigned to'))
    status = models.CharField(_('Status'), choices=STATUS_CHOICES, default='C', max_length=2)
    details = JSONField(_('Task details'), null=True, default='',
        help_text=_('Task execution details in JSON format'))

    # Algorithm specific
    func_name = models.CharField(_('Function name'), null=True, max_length=255, help_text=_('Function name'))
    func_cls = models.IntegerField(_('GKLS class'), null=True, help_text=_('GKLS function class'))
    func_id = models.IntegerField(_('GKLS id'), null=True, help_text=_('GKLS function id'))
    calls = models.IntegerField(_('Calls'), null=True, help_text=_('Calls'))
    subregions = models.IntegerField(_('Subregions'), null=True, help_text=_('Subregions in final partition'))
    f_min = models.FloatField(_('F min'), null=True, help_text=_('Value of minimum, which managed to determine'))
    x_min = models.CharField(_('X min'), max_length=255, null=True, help_text=_('Determined minimum coordinates'))
