from jsontoolkit.jsontoolkit import JsonToolKit
import unittest
import json


class DelItemTestCase(unittest.TestCase):
    def setUp(self):
        self.file = open('tests/test_data/test.json', 'r')
        self.test_data1 = json.load(self.file)
        self.file2 = open('tests/test_data/test2.json', 'r')
        self.test_data2 = json.load(self.file2)
        self.tk = JsonToolKit()
        self.tk_impl = JsonToolKit(self.test_data1)

    def test_del_item_explicit(self):
        data1=self.tk.del_item(keychain="company1.department2.janitor", \
                                data=self.test_data1)
        test_data1_result={'head': {'name': 'Mike Steffens'}}
        self.assertEqual(self.tk.get_value(data1, "company1.department2"),
                         test_data1_result)

    def tearDown(self):
        self.file.close()
        self.file2.close()