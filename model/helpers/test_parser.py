from unittest import TestCase

from model.equalgain import EqualGainModel
from model.helpers import csvParser


class TestParser(TestCase):
    def setUp(self):
        self.parser = csvParser.Parser(EqualGainModel())

    def test_read(self):
        model = self.parser.read('data/input/sample_data.txt')

        self.assertEqual(len(model.actors), 10)
        self.assertEqual(len(model.issues), 6)
        self.assertEqual(len(model.actor_issues), 6)
        self.assertEqual(len(model.actor_issues[model.issues['tolheffingbinnenstad'].id]), 10)
