from jsontoolkit import jsontoolkit as jtk
import unittest
import json

class AddItemTestCase(unittest.TestCase):
    def setUp(self):
        self.file = open('tests/test_data/test.json', 'r')
        self.test_data1 = json.load(self.file)
        self.file2 = open('tests/test_data/test2.json', 'r')
        self.test_data2 = json.load(self.file2)

    def test_add_item(self):
        data1=jtk.add_item(self.test_data1,"company1.department2.test","Test")
        test_data1_result={'head': {'name': 'Mike Steffens'},
                            'janitor': {'name': 'Johanna Simon'}, 'test': 'Test'}
        data2= jtk.add_item(self.test_data2,"p.contents.strong.string", "Hello World")
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
        self.assertEqual(jtk.get_value(data1,"company1.department2"), test_data1_result)
        self.assertEqual(data2, test_data2_result)

    def tearDown(self):
        self.file.close()
        self.file2.close()