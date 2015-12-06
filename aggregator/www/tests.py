import django.test

import aggregator.tests


class WWWTests(django.test.TestCase):
    def test__index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test__tag(self):
        tid = aggregator.tests.ModelTests._tag()[0]
        resp = self.client.get('/tag/{}/'.format(tid))
        self.assertEqual(resp.status_code, 200)

    def test__events_list(self):
        resp = self.client.get('/event/')
        self.assertEqual(resp.status_code, 200)

    def test__event(self):
        eid = aggregator.tests.ModelTests._event()[0]
        resp = self.client.get('/event/{}/'.format(eid))
        self.assertEqual(resp.status_code, 200)

    def test__places_list(self):
        resp = self.client.get('/place/')
        self.assertEqual(resp.status_code, 200)

    def test__place(self):
        pid = aggregator.tests.ModelTests._place()[0]
        resp = self.client.get('/place/{}/'.format(pid))
        self.assertEqual(resp.status_code, 200)
