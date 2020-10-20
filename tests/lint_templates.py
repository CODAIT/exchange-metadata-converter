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
import glob
import re
import unittest

#
# Lints built-in templates in /templates
#


class LintBuiltInTemplates(unittest.TestCase):

    def test_internal_templates(self):

        # Run linter over the built-in templates in
        # templates/
        trailing_whitespace_list = []
        error_count = 0
        prog = re.compile(r'\s+\s$')
        for descriptor in glob.iglob('templates/*.yaml'):
            current_line = 0
            with open(descriptor, 'r') as d:
                for line in d.readlines():
                    current_line = current_line + 1
                    m = prog.search(line)
                    if m is None:
                        continue
                    else:
                        trailing_whitespace_list.append(current_line)
            if len(trailing_whitespace_list) > 0:
                print('{} contains {} trailing whitespaces in line(s) {}'
                      .format(descriptor,
                              len(trailing_whitespace_list),
                              trailing_whitespace_list))
                error_count = error_count + 1
                trailing_whitespace_list = []
        self.assertEqual(error_count, 0)


if __name__ == '__main__':
    unittest.main()
