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
from metadata_converter.apply import generate
import unittest
import yaml


class TestSimpleLists(unittest.TestCase):

    def setUp(self):

        self.placeholder_file = 'tests/inputs/simple_lists.yaml'

        with open(self.placeholder_file, 'r') as source_yaml:
            self.in_yamls = list(yaml.load_all(source_yaml,
                                               Loader=yaml.FullLoader))

        self.assertTrue(len(self.in_yamls) == 2)

    def test_string_list(self):

        try:
            template = ['property: value',
                        'string_list_property:',
                        '  {{string_list}}']
            # should succeed
            lines = generate(self.in_yamls[1], template)
            out_yaml = yaml.load('\n'.join(lines), Loader=yaml.FullLoader)
            self.assertTrue(isinstance(out_yaml['string_list_property'], list))
            self.assertEqual(len(out_yaml['string_list_property']), 3)
            self.assertEqual(out_yaml['string_list_property'][0],
                             'property item 1')
            self.assertEqual(out_yaml['string_list_property'][1],
                             'property item 2')
            self.assertEqual(out_yaml['string_list_property'][2],
                             'property item 3')
        except Exception as e:
            self.assertTrue(False, e)

        self.assertTrue(True)

    def test_dict_list(self):

        try:
            template = ['property: value',
                        'dict_list_property:',
                        '  {{dict_list}}']
            # should succeed
            lines = generate(self.in_yamls[1], template)
            out_yaml = yaml.load('\n'.join(lines), Loader=yaml.FullLoader)
            self.assertTrue(isinstance(out_yaml['dict_list_property'], list))
            self.assertEqual(len(out_yaml['dict_list_property']), 3)
            self.assertEqual(len(out_yaml['dict_list_property'][0]), 1)
            self.assertEqual(out_yaml['dict_list_property'][0]['property1'],
                             'value1a')
            self.assertEqual(len(out_yaml['dict_list_property'][1]), 2)
            self.assertEqual(out_yaml['dict_list_property'][1]['property1'],
                             'value1b')
            self.assertEqual(out_yaml['dict_list_property'][1]['property2'],
                             'value2a')
            self.assertEqual(len(out_yaml['dict_list_property'][2]), 3)
            self.assertEqual(out_yaml['dict_list_property'][2]['property1'],
                             'value1c')
            self.assertEqual(out_yaml['dict_list_property'][2]['property2'],
                             'value2b')
            self.assertEqual(out_yaml['dict_list_property'][2]['property3'],
                             'value3a')
        except Exception as e:
            self.assertTrue(False, e)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
