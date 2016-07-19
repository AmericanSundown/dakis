from django_webtest import WebTest

from django.contrib.auth.models import User, AnonymousUser


class IndexPageTests(WebTest):

    def test_index_page(self):
        resp = self.app.get('/', user=AnonymousUser())
        self.assertEqual(resp.status_int, 200)

        user = User.objects.create(username='u1')
        resp = self.app.get('/', user=user)
        self.assertEqual(resp.status_int, 200)
