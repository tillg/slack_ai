import unittest
from slack_ai.utils.robust_jsonify import robust_jsonify


class TestRobustJsonify(unittest.TestCase):
#     def test_simple_object(self):
#         class MyClass:
#             def __init__(self, x, y):
#                 self.x = x
#                 self.y = y

#         obj = MyClass(1, 2)
#         json_str = robust_jsonify(obj)
#         self.assertEqual(json_str, '{\n   "x": 1,\n   "y": 2\n}')

    def test_complex_object(self):
        class MyClass:
            def __init__(self, x, y, z=None):
                self.x = x
                self.y = y
                self.z = z

        obj1 = MyClass(1, 2)
        obj2 = MyClass(3, 4, obj1)
        obj1.z = obj2  # create a circular reference

        json_str = robust_jsonify(obj2)
        expected = '{\n   "x": 3,\n   "y": 4,\n   "z": {\n      "x": 1,\n      "y": 2,\n      "z": "<Circular Reference>"\n   }\n}'
        self.assertEqual(json_str, expected)


    # def test_custom_args(self):
    #     obj = {"x": 1, "y": 2}
    #     json_str = robust_jsonify(obj, indent=4, sort_keys=False)
    #     self.assertEqual(json_str, '{\n    "x": 1,\n    "y": 2\n}')


if __name__ == '__main__':
    unittest.main()
