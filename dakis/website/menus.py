from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Item(object):
    def __init__(self, label, name=None, url=None, *args, **kwargs):
        self.label = label
        self.name = name
        self.address = url
        self.args = args
        self.kwargs = kwargs

    def url(self):
        if self.address:
            return self.address
        return reverse(self.name, args=self.args, kwargs=self.kwargs)


menus = {
    'topmenu': [
        Item(_('New'), name='experiment-list'),
        Item(_('Feedback'), url='https://github.com/niekas/dakis/issues/new'),
    ],
}
