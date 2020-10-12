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

#
# Tests DLF template (templates/dlf_out.yaml)
#


class TestDLF(unittest.TestCase):

    def setUp(self):

        self.placeholder_file = 'dax-data-set-descriptors/lorem_ipsum.yaml'

        with open(self.placeholder_file, 'r') as source_yaml:
            self.in_yamls = list(yaml.load_all(source_yaml,
                                               Loader=yaml.FullLoader))

        self.assertTrue(len(self.in_yamls) == 1)

        self.template_file = 'templates/dlf_out.yaml'

        with open(self.template_file, 'r') as template_yaml:
            self.template_yamls = list(yaml.load_all(template_yaml,
                                                     Loader=yaml.FullLoader))

        self.assertTrue(len(self.template_yamls) == 1)

    def test_dtest_dlf(self):

        try:
            out_dict = replace(self.in_yamls[0], self.template_yamls[0])
            self.assertTrue(out_dict is not None)
            self.assertTrue(isinstance(out_dict, dict))
            self.assertEqual(out_dict['apiVersion'], 'com.ibm/v1alpha1')
            self.assertEqual(out_dict['kind'], 'Dataset')
            self.assertEqual(out_dict['metadata']['name'],
                             self.in_yamls[0]['name'])
            self.assertEqual(out_dict['metadata']['labels']['version'],
                             self.in_yamls[0]['version'])
            self.assertEqual(out_dict['spec']['type'],
                             'ARCHIVE')
            self.assertEqual(out_dict['spec']['url'],
                             self.in_yamls[0]['repository']['url'])
            self.assertEqual(out_dict['spec']['format'],
                             self.in_yamls[0]['repository']['mime_type'])
        except Exception as e:
            self.assertTrue(False, e)


if __name__ == '__main__':
    unittest.main()
