from jsontoolkit import jsontoolkit as jtk
import unittest
import json

class GetKeyPathsTestCase(unittest.TestCase):

    def setUp(self):
        self.file = open('tests/test_data/test.json', 'r')
        self.test_data1=json.load(self.file)
        self.file2 = open('tests/test_data/test2.json', 'r')
        self.test_data2=json.load(self.file2)


    def test_get_keypaths(self):
        test_data1_keypaths=['company1.department2.head.name',
                                  'company2.department2.janitor',
                                  'company1.department2', 'company2.department1',
                                  'company2.department1.head',
                                  'company2.department2.janitor.name',
                                  'company1.department1.team.age',
                                  'company2.department2.head.name',
                                  'company2.department1.head.name',
                                  'company1.department1.team.name',
                                  'company1.department1.head',
                                  'company1.department1.janitor',
                                  'company2.department1.janitor',
                                  'company2.department1.janitor.name',
                                  'company2.department2',
                                  'company1.department1.team.skills',
                                  'company1.department1', 'company2.department2.head',
                                  'company1.department2.janitor.name',
                                  'company1.department1.team',
                                  'company1.department2.head',
                                  'company1.department1.head.name',
                                  'company1.department1.janitor.name',
                                  'company1.department2.janitor', 'company2', 'company1']
        test_data2_keypaths=['p.contents.strong', 'p.contents.p.string',
                                  'p.contents', 'p.contents.strong.string',
                                  'p.contents.p', 'p.string', 'p']

        self.assertListEqual(sorted(jtk.get_keypaths(self.test_data1)),
                      sorted(test_data1_keypaths))
        self.assertListEqual(sorted(jtk.get_keypaths(self.test_data2)),
                             sorted(test_data2_keypaths))

    def test_get_keypaths_hide_no_arrays(self):
        test_data1_keypaths=['company1.department1.janitor',
                             'company2.department2.head',
                             'company1.department2.janitor.name',
                             'company2.department1.head',
                             'company2.department1.janitor.name',
                             'company2.department1', 'company2',
                             'company1.department2.janitor',
                             'company2.department2.janitor', 'company1.department1',
                             'company2.department1.janitor', 'company1',
                             'company2.department1.head.name',
                             'company1.department1.head.name',
                             'company1.department1.janitor.name',
                             'company1.department2.head.name', 'company2.department2',
                             'company1.department1.team',
                             'company2.department2.head.name',
                             'company1.department1.team[1].name',
                             'company1.department2',
                             'company1.department1.team[0].name',
                             'company1.department1.team[0].skills',
                             'company1.department1.team[0].age',
                             'company1.department1.head',
                             'company1.department1.team[1].age',
                             'company2.department2.janitor.name',
                             'company1.department2.head']
        test_data2_keypaths=['[0].p.string', '[0].p.contents[1].p.string',
                             '[1].p.contents[2].p', '[1].p.contents[1].strong.string',
                             '[0].p.contents[1].p', '[1].p.contents[1].strong',
                             '[1].p.contents[2].p.string', '[0].p.contents',
                             '[1].p.contents[0].strong.string', '[1].p',
                             '[1].p.contents', '[0].p',
                             '[0].p.contents[0].strong.string',
                             '[1].p.contents[0].strong', '[1].p.string',
                             '[0].p.contents[0].strong']
        self.assertListEqual(sorted(jtk.get_keypaths(self.test_data1,
                                                     hide_arrays=False)),
                             sorted(test_data1_keypaths))
        self.assertListEqual(sorted(jtk.get_keypaths(self.test_data2,
                                                     hide_arrays=False)),
                             sorted(test_data2_keypaths))

    def test_get_keypaths_startkey(self):
        test_data1_keypaths=['head.name', 'janitor.name', 'team.skills', 'head',
                                  'team', 'janitor', 'team.age', 'team.name']
        test_data2_keypaths=['p', 'p.string', 'strong', 'strong.string']
        self.assertListEqual(sorted(jtk.get_keypaths(self.test_data1,
                                                  start_key="company1.department1")),
                             sorted(test_data1_keypaths))
        self.assertListEqual(sorted(jtk.get_keypaths(self.test_data2,
                                                     start_key="p.contents")),
                             sorted(test_data2_keypaths))

    def tearDown(self):
        self.file.close()
        self.file2.close()