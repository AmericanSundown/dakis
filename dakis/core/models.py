from autoslug import AutoSlugField
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from json_field import JSONField

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


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

    invalid = models.BooleanField(_('Not valid'), default=False,
        help_text=_('Is this experiment not valid? Its not valid if critical mistake was found.'))
    mistakes = models.TextField(_('Mistakes'), null=True,
        help_text=_('Descriptions of mistakes, which were found in this experiment'))

    status = models.CharField(_('Status'), choices=STATUS_CHOICES, default='C', max_length=2)

    threads = models.IntegerField(_('Threads'), null=True,
        help_text=_('How many threads are currently running'))

    is_major = models.BooleanField(_('Is major'), default=False,
        help_text=_('Is this algorithm unique? And should it be used for comparison as its algorithm class representative?'))

    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    def __str__(self):
        return self.algorithm

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
        new_exp.neighbours = self.neighbours
        new_exp.subregion_selection = self.subregion_selection
        new_exp.lipschitz_estimation = self.lipschitz_estimation
        new_exp.subregion_division = self.subregion_division
        new_exp.stopping_criteria = self.stopping_criteria
        new_exp.stopping_accuracy = self.stopping_accuracy
        new_exp.subregion = self.subregion
        new_exp.inner_problem_accuracy = self.inner_problem_accuracy
        new_exp.inner_problem_iters = self.inner_problem_iters
        new_exp.inner_problem_division = self.inner_problem_division
        new_exp.invalid = self.invalid
        new_exp.parent = self
        new_exp.save()
        return new_exp

    def move_data_to_details_field(self):
        if self.details is None:
            self.details = dict()
        self.details['neighbours'] = self.neighbours
        self.details['subregion_selection'] = self.subregion_selection
        self.details['lipschitz_estimation'] = self.lipschitz_estimation
        self.details['subregion_division'] = self.subregion_division
        self.details['stopping_criteria'] = self.stopping_criteria
        self.details['stopping_accuracy'] = self.stopping_accuracy
        self.details['subregion'] = self.subregion
        self.details['inner_problem_accuracy'] = self.inner_problem_accuracy
        self.details['inner_problem_iters'] = self.inner_problem_iters
        self.details['inner_problem_division'] = self.inner_problem_division
        self.save()


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
