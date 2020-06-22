from jsontoolkit.utils import utils
import unittest


class StringRepsIntTestCase(unittest.TestCase):

    def test_string_reps_int(self):
        self.assertEqual(utils.string_reps_int("15"), 15)

    def test_string_reps_int_fails(self):
        self.assertEqual(utils.string_reps_int("NoInt"), False)

    def test_string_reps_fails_mix(self):
        self.assertEqual(utils.string_reps_int("12NoInt"), False)

    def test_string_reps_int_bool(self):
        self.assertEqual(utils.string_reps_int(True), False)
