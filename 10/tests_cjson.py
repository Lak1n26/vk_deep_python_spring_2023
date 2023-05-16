import unittest

import json
import ujson
import cjson

import main

class TestCJSON(unittest.TestCase):
    def test_loads(self):
        json_str = '{"hello": 10, "world": "value"}'
        json_doc = json.loads(json_str)
        ujson_doc = ujson.loads(json_str)
        cjson_doc = cjson.loads(json_str)
        self.assertEqual(json_doc, ujson_doc, cjson_doc)


        fake_json = json.dumps(
            {
                "name": "Danila Lyapin",
                "age": 21,
                "address": "Russia, Voronezh",
                "company": "VSU",
                "status": "student",
                "Best company in the world": "VK :)",
                "123": "456"
            }
        )
        self.assertEqual(cjson.loads(fake_json), ujson.loads(fake_json))

    def test_dumps(self):
        json_str = '{"hello": 10, "world": "value"}'
        self.assertEqual(json_str, cjson.dumps(cjson.loads(json_str)))
    
        some_dict = {
                "name": "Danila Lyapin",
                "age": 21,
                "address": "Russia, Voronezh",
                "company": "VSU",
                "status": "student",
                "Best company in the world": "VK :)",
                "123": "456"
            }
        print(cjson.dumps(some_dict))
        print(jjson.dumps(some_dict))
        print(ujson.dumps(some_dict))
        self.assertEqual(cjson.dumps(some_dict), json.dumps(some_dict))



if __name__ == '__main__':
    unittest.main()
