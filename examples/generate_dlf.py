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
from metadata_converter.generate import generate_dlf_yaml
from metadata_converter.generate import generate_dlf_yaml_dict
from pathlib import Path
from ruamel.yaml import YAML
import sys

yaml = YAML()

#
# This example illustrates how to invoke the exchange metadata converter
# programmatically, using the DLF template
# Required parameters:
# /path/to/placeholder/yaml see examples in dax-data-set-descriptors/
if __name__ == "__main__":

    try:

        if len(sys.argv) != 2:
            print('Usage: {} {}'
                  .format(sys.argv[0],
                          '/path/to/placeholder/yaml'))
            sys.exit(1)

        # load placeholder YAML
        placeholder_yaml = yaml.load(Path(sys.argv[1]))

        # Generate DLF-compatible YAML by replacing the placeholders
        # in  "templates/dlf_out.yaml" with values from placeholder_yaml
        generated_dlf_yaml_dict = generate_dlf_yaml_dict(placeholder_yaml)

        # print DLF-compatible output with replacements in place
        print('Generated DLF YAML dict: ')
        print(generated_dlf_yaml_dict)

        print('Generated DLF YAML file: ')
        print(generate_dlf_yaml(placeholder_yaml))

    except Exception as ex:
        print(ex)
