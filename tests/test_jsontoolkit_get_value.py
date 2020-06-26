from jsontoolkit.jsontoolkit import JsonToolKit
import unittest
import json


class GetValueTestCase(unittest.TestCase):

    def setUp(self):
        self.file = open('tests/test_data/test.json', 'r')
        self.test_data1 = json.load(self.file)
        self.file2 = open('tests/test_data/test2.json', 'r')
        self.test_data2 = json.load(self.file2)
        self.tk = JsonToolKit()
        self.tk = JsonToolKit()
        self.tk_impl = JsonToolKit(self.test_data1)
        self.tk_impl2 = JsonToolKit(self.test_data2)

    def test_get_value_impl(self):
        ret_val = self.tk.get_value("company1", self.test_data1)
        test_val1 = {"department1": {"head": {"name": "Jacky Lynch"},
                                     "janitor": {"name": "Paul Meier"},
                                     "team": [{"name": "Lodger Reimann", "skills": [
                                         "C#", "JavaScript", "Python"], "age": 34},
                                              {"name": "Maria Benz", "age": 21}]
                                     },
                     "department2": {"head": {"name": "Mike Steffens"},
                                     "janitor": {"name": "Johanna Simon"}
                                     }
                     }
        self.assertEqual(ret_val, test_val1)

        ret_val = self.tk.get_value("company1.department1", self.test_data1)
        test_val2 = {"head": {"name": "Jacky Lynch"},
                     "janitor": {"name": "Paul Meier"},
                     "team": [{"name": "Lodger Reimann",
                               "skills": ["C#", "JavaScript", "Python"],
                               "age": 34},
                              {"name": "Maria Benz", "age": 21}]
                     }
        self.assertEqual(ret_val, test_val2)
        ret_val = self.tk.get_value("company1", self.test_data1)
        self.assertEqual(ret_val, test_val1)

    def test_get_value_expl(self):
        ret_val = self.tk_impl.get_value("company1")
        test_val1 = {"department1": {"head": {"name": "Jacky Lynch"},
                                     "janitor": {"name": "Paul Meier"},
                                     "team": [{"name": "Lodger Reimann", "skills": [
                                         "C#", "JavaScript", "Python"], "age": 34},
                                              {"name": "Maria Benz", "age": 21}]
                                     },
                     "department2": {"head": {"name": "Mike Steffens"},
                                     "janitor": {"name": "Johanna Simon"}
                                     }
                     }
        self.assertEqual(ret_val, test_val1)
        ret_val = self.tk_impl.get_value("company1.department1.head.name")
        test_val2 = "Jacky Lynch"
        self.assertEqual(ret_val, test_val2)
        ret_val = self.tk_impl.get_value("company1")
        self.assertEqual(ret_val, test_val1)

    def test_get_root_array_member(self):
        ret_val = self.tk_impl2.get_value("p")
        test_val1 = [{"string": "",
                      "contents": [
                          {"strong": {"string": "This is a string text"}},
                          {"p": {"string": "Foo Bar"}}]
                      },
                     {"string": "",
                      "contents": [
                          {"strong": {"string": "This is another strong text"}},
                          {"strong": {"string": "another text"}},
                          {"p": {"string": "some text, again"}}]
                      }
                     ]
        self.assertEqual(ret_val, test_val1)
        ret_val = self.tk_impl2.get_value("strong")
        test_val2 = []
        self.assertEqual(ret_val, test_val2)

    def test_get_single_root_array_member(self):
        ret_val = self.tk_impl2.get_value("[0].p")
        test_val1 = {"string": "",
                      "contents": [
                          {"strong": {"string": "This is a string text"}},
                          {"p": {"string": "Foo Bar"}}]
                      }

        self.assertEqual(ret_val, test_val1)
        ret_val = self.tk_impl2.get_value("[0].strong")
        test_val2 = {}
        self.assertEqual(ret_val, test_val2)
        ret_val = self.tk_impl2.get_value("[0].p")
        self.assertEqual(ret_val, test_val1)
        self.assertEqual(self.tk_impl2.get_json(),self.test_data2)

    def test_get_array(self):
        ret_val = self.tk_impl2.get_value("p.contents")
        test_val1 = [{"strong": {"string": "This is a string text"}},
                    {"p": {"string": "Foo Bar"}},
                    {"strong": {"string": "This is another strong text"}},
                    {"strong": {"string": "another text"}},
                    {"p": {"string": "some text, again"}}
                    ]
        self.assertEqual(ret_val, test_val1)

    def test_get_filtered_array(self):
        ret_val = self.tk_impl2.get_value("p.contents.strong")
        test_val1 = [{"string": "This is a string text"},
                    {"string": "This is another strong text"},
                    {"string": "another text"},
                    ]
        self.assertEqual(ret_val, test_val1)

    def test_get_array_member(self):
        ret_val = self.tk_impl2.get_value("p.contents[0]")
        test_val1 = [{"strong": {"string": "This is a string text"}},
                     {"strong": {"string": "This is another strong text"}},
                     ]
        self.assertEqual(ret_val, test_val1)

    def test_get_filtered_array_member(self):
        ret_val = self.tk_impl2.get_value("p.contents[1].strong")
        test_val1 = [{"string": "another text"}]
        self.assertEqual(ret_val, test_val1)

    def tearDown(self):
        self.file.close()
        self.file2.close()
