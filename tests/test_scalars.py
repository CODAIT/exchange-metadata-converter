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


class TestScalars(unittest.TestCase):

    def setUp(self):

        self.placeholder_file = 'tests/inputs/scalars.yaml'

        with open(self.placeholder_file, 'r') as source_yaml:
            self.in_yamls = list(yaml.load_all(source_yaml,
                                               Loader=yaml.FullLoader))

        self.assertTrue(len(self.in_yamls) == 1)

        self.template_file = 'tests/templates/scalars.yaml'

        with open(self.template_file, 'r') as template_yaml:
            self.template_yamls = list(yaml.load_all(template_yaml,
                                                     Loader=yaml.FullLoader))

        self.assertTrue(len(self.template_yamls) == 1)

    def test_scalars(self):

        try:
            out_dict = replace(self.in_yamls[0], self.template_yamls[0])
            self.assertTrue(out_dict is not None)
            self.assertTrue(isinstance(out_dict, dict))
            self.assertEqual(out_dict['apiVersion'], None)
            self.assertEqual(out_dict['kind'],
                             self.template_yamls[0]['kind'])
            self.assertEqual(out_dict['metadata'],
                             self.in_yamls[0]['level0_1'])
            self.assertEqual(out_dict['basic'],
                             self.template_yamls[0]['basic'])
            self.assertEqual(out_dict['anton'], None)
            self.assertEqual(out_dict['delta'],
                             self.in_yamls[0]['level0_3']['level1_1'])
            self.assertEqual(out_dict['caesar'],
                             self.template_yamls[0]['caesar'])
            self.assertEqual(out_dict['gamma'],
                             self.in_yamls[0]
                             ['level0_3']['level1_2']['level2_1'])
        except Exception as e:
            self.assertTrue(False, e)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
