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
# which cannot be found.
class PlaceholderNotFoundError(Exception):
    def __init__(self, placeholder):
        self.placeholder = placeholder
        self.message = 'Placeholder "{}" was not found.'.format(placeholder)
        super().__init__(self.message)


# Raised if template contains a placeholder
# which cannot be properly resolved
class PlaceholderTypeNotSupportedError(Exception):
    def __init__(self, placeholder, type):
        self.placeholder = placeholder
        self.type = type
        self.message = 'Type "{}" is not supported for placeholder "{}".'\
            .format(type, placeholder)
        super().__init__(self.message)


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
        r = p.search(line)
        if r is None:
            template_out.append(line)
            continue

        replacements = replace_placeholder(r)
        if isinstance(replacements, str):
            template_out.append(
                line[:r.start()] +
                replacements + line[r.end():])
        elif isinstance(replacements, list):
            for replacement in replacements:
                if isinstance(replacement, str):
                    # "- <replacement>"
                    template_out.append(
                            line[:r.start()] + '- ' +
                            replacement + line[r.end():])
                elif isinstance(replacement, dict):
                    is_first = True
                    for key in replacement.keys():
                        # "- <replacement_key>: <replacement_value>"
                        if is_first:
                            template_out.append(
                                line[:r.start()] + '- ' +
                                key + ': ' +
                                replacement[key] +
                                line[r.end():])
                            is_first = False
                        else:
                            # "  <replacement_key>: <replacement_value>"
                            template_out.append(
                                line[:r.start()] + '  ' +
                                key + ': ' +
                                replacement[key] +
                                line[r.end():])
                else:
                    raise PlaceholderTypeNotSupportedError(
                            r.group(1),
                            type(replacement))

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

    except FileNotFoundError as fnfe:
        # One of the input files was not found
        print(str(fnfe))
    except yaml.parser.ParserError as pe:
        # Input YAML file is not valid
        print('Error parsing file {}: {}'.format(args.input_yaml, str(pe)))
    except PlaceholderNotFoundError as pnfe:
        # Template file contains a placeholder, which is not defined
        # in the input YAML file
        print('Error processing template "{}". '
              '"{}" does not define property "{}"'
              .format(args.template, args.input_yaml, pnfe.placeholder))
