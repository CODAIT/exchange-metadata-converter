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
from pathlib import Path
from ruamel.yaml import YAML
import io
import sys
import templates

yaml = YAML()
yaml.default_flow_style = False


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

    buf = io.StringIO()
    yaml.dump(dlf_yaml_dict, buf)

    return buf.getvalue()


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
    dlf_template_yaml = yaml.load(dlf_yaml)

    # replace placeholders in in_template_yaml with values from
    # in_placeholder_yaml
    dlf_yaml_dict = replace(in_yaml, dlf_template_yaml)

    return dlf_yaml_dict


def generate_oah_yaml(in_yaml):
    """
    Generate OpenAIHub-compatible YAML configuration file using
    "templates/openaihub_out.yaml" as template.

    :param in_yaml: dict representation of a YAML document defining
    placeholder values in "templates/openaihub_out.yaml"
    :type in_yaml: dict
    :raises PlaceholderNotFoundError: a {{...}} placeholder referenced
    in "templates/openaihub_out.yaml" was not found
    :raises ValueError in_yaml is not of type dict
    :return: OpenAIHub-compatible YAML file
    :rtype: str
    """

    oah_yaml_dict = generate_oah_yaml_dict(in_yaml)

    buf = io.StringIO()
    yaml.dump(oah_yaml_dict, buf)

    return buf.getvalue()


def generate_oah_yaml_dict(in_yaml):
    """
    Generate OpenAIHub-compatible YAML configuration using
    "templates/openaihub_out.yaml" as template.

    :param in_yaml: dict representation of a YAML document defining
    placeholder values in "templates/openaihub_out.yaml"
    :type in_yaml: dict
    :raises PlaceholderNotFoundError: a {{...}} placeholder referenced
    in "templates/openaihub_out.yaml" was not found
    :raises ValueError in_yaml is not of type dict
    :return: OpenAIHub-compatible YAML file
    :rtype: dict
    """

    oah_yaml = files(templates).joinpath('openaihub_out.yaml')

    oah_template_yaml = yaml.load(oah_yaml)

    # replace placeholders in in_template_yaml with values from
    # in_placeholder_yaml
    oah_yaml_dict = replace(in_yaml, oah_template_yaml)

    return oah_yaml_dict


#
# This example illustrates how to invoke the exchange metadata converter
# programmatically, using the DLF and OpenAIHub templates
# Required parameters:
# /path/to/placeholder/yaml see examples in dax-data-set-descriptors/
if __name__ == "__main__":

    try:

        if len(sys.argv) != 2:
            print('Usage: {} {}'
                  .format(sys.argv[0],
                          '/path/to/placeholder/yaml'))
            sys.exit(1)

        placeholder_yaml = yaml.load(Path(sys.argv[1]))

        # print template yamls with replacements in place
        print('Generated DLF YAML dict: \n{}'
              .format(generate_dlf_yaml_dict(placeholder_yaml)))

        print('Generated DLF YAML: \n{}'
              .format(generate_dlf_yaml(placeholder_yaml)))

        print('Generated OpenAIHub YAML dict: \n{}'
              .format(generate_oah_yaml_dict(placeholder_yaml)))

        print('Generated OpenAIHub YAML: \n{}'
              .format(generate_oah_yaml(placeholder_yaml)))

    except Exception as ex:
        raise (ex)
