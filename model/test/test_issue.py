from unittest import TestCase

from model.base import Issue


class TestIssue(TestCase):
    def test_normalization(self):

        # the normal case, works always
        x = Issue(name="test", lower=0, upper=100)

        self.assertEqual(x.step_size, 1)
        self.assertEqual(x.de_normalize(50), 50)

        # case with a smaller delta
        y = Issue(name="test", lower=0, upper=60)

        self.assertEqual(y.step_size, 100 / 60)
        self.assertEqual(y.de_normalize(50), 30)

        # case with a negative delta
        z = Issue(name="test", lower=0, upper=-60)

        self.assertEqual(z.step_size, 100 / -60)
        self.assertEqual(z.de_normalize(50), -30)
        self.assertEqual(z.de_normalize(0), 0)
        self.assertEqual(z.de_normalize(100), -60)

        # case with a different starting position

        a = Issue(name="test", lower=10, upper=90)

        self.assertEqual(a.step_size, 100 / 80)
        self.assertEqual(a.delta, 80)
        self.assertEqual(a.de_normalize(50), 50)
        self.assertEqual(a.de_normalize(0), 10)

        # case with a different starting position and negative delta

        b = Issue(name="test", lower=-10, upper=-90)

        self.assertEqual(b.step_size, 100 / -80)
        self.assertEqual(b.delta, -80)
        self.assertEqual(b.de_normalize(50), -50)
        self.assertEqual(b.de_normalize(0), -10)

        # negative delta, positive lower point, negative upper

        c = Issue(name="test", lower=10, upper=-90)

        self.assertEqual(c.step_size, 100 / -100)
        self.assertEqual(c.delta, -100)
        self.assertEqual(c.de_normalize(50), -40)
        self.assertEqual(c.de_normalize(0), 10)

    pass
