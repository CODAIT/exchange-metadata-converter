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
import glob
import unittest

yaml = YAML()

#
# Tests DLF template (templates/dlf_out.yaml)
#


class TestDLF(unittest.TestCase):

    def setUp(self):

        self.placeholder_file = 'dax-data-set-descriptors/lorem_ipsum.yaml'

        self.in_yamls = yaml.load(Path(self.placeholder_file))

        self.template_file = 'templates/dlf_out.yaml'

        self.template_yamls = yaml.load(Path(self.template_file))

    def test_dtest_dlf(self):

        try:
            out_dict = replace(self.in_yamls, self.template_yamls)
            self.assertTrue(out_dict is not None)
            self.assertTrue(isinstance(out_dict, dict))
            self.assertEqual(out_dict['apiVersion'],
                             'com.ie.ibm.hpsys/v1alpha1')
            self.assertEqual(out_dict['kind'], 'Dataset')
            self.assertEqual(out_dict['metadata']['name'],
                             self.in_yamls['name'])
            self.assertEqual(out_dict['metadata']['labels']['version'],
                             self.in_yamls['version'])
            self.assertEqual(out_dict['spec']['type'],
                             'ARCHIVE')
            self.assertEqual(out_dict['spec']['url'],
                             self.in_yamls['repository']['url'])
            self.assertEqual(out_dict['spec']['format'],
                             self.in_yamls['repository']['mime_type'])
        except Exception as e:
            self.assertTrue(False, e)

    def test_dax_dataset_descriptors(self):

        # Verify that the DAX data set descriptors in dax-data-set-descriptors
        # don't raise any exceptions during processing. For example, an
        # exception is raised if the DLF YAML template contains a placeholder
        # that is not defined.
        error_count = 0
        for descriptor in glob.iglob('dax-data-set-descriptors/*.yaml'):
            in_yaml = yaml.load(Path(descriptor))
            try:
                replace(in_yaml, self.template_yamls)
            except Exception as e:
                print('Error prossing {}: {}'
                      .format(descriptor, str(e)))
                error_count = error_count + 1
        self.assertEqual(error_count, 0,
                         'Processing of {} descriptors failed'
                         .format(error_count))


if __name__ == '__main__':
    unittest.main()
