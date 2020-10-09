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


def replace(yaml_dict, template_dict):
    """Replace matched {{...}} in template_dict with values from yaml_dict

    :param yaml_dict: dict representation of a YAML document defining
    placeholder values
    :type yaml_dict: dict
    :param template_dict: dict representation of a YAML document containing
    '{{...}}' string placeholders
    :type template_dict: dict
    :raises PlaceholderNotFoundError: a {{...}} placeholder in template_dict
    was not found in yaml_dict
    :raises ValueError: at least one input parameter is invalid
    :raises NotImplementedError: [description]
    :return: yaml_dict with all '{{...}}' replaced
    :rtype: dict
    """

    # pre-compile the {{...}} placeholder search expression
    # outside `do_replace` to avoid doing it multiple times
    p = re.compile(r'{{([\w\.]+)}}', re.VERBOSE)

    def process_string(yaml_dict, str):
        # determine whether {{...}} placeholder
        # replacement is required
        r = p.search(str)
        if r is None:
            return str
        else:
            root = yaml_dict
            for property in r.group(1).split('.'):
                root = root.get(property)
                if root is None:
                    raise PlaceholderNotFoundError(r.group(1))
            return root

    def process_list(yaml_dict, list_in):
        list_out = []
        for v in list_in:
            # if v is a string process it
            if(isinstance(v, str)):
                list_out.append(process_string(yaml_dict, v))
            elif(isinstance(v, dict)):
                list_out.append(do_replace(yaml_dict, v))
            elif(isinstance(v, list)):
                list_out.append(process_list(yaml_dict, v))
            else:
                raise NotImplementedError(
                        'Support for properties of type {} in lists '
                        'is not implemented.'
                        .format(type(v)))
        return list_out

    # Recursive function does the actual work
    def do_replace(yaml_dict, template_dict):

        if yaml_dict is None or template_dict is None:
            # nothing to do
            return None

        if not isinstance(yaml_dict, dict):
            raise ValueError('Parameter \'yaml_dict\' must be of type '
                             '\'dict\' not {}.'.format(type(yaml_dict)))

        if not isinstance(template_dict, dict):
            raise ValueError('Parameter \'template_dict\' must be of type '
                             '\'dict\' not {}.'.format(type(template_dict)))

        template_out = {}
        # replace placeholders in the template, one value at a time
        for key in template_dict.keys():
            val = template_dict[key]
            # print('Key: {} Value: {} Type: {}'.format(key, val, type(val)))
            if val is None:
                # NoneType - no value
                template_out[key] = None
            elif isinstance(val, str):
                # process string
                template_out[key] = process_string(yaml_dict, val)
            elif isinstance(val, dict):
                # process the dictionary recursively
                template_out[key] = do_replace(yaml_dict, val)
            elif isinstance(val, list):
                # process each list item
                template_out[key] = process_list(yaml_dict, val)
            else:
                raise NotImplementedError(
                        'Support for properties of type {} is not implemented.'
                        .format(type(val)))

        return template_out

    return do_replace(yaml_dict, template_dict)


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
    parser.add_argument('--yaml_dump_null_as_empty',
                        action='store_true',
                        help='If specified, null values are dumped '
                             'as empty string, e.g. "mykey: null" is '
                             'dumped as "mykey: "')
    args = parser.parse_args()

    try:
        # load the input YAML
        with open(args.input_yaml, 'r') as source_yaml:
            in_yaml = yaml.load(source_yaml, Loader=yaml.FullLoader)

        # load template
        with open(args.template, 'r') as template_file:
            in_template = yaml.load(template_file, Loader=yaml.FullLoader)

        # replace placeholders in template
        out_yaml = replace(in_yaml, in_template)

        if args.yaml_dump_null_as_empty:
            # dump NoneType as an empty string `` instead of `null`
            yaml.SafeDumper.add_representer(
                type(None),
                lambda dumper, value:
                    dumper.represent_scalar('tag:yaml.org,2002:null',
                                            ''))

        # save completed template in file or STDOUT
        if args.output is not None:
            with open(args.output, 'w') as output_file:
                yaml.dumsafe_dump(out_yaml,
                                  output_file,
                                  default_flow_style=False,
                                  allow_unicode=True,
                                  sort_keys=False)
        else:
            print(yaml.safe_dump(out_yaml,
                                 default_flow_style=False,
                                 allow_unicode=True,
                                 sort_keys=False))

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
