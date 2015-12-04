import django.test


class WWWTests(django.test.TestCase):
    def test__index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
