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
# import metadata_converter.apply as
from metadata_converter.apply import generate
from metadata_converter.apply import PlaceholderNotFoundError
import unittest
import yaml


class TestDLF(unittest.TestCase):

    def setUp(self):
        self.template_file = 'templates/dlf_out.yaml'

        with open(self.template_file, 'r') as template_file:
            self.template = template_file.readlines()

    def test_required_properties(self):
        in_yaml = {}

        try:
            # should raise PlaceholderNotFoundError('name')
            generate(in_yaml, self.template)
            self.assertTrue(False)
        except PlaceholderNotFoundError as pnfe:
            self.assertEqual(pnfe.placeholder, 'name')

        in_yaml['name'] = 'name'

        try:
            # should raise PlaceholderNotFoundError('repository.url')
            generate(in_yaml, self.template)
            self.assertTrue(False)
        except PlaceholderNotFoundError as pnfe:
            self.assertEqual(pnfe.placeholder, 'repository.url')

        in_yaml['repository'] = {
            'url': 'https://www.google.com'
        }

        try:
            # should raise PlaceholderNotFoundError('repository.mime_type')
            generate(in_yaml, self.template)
            self.assertTrue(False)
        except PlaceholderNotFoundError as pnfe:
            self.assertEqual(pnfe.placeholder, 'repository.mime_type')

        self.assertTrue(True)

    def test_ok(self):
        # payload
        in_yaml = {
            'name': 'test_name',
            'repository': {
                'url': 'www.google.com',
                'mime_type': 'application/x-tar'
            }
        }

        try:
            # should succeed
            lines = generate(in_yaml, self.template)
            out_yaml = yaml.load('\n'.join(lines), Loader=yaml.FullLoader)
            self.assertEqual(out_yaml['apiVersion'], 'com.ibm/v1alpha1')
            self.assertEqual(out_yaml['kind'], 'Dataset')
            self.assertEqual(out_yaml['metadata']['name'], 'test_name')
            self.assertEqual(out_yaml['spec']['type'], 'ARCHIVE')
            self.assertEqual(out_yaml['spec']['url'], 'www.google.com')
            self.assertEqual(out_yaml['spec']['format'], 'application/x-tar')
        except Exception as e:
            print(e)
            self.assertTrue(False)

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
