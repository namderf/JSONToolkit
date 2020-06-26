from jsontoolkit.jsontoolkit import JsonToolKit
import unittest
import json

class GetValueTestCase(unittest.TestCase):

    def setUp(self):
        self.file = open('tests/test_data/test.json', 'r')
        self.test_data1=json.load(self.file)
        self.file2 = open('tests/test_data/test2.json', 'r')
        self.test_data2=json.load(self.file2)
        self.tk = JsonToolKit()
        self.tk = JsonToolKit()
        self.tk_impl = JsonToolKit(self.test_data1)

    def test_get_value_impl(self):
        ret_val = self.tk.get_value("company1", self.test_data1)
        test_val1 = {"department1": {"head": {"name": "Jacky Lynch"},
                                   "janitor": {"name": "Paul Meier"},
                                    "team": [{"name":  "Lodger Reimann", "skills":  [
                                        "C#", "JavaScript", "Python"], "age":  34},
                                             {"name":  "Maria Benz", "age":  21}]
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

    def tearDown(self):
        self.file.close()
        self.file2.close()