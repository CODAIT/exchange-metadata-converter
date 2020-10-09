#
# Copyright 2020 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from metadata_converter.apply import replace
import unittest
import yaml


class TestLists(unittest.TestCase):

    def setUp(self):

        self.placeholder_file = 'tests/inputs/lists.yaml'

        with open(self.placeholder_file, 'r') as source_yaml:
            self.in_yamls = list(yaml.load_all(source_yaml,
                                               Loader=yaml.FullLoader))

        self.assertTrue(len(self.in_yamls) == 2)

        self.template_file = 'tests/templates/lists.yaml'

        with open(self.template_file, 'r') as template_yaml:
            self.template_yamls = list(yaml.load_all(template_yaml,
                                                     Loader=yaml.FullLoader))

        self.assertTrue(len(self.template_yamls) == 1)

    def test_lists(self):

        try:
            out_dict = replace(self.in_yamls[1], self.template_yamls[0])
            self.assertTrue(out_dict is not None)
            self.assertTrue(isinstance(out_dict, dict))
            self.assertEqual(out_dict['apiVersion'], None)
            self.assertEqual(out_dict['kind'],
                             self.template_yamls[0]['kind'])
            # list of strings
            self.assertIsInstance(out_dict['string_list_key'], list)
            self.assertTrue(len(out_dict['string_list_key']) == 2)
            self.assertSetEqual(set(out_dict['string_list_key']),
                                set(['item1', self.in_yamls[1]['string_key']]))

            # list of dicts (no replacement)
            self.assertIsInstance(out_dict['dict_list_key'], list)
            self.assertTrue(len(out_dict['dict_list_key']) == 3)
            self.assertIsInstance(out_dict['dict_list_key'][0], dict)
            self.assertEqual(out_dict['dict_list_key'][0]['key1'], 'value1a')
            self.assertEqual(out_dict['dict_list_key'][0]['key2'], 'value2a')
            self.assertEqual(out_dict['dict_list_key'][1]['key1'], 'value1b')
            self.assertEqual(out_dict['dict_list_key'][2]['key1'], 'value1c')
            self.assertEqual(out_dict['dict_list_key'][2]['key2'], 'value2b')
            self.assertEqual(out_dict['dict_list_key'][2]['key3'], 'value3a')

            # list of dicts (with replacement)
            self.assertIsInstance(out_dict['dict_list_key2']['list_a'], list)
            self.assertTrue(len(out_dict['dict_list_key2']['list_a']) == 3)

            print(out_dict['dict_list_key2']['list_a'])

            self.assertEqual(
                out_dict['dict_list_key2']['list_a'][0]['property1'],
                'value1a')
            self.assertEqual(
                out_dict['dict_list_key2']['list_a'][1]['property1'],
                'value1b')
            self.assertEqual(
                out_dict['dict_list_key2']['list_a'][1]['property2'],
                'value2a')
            self.assertEqual(
                out_dict['dict_list_key2']['list_a'][2]['property1'],
                'value1c')
            self.assertEqual(
                out_dict['dict_list_key2']['list_a'][2]['property2'],
                'value2b')
            self.assertEqual(
                out_dict['dict_list_key2']['list_a'][2]['property3'],
                'value3a')

        except Exception as e:
            self.assertTrue(False, e)


if __name__ == '__main__':
    unittest.main()
