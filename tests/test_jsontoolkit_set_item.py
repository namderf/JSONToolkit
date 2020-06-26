from jsontoolkit.jsontoolkit import JsonToolKit
import unittest
import json


class SetItemTestCase(unittest.TestCase):
    def setUp(self):
        self.file = open('tests/test_data/test.json', 'r')
        self.test_data1 = json.load(self.file)
        self.file2 = open('tests/test_data/test2.json', 'r')
        self.test_data2 = json.load(self.file2)
        self.tk = JsonToolKit()
        self.tk_impl = JsonToolKit(self.test_data1)

    def test_set_item_explicit(self):
        data1=self.tk.set_item("company1.department2.test", "Test", data=self.test_data1)
        test_data1_result={'head': {'name': 'Mike Steffens'},
                            'janitor': {'name': 'Johanna Simon'}, 'test': 'Test'}
        data2=self.tk.set_item("p.contents.strong.string", "Hello World",
                                data=self.test_data2)
        test_data2_result=[{'p': {'string': '',
                                  'contents': [
                                      {'strong': {'string':'Hello World'}},
                                      {'p': {'string': 'Foo Bar'}}
                                  ]}},
                           {'p': {'string': '',
                                  'contents': [
                                      {'strong': {'string': 'Hello World'}},
                                      {'strong': {'string': 'Hello World'}},
                                      {'p': {'string': 'some text, again'}}
                                  ]}}
                           ]
        self.assertEqual(self.tk.get_value("company1.department2", data1),
                         test_data1_result)
        self.assertEqual(data2, test_data2_result)

    def test_set_item_implicit(self):
        self.tk_impl.set_item("company1.department2.test", "Test")
        test_data1_result = {'head': {'name': 'Mike Steffens'},
                             'janitor': {'name': 'Johanna Simon'}, 'test': 'Test'}
        self.assertEqual(self.tk_impl.get_value("company1.department2"),
                         test_data1_result)

    def tearDown(self):
        self.file.close()
        self.file2.close()