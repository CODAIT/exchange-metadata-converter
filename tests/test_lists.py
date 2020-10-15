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
from pathlib import Path
from ruamel.yaml import YAML
import unittest

yaml = YAML()


class TestLists(unittest.TestCase):

    def setUp(self):

        self.placeholder_file = 'tests/inputs/lists.yaml'

        self.in_yamls = yaml.load(Path(self.placeholder_file))

        self.template_file = 'tests/templates/lists.yaml'

        self.template_yamls = yaml.load(Path(self.template_file))

    def test_lists(self):

        try:
            out_dict = replace(self.in_yamls, self.template_yamls)
            self.assertTrue(out_dict is not None)
            self.assertTrue(isinstance(out_dict, dict))
            self.assertEqual(out_dict['apiVersion'], None)
            self.assertEqual(out_dict['kind'],
                             self.template_yamls['kind'])
            # list of strings
            self.assertIsInstance(out_dict['string_list_key'], list)
            self.assertTrue(len(out_dict['string_list_key']) == 2)
            self.assertSetEqual(set(out_dict['string_list_key']),
                                set(['item1', self.in_yamls['string_key']]))

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
