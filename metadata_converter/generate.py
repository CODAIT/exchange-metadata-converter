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

from importlib_resources import files
from metadata_converter.apply import replace
import sys
import templates
import yaml


def generate_dlf_yaml(in_yaml):
    """
    Generate DLF-compatible YAML configuration file using
    "templates/dlf_out.yaml" as template.

    :param in_yaml: dict representation of a YAML document defining
    placeholder values in "templates/dlf_out.yaml"
    :type in_yaml: dict
    :raises PlaceholderNotFoundError: a {{...}} placeholder referenced
    in "templates/dlf_out.yaml" was not found
    :raises ValueError in_yaml is not of type dict
    :return: DLF-compatible YAML file
    :rtype: str
    """

    dlf_yaml_dict = generate_dlf_yaml_dict(in_yaml)

    dlf_yaml = yaml.safe_dump(dlf_yaml_dict,
                              default_flow_style=False,
                              allow_unicode=True,
                              sort_keys=False)

    return dlf_yaml


def generate_dlf_yaml_dict(in_yaml):
    """
    Generate DLF-compatible YAML configuration using
    "templates/dlf_out.yaml" as template.

    :param in_yaml: dict representation of a YAML document defining
    placeholder values in "templates/dlf_out.yaml"
    :type in_yaml: dict
    :raises PlaceholderNotFoundError: a {{...}} placeholder referenced
    in "templates/dlf_out.yaml" was not found
    :raises ValueError in_yaml is not of type dict
    :return: DLF-compatible YAML file
    :rtype: dict
    """

    dlf_yaml = files(templates).joinpath('dlf_out.yaml')

    # load the template YAML
    with open(dlf_yaml, 'r') as template_yaml:
        dlf_template_yaml = yaml.load(template_yaml,
                                      Loader=yaml.FullLoader)

    # replace placeholders in in_template_yaml with values from
    # in_placeholder_yaml
    dlf_yaml_dict = replace(in_yaml, dlf_template_yaml)

    return dlf_yaml_dict


#
# This example illustrates how to invoke the exchange metadata converter
# programatically, using the DLF template
# Required parameters:
# /path/to/placeholder/yaml see examples in dax-data-set-descriptors/
if __name__ == "__main__":

    try:

        if len(sys.argv) != 2:
            print('Usage: {} {}'
                  .format(sys.argv[0],
                          '/path/to/placeholder/yaml'))
            sys.exit(1)

        with open(sys.argv[1], 'r') as source_yaml:
            placeholder_yaml = yaml.load(source_yaml,
                                         Loader=yaml.FullLoader)

        generated_dlf_yaml_dict = generate_dlf_yaml(placeholder_yaml)

        # print template yamls with replacements in place
        print('Generated DLF YAML dict: ')
        print(generated_dlf_yaml_dict)

        print('Generated DLF YAML file: ')
        print(generate_dlf_yaml(placeholder_yaml))

    except Exception as ex:
        print(ex)
