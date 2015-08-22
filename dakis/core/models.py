from autoslug import AutoSlugField
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Experiment(models.Model):
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    description = models.TextField(_('Description'), null=True,
        help_text=_('This experiment description'))

    algorithm = models.CharField(_('Algorithm'), max_length=255, null=True,
        help_text=_('Name of algorithm'))

    neighbours = models.CharField(_('Neighbours'), max_length=255, null=True,
        help_text=_('Strategy how neighbours are determined'))

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

    lipschitz_estimation = models.CharField(_('Lipschitz estimation'), max_length=255, null=True,
        help_text=_('Subregion Lipschitz constant estimation strategy'))

    simplex_division = models.CharField(_('Simplex division'), max_length=255, null=True,
        help_text=_('Subregion division strategy'))

    invalid = models.BooleanField(_('Not valid'), default=True,
        help_text=_('Is this experiment not valid? Its not valid if critical mistake was found.'))
    mistakes = models.TextField(_('Mistakes'), null=True,
        help_text=_('Descriptions of mistakes, which were found in this experiment'))

    def __str__(self):
        return '%s  %s  %s  %s' % (self.algorithm, self.neighbours, self.subregion, self.stopping_accuracy)

    def get_absolute_url(self):
        return reverse('exp-summary', args=[self.pk])


class Task(models.Model):
    STATUS_CHOICES = (
        ('C', 'Created'),
        ('R', 'Running'),
        ('S', 'Suspended'),
        ('D', 'Done')
    )
    func_name = models.CharField(_('Function name'), null=True, max_length=255, help_text=_('Function name'))
    func_cls = models.IntegerField(_('GKLS class'), null=True, help_text=_('GKLS function class'))
    func_id = models.IntegerField(_('GKLS id'), null=True, help_text=_('GKLS function id'))
    calls = models.IntegerField(_('Calls'), null=True, help_text=_('Calls'))
    subregions = models.IntegerField(_('Subregions'), null=True, help_text=_('Subregions in final partition'))
    duration = models.DurationField(_('Duration'), null=True, help_text=_('Duration of task execution'))
    f_min = models.FloatField(_('F min'), null=True, help_text=_('Value of minimum, which managed to determine'))
    x_min = models.CharField(_('X min'), max_length=255, null=True, help_text=_('Determined minimum coordinates'))
    experiment = models.ForeignKey('Experiment', related_name='tasks', null=True,
                    help_text=_('ID of experiment to which this task is assigned to'))
    status = models.CharField(_('Status'), choices=STATUS_CHOICES, default='C', max_length=2)
