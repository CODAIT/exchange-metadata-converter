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


class TestSignature(unittest.TestCase):

    def setUp(self):

        self.placeholder_file = 'tests/inputs/scalars.yaml'

        self.in_yamls = yaml.load(Path(self.placeholder_file))

        self.template_file = 'tests/templates/scalars.yaml'

        self.template_yamls = yaml.load(Path(self.template_file))

    def test_none_parms(self):

        try:
            # one or more of the inputs is None
            self.assertEqual(replace(None, None), None)
            self.assertEqual(replace({}, None), None)
            self.assertEqual(replace(None, {}), None)
        except Exception as e:
            self.assertTrue(False, e)

    def test_invalid_parm_types(self):

        invalid_parm_types = [[], '']
        for invalid_type in invalid_parm_types:
            try:
                # first input parameter type is not a dict
                self.assertEqual(replace(invalid_type, {}), None)
                self.assertTrue(False)
            except ValueError:
                pass

            try:
                # second input parameter type is not a dict
                self.assertEqual(replace({}, invalid_type), None)
                self.assertTrue(False)
            except ValueError:
                pass

            try:
                # both input parameter types are not a dict
                self.assertEqual(replace(invalid_type, invalid_type), None)
                self.assertTrue(False)
            except ValueError:
                pass

    def test_valid_parm_types(self):

        try:
            # inputs are empty (nothing to process)
            result = replace({}, {})
            # result must be an empty dict
            self.assertTrue(isinstance(result, dict))
            self.assertTrue(len(result.keys()) == 0)
        except Exception as ex:
            self.assertTrue(False, ex)


if __name__ == '__main__':
    unittest.main()
