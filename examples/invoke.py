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
import sys

yaml = YAML()
yaml.default_flow_style = False


#
# This example illustrates how to invoke the exchange metadata converter
# programmatically.
# Required parameters:
# /path/to/placeholder/yaml see examples in dax-data-set-descriptors/
# /path/to/template/yaml see examples in templates/
if __name__ == "__main__":

    try:

        if len(sys.argv) != 3:
            print('Usage: {} {} {}'
                  .format(sys.argv[0],
                          '/path/to/placeholder/yaml',
                          '/path/to/template/yaml'))
            sys.exit(1)

        # load the placeholder YAML
        in_placeholder_yaml = yaml.load(Path(sys.argv[1]))

        # load the template YAML
        in_template_yaml = yaml.load(Path(sys.argv[2]))

        # replace placeholders in in_template_yaml with values from
        # in_placeholder_yaml
        out_template_yaml = replace(in_placeholder_yaml, in_template_yaml)

        # print template yamls with replacements in place
        yaml.dump(out_template_yaml, sys.stdout)

    except Exception as ex:
        print(ex)
