from django import forms
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from dakis.core.models import Experiment


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
