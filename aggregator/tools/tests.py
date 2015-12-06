import django.test

import aggregator.tools.enum


class EnumA(aggregator.tools.enum.Enum):
    a = 0
    b = 1
    c = 2

    choices = (
        (a, 'A'),
        (b, 'B'),
        (c, 'C'),
    )


class EnumTests(django.test.TestCase):
    def test__to_str__int(self):
        value = [x[1] for x in EnumA.choices if x[0] == EnumA.a][0]
        self.assertEqual(
            value,
            EnumA(EnumA.a)
        )

    def test__to_str__str(self):
        value = [x[1] for x in EnumA.choices if x[0] == EnumA.b][0]
        self.assertEqual(
            value,
            EnumA('1')
        )

    def test__to_str__invalid(self):
        self.assertEqual(EnumA(-1), None)
        self.assertEqual(EnumA('-1'), None)
        self.assertEqual(EnumA('abc'), None)

    def test__getitem(self):
        value = [x[1] for x in EnumA.choices if x[0] == EnumA.c][0]
        self.assertEqual(
            EnumA.c,
            EnumA.get_key(value)
        )

    def test__getitem__invalid(self):
        self.assertEqual(EnumA.get_key('D'), None)
