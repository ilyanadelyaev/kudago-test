import django.test

import core.tools.enum


class EnumA(core.tools.enum.Enum):
    a = 0
    b = 1
    c = 2

    _choices = (
        (a, 'A'),
        (b, 'B'),
        (c, 'C'),
    )


class EnumTests(django.test.TestCase):
    def test__to_str__int(self):
        value = filter(
            lambda x: x[0] == EnumA.a,
            EnumA()
        )[0][1]
        self.assertEqual(
            value,
            EnumA(EnumA.a)
        )

    def test__to_str__str(self):
        value = filter(
            lambda x: x[0] == EnumA.b,
            EnumA()
        )[0][1]
        self.assertEqual(
            value,
            EnumA('1')
        )

    def test__to_str__invalid(self):
        self.assertEqual(EnumA(-1), None)
        self.assertEqual(EnumA('-1'), None)
        self.assertEqual(EnumA('abc'), None)

    def test__getitem(self):
        value = filter(
            lambda x: x[0] == EnumA.c,
            EnumA()
        )[0][1]
        self.assertEqual(
            EnumA.c,
            EnumA.get_key(value)
        )

    def test__getitem__invalid(self):
        self.assertEqual(EnumA.get_key('D'), None)
