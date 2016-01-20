from django import forms
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from dakis.core.models import Experiment, Algorithm, Problem


class PropertyForm(forms.Form):
    name = forms.CharField()
    value = forms.CharField()

    def clean_value(self):
        value = self.cleaned_data['value']
        try:
            value = int(value)
        except:
            try:
                value = float(value)
            except:
                pass
        return value


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ('description', 'status', 'invalid', 'mistakes', 'is_major', 'parent')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
            'mistakes': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
        }

class AlgorithmForm(forms.ModelForm):
    class Meta:
        model = Algorithm
        fields = ('title', 'repository', 'branch', 'executable', 'details')
        widgets = {
            'details': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
            'title': forms.TextInput(attrs={'size': 71}),
            'repository': forms.TextInput(attrs={'size': 71}),
            'branch': forms.TextInput(attrs={'size': 71}),
            'executable': forms.TextInput(attrs={'size': 71}),
        }

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('title', 'input_params', 'result_display_params')
        widgets = {
            'title': forms.TextInput(attrs={'size': 71}),
            'input_params': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
            'result_display_params': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
        }

