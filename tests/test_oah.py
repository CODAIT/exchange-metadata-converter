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
import glob
import unittest
import yaml

#
# Tests OpenAIHub template (templates/openaihub_out.yaml)
#


class TestOAH(unittest.TestCase):

    def setUp(self):

        self.template_file = 'templates/openaihub_out.yaml'

        with open(self.template_file, 'r') as template_yaml:
            self.template_yamls = list(yaml.load_all(template_yaml,
                                                     Loader=yaml.FullLoader))

        self.assertTrue(len(self.template_yamls) == 1)

    def test_dax_dataset_descriptors(self):

        # Verify that the DAX data set descriptors in dax-data-set-descriptors
        # don't raise any exceptions during processing. For example, an
        # exception is raised if the OpenAIHub YAML template contains a
        # placeholder that is not defined.

        error_count = 0
        for descriptor in glob.iglob('dax-data-set-descriptors/*.yaml'):
            with open(descriptor, 'r') as source_yaml:
                in_yamls = list(yaml.load_all(source_yaml,
                                              Loader=yaml.FullLoader))
                self.assertTrue(len(in_yamls) == 1)
                try:
                    replace(in_yamls[0], self.template_yamls[0])
                except Exception as e:
                    print('Error prossing {}: {}'
                          .format(descriptor, str(e)))
                    error_count = error_count + 1
        self.assertEqual(error_count, 0,
                         'Processing of {} descriptors failed'
                         .format(error_count))


if __name__ == '__main__':
    unittest.main()
