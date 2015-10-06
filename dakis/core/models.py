from autoslug import AutoSlugField
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from json_field import JSONField

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class ExperimentManager(models.Manager):
    def dublicate(self, exp):
        new_exp = Experiment.objects.create()
        # General purpose fields
        new_exp.author = exp.author
        new_exp.description = exp.description
        new_exp.algorithm = exp.algorithm + ' (copy)'
        new_exp.repository = exp.repository
        new_exp.branch = exp.branch
        new_exp.executable = exp.executable
        new_exp.max_duration = exp.max_duration
        # Algorithm specific fields
        new_exp.neighbours = exp.neighbours
        new_exp.subregion_selection = exp.subregion_selection
        new_exp.lipschitz_estimation = exp.lipschitz_estimation
        new_exp.subregion_division = exp.subregion_division
        new_exp.stopping_criteria = exp.stopping_criteria
        new_exp.stopping_accuracy = exp.stopping_accuracy
        new_exp.subregion = exp.subregion
        new_exp.inner_problem_accuracy = exp.inner_problem_accuracy
        new_exp.inner_problem_iters = exp.inner_problem_iters
        new_exp.inner_problem_division = exp.inner_problem_division
        new_exp.save()
        return new_exp


class Experiment(models.Model):
    STATUS_CHOICES = (
        ('C', 'Created'),
        ('R', 'Running'),
        ('P', 'Paused'),
        ('D', 'Done')
    )

    objects = ExperimentManager()

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    author = models.ForeignKey(User, null=True)

    description = models.TextField(_('Description'), null=True,
        help_text=_('This experiment description'))
    algorithm = models.CharField(_('Algorithm'), max_length=255, null=True,
        help_text=_('Unique verbose name of this algorithm'))
    max_duration = models.FloatField(_('Max one execution duration in seconds'), null=True)

    repository = models.CharField(_('Source code repository'), max_length=255, null=True,
        help_text=_('Git of Mercurial repository, where source code is stored, e.g. http://github.com/niekas/dakis'))
    branch = models.CharField(_('Branch'), max_length=255, null=True,
        help_text=_('Branch of source code repository, need only if its not master branch'))
    executable = models.CharField(_('Executable'), max_length=255, null=True,
        help_text=_('Executable file in source code repository, e.g. main.out'))

    details = JSONField(_('Algorithm details'), null=True, default='',
        help_text=_('Algorithm details in JSON format'))

    neighbours = models.CharField(_('Neighbours'), max_length=255, null=True,
        help_text=_('Strategy how neighbours are determined'))
    subregion_selection = models.CharField(_('Subregion selection strategy'), max_length=255, null=True,
        help_text=_('Strategy how subregion is selected for division'))

    lipschitz_estimation = models.CharField(_('Lipschitz estimation'), max_length=255, null=True,
        help_text=_('Subregion Lipschitz constant estimation strategy'))

    subregion_division = models.CharField(_('Subregion division'), max_length=255, null=True,
        help_text=_('Subregion division strategy'))

    stopping_criteria = models.CharField(_('Stopping criteria'), max_length=255, null=True,
        help_text=_('Stopping criteria strategy'))
    stopping_accuracy = models.CharField(_('Stopping accuracy'), max_length=255, null=True,
        help_text=_('Stopping accuracy'))

    subregion = models.CharField(_('Subregion'), max_length=255, null=True,
        help_text=_('Subregion type: simplex or rectangle'))

    inner_problem_accuracy = models.CharField(_('Inner accuracy'), max_length=255, null=True,
        help_text=_('Inner problem solution accuracy'))
    inner_problem_iters = models.IntegerField(_('Inner iters'), null=True,
        help_text=_('Inner problem maximum iterations to get solution'))
    inner_problem_division = models.CharField(_('Division strategy in inner problem'), max_length=255, null=True,
        help_text=_('Inner problem subregion division strategy'))

    invalid = models.BooleanField(_('Not valid'), default=True,
        help_text=_('Is this experiment not valid? Its not valid if critical mistake was found.'))
    mistakes = models.TextField(_('Mistakes'), null=True,
        help_text=_('Descriptions of mistakes, which were found in this experiment'))

    status = models.CharField(_('Status'), choices=STATUS_CHOICES, default='C', max_length=2)

    threads = models.IntegerField(_('Threads'), null=True,
        help_text=_('How many threads are currently running'))

    def __str__(self):
        return self.algorithm

    def get_absolute_url(self):
        return reverse('exp-summary', args=[self.pk])


class Task(models.Model):
    STATUS_CHOICES = (
        ('C', 'Created'),
        ('R', 'Running'),
        ('S', 'Suspended'),
        ('D', 'Done')
    )
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
