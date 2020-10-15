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
from metadata_converter.apply import PlaceholderNotFoundError
from pathlib import Path
from ruamel.yaml import YAML
import unittest

yaml = YAML()
yaml.default_flow_style = False

#
# Tests template annotations: @optional
#


class TestAnnotations(unittest.TestCase):

    def setUp(self):

        self.placeholder_file = 'tests/inputs/annotations.yaml'

        self.in_yamls = yaml.load(Path(self.placeholder_file))

        self.template_file = 'tests/templates/annotations.yaml'

        self.template_yamls = list(yaml.load_all(Path(self.template_file)))
        self.assertEqual(len(self.template_yamls), 6)

    def test_optional_annotation(self):

        try:
            out_dict = replace(self.in_yamls, self.template_yamls[0])
            self.assertTrue(out_dict is not None)
            self.assertTrue(isinstance(out_dict, dict))
            self.assertIsNone(out_dict['property1'])
            self.assertIsNone(out_dict['property2'])
            self.assertIsNone(out_dict['property3'])
            self.assertIsNone(out_dict['property4'])
            self.assertIsNone(out_dict['property5'])
            self.assertIsNone(out_dict['property6'])
            self.assertIsNone(out_dict['property7']['property8'])
            self.assertIsNone(
                out_dict['property9']['property10']['property11'])
            self.assertEqual(
                out_dict['property12'][0]['property12a'],
                self.in_yamls['hey']['we_are_a_match'])
            self.assertIsNone(
                out_dict['property12'][0]['property12b'])
            self.assertEqual(
                self.template_yamls[0]['property12'][0]['property12c'],
                out_dict['property12'][0]['property12c'])
            self.assertIsNone(
                out_dict['property13']['property14']
                        ['property15']['property16a'])
            self.assertIsNone(
                out_dict['property13']['property14']
                        ['property15']['property16b'])
            self.assertIsNone(
                out_dict['property13']['property14']
                        ['property15']['property16c'])
            self.assertEqual(out_dict['property13']
                             ['property14']['property17'],
                             self.template_yamls[0]['property13']['property14']
                             ['property17'])
            self.assertEqual(out_dict['property13']
                             ['property14']['property18'],
                             self.in_yamls['hey']['we_are_a_match'])
        except Exception as e:
            self.assertTrue(False, e)

    def test_without_optional_annotation(self):

        # self.template_yamls contains multipe documents with
        # references to an undefined placeholder
        for index in [1, 2, 3, 4]:
            try:
                # should fail
                replace(self.in_yamls, self.template_yamls[index])
                self.assertTrue(False)
            except PlaceholderNotFoundError as pnfe:
                self.assertEqual('{{' + pnfe.placeholder + '}}',
                                 self.template_yamls[index]['property1'])
            except Exception as e:
                self.assertTrue(False, e)

        for index in [5]:
            try:
                # should fail
                replace(self.in_yamls, self.template_yamls[index])
                self.assertTrue(False)
            except PlaceholderNotFoundError as pnfe:
                self.assertEqual('{{' + pnfe.placeholder + '}}',
                                 self.template_yamls[index]
                                 .get('property1').get('property1a'))
            except Exception as e:
                self.assertTrue(False, e)


if __name__ == '__main__':
    unittest.main()
