from jsontoolkit.utils import utils
import unittest


class GetIndexFromKeyTestCase(unittest.TestCase):

    def test_get_index_from_keystring(self):
        key_string = "Key[1]"
        self.assertEqual(utils.get_index_from_key(key_string), ['Key', '1'])

    def test_get_index_from_keystring_somestring(self):
        key_string = "Key[blablub]"
        self.assertEqual(utils.get_index_from_key(key_string), ['Key', 'blablub'])

    def test_index_from_keystring_longKey(self):
        key = 'Key' * 256
        index = '100'
        key_string = f'{key}[{index}]'
        self.assertEqual(utils.get_index_from_key(key_string), [key, index])

    def test_index_from_keystring_longIndex(self):
        key = 'Key'
        index = '198' * 256
        key_string = f'{key}[{index}]'
        self.assertEqual(utils.get_index_from_key(key_string), [key, index])

    def test_index_from_keystring_keystring_continues_after_index(self):
        key_string = "Before[1234]After"
        self.assertEqual(utils.get_index_from_key(key_string), ['Before', '1234'])

    def test_index_from_keystring_doubled_index(self):
        key_string = "Before[1234]After[5678]"
        self.assertEqual(utils.get_index_from_key(key_string), ['Before', '1234'])

    def test_index_from_keystring_no_index(self):
        key_string = "Key"
        self.assertEqual(utils.get_index_from_key(key_string), ['Key', None])

    def test_index_from_key_string_no_closing(self):
        key_string = "Key[1234"
        self.assertEqual(utils.get_index_from_key(key_string), ['Key', None])

    def test_index_from_keystring_no_opening(self):
        key_string = "Key1234]"
        self.assertEqual(utils.get_index_from_key(key_string), ['Key1234]', None])

    def test_index_from_keystring_close_before_opening(self):
        key_string = "Key]1234["
        self.assertEqual(utils.get_index_from_key(key_string), ['Key', None])
