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


class TestScalars(unittest.TestCase):

    def setUp(self):

        self.placeholder_file = 'tests/inputs/scalars.yaml'

        self.in_yamls = yaml.load(Path(self.placeholder_file))

        self.template_file = 'tests/templates/scalars.yaml'

        self.template_yamls = yaml.load(Path(self.template_file))

    def test_scalars(self):

        try:
            out_dict = replace(self.in_yamls, self.template_yamls)
            self.assertTrue(out_dict is not None)
            self.assertTrue(isinstance(out_dict, dict))
            self.assertEqual(out_dict['apiVersion'], None)
            self.assertEqual(out_dict['kind'],
                             self.template_yamls['kind'])
            self.assertEqual(out_dict['metadata'],
                             self.in_yamls['level0_1'])
            self.assertEqual(out_dict['basic'],
                             self.template_yamls['basic'])
            self.assertEqual(out_dict['anton'], None)
            self.assertEqual(out_dict['delta'],
                             self.in_yamls['level0_3']['level1_1'])
            self.assertEqual(out_dict['caesar'],
                             self.template_yamls['caesar'])
            self.assertEqual(out_dict['gamma'],
                             self.in_yamls
                             ['level0_3']['level1_2']['level2_1'])
        except Exception as e:
            self.assertTrue(False, e)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
