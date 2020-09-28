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
from argparse import ArgumentParser
import re
import yaml


# Raised if template contains a placeholder
# which cannot be resolved.
class PlaceholderNotFoundError(Exception):
    pass


def generate(yaml_dict, template):

    # Helper; attempts to resolve a placeholder
    # using the values provided in yaml_dict
    # Raises PlaceholderNotFoundError
    def replace_placeholder(match):
        root = yaml_dict

        for property in match.group(1).split('.'):
            root = root.get(property)
            if root is None:
                raise PlaceholderNotFoundError(match.group(1))
        return root

    if yaml_dict is None or template is None:
        # nothing to do
        return None

    # compile the {{...}} placeholder search expression
    p = re.compile('{{([a-zA-Z_.]+)}}', re.VERBOSE)

    template_out = []
    # replace placeholders in the template
    for line in template:
        template_out.append(p.sub(replace_placeholder, line))
    return template_out


# Main entry point
if __name__ == "__main__":

    parser = ArgumentParser(
                description='Populate a template file using '
                            'values from a YAML file.')
    parser.add_argument('input_yaml',
                        help='YAML file containing placeholder values')
    parser.add_argument('template',
                        help='Template file to be completed')
    parser.add_argument('-o', '--output', default=None,
                        help='Output file name. If not specified '
                              'output is sent to STDOUT.')
    args = parser.parse_args()

    try:
        # load the input YAML
        with open(args.input_yaml, 'r') as source_yaml:
            in_yaml = yaml.load(source_yaml, Loader=yaml.FullLoader)

        # load template
        with open(args.template, 'r') as template_file:
            in_template = template_file.readlines()

        # replace placeholders in template
        completed_template = generate(in_yaml, in_template)

        # save completed template in file or STDOUT
        if args.output is not None:
            with open(args.output, 'w') as output_file:
                output_file.writelines(completed_template)
        else:
            for line in completed_template:
                print(line.rstrip())

    except FileNotFoundError:
        print('File {} was not found.'.format(args.input_yaml))
    except yaml.parser.ParserError as pe:
        # Input YAML file is not valid
        print('Error parsing file {}: {}'.format(args.input_yaml, str(pe)))
    except PlaceholderNotFoundError as pnfe:
        # Template file contains a placeholder, which is not defined
        # in the input YAML file
        print('Error processing template "{}". '
              '"{}" does not define property "{}"'
              .format(args.template, args.input_yaml, str(pnfe)))
