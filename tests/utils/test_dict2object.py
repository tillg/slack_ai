import unittest
from slack_ai.utils.dict2object import dict2object

class TestDict2Object(unittest.TestCase):
    def test_dict2object(self):
        d = {'key1': 'value1', 'key2': 'value2'}
        o = dict2object(d)
        self.assertEqual(o.key1, 'value1')
        self.assertEqual(o.key2, 'value2')

    def test_dict2object_with_sub_structure(self):
        d = {'key1': 'value1', 'key2': 'value2', 
             'key3': {'key4': 'value4', 'key5': 'value5', 
                      'key6': {'key7': 'value7', 'key8': 'value8'}},
             'key9': ['value9', 'value10', {'key11': 'value11'}]
            }
        o = dict2object(d)
        self.assertEqual(o.key1, 'value1')
        self.assertEqual(o.key2, 'value2')
        self.assertEqual(o.key3.key4, 'value4')
        self.assertEqual(o.key3.key5, 'value5')
        self.assertEqual(o.key3.key6.key7, 'value7')
        self.assertEqual(o.key3.key6.key8, 'value8')
        self.assertEqual(o.key9[0], 'value9')
        self.assertEqual(o.key9[2].key11, 'value11')

if __name__ == '__main__':
    unittest.main()