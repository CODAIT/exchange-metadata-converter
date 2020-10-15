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
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.tokens import CommentToken
from ruamel.yaml.comments import CommentedMap
import re
import sys

yaml = YAML()


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

    def get_metadata(template_dict, key):
        # If d is an instance of ruamel.yaml.comments.CommentedMap
        # this method returns the metadata associated with the
        # provided property key

        if not isinstance(template_dict, CommentedMap):
            return None

        d = template_dict

        metadata = {
            'comment': None,
            'comment_text': None,
            'annotations': set()
        }
        # raw comment, e.g. "# @optional another comment\n"
        if key in d.ca.items:
            if (len(d.ca.items.get(key)) > 2) and \
               isinstance(d.ca.items.get(key)[2], CommentToken):
                metadata['comment'] = d.ca.items.get(key)[2].value
        # comment text, e.g. "another comment"
        metadata['comment_text'] = metadata['comment']
        # extract embedded annotations, e.g. "@optional"
        if metadata['comment'] is not None:
            # Extract @... annotations
            for match in re.finditer('@([a-zA-Z]+)',
                                     metadata['comment'],
                                     re.I):
                metadata['annotations'].add(match.group(1).lower())
            # Remove noise from the comment, such as annotations
            # comment characters and whitespace characters
            #  - Remove annotations
            for annotation in metadata['annotations']:
                metadata['comment_text'] =\
                    metadata['comment_text'].replace('@{}'.format(annotation),
                                                     '')
            #  - Remove '#' and whitespaces from the beginning of each line
            #    This needs to be done twice to handle empty comments properly.
            metadata['comment_text'] = re.sub(r'^\s*#\s*',
                                              '',
                                              metadata['comment_text'],
                                              flags=re.MULTILINE)
            metadata['comment_text'] = re.sub(r'^\s*#\s*',
                                              '',
                                              metadata['comment_text'],
                                              flags=re.MULTILINE)
            #  - remove whitespace chars from the end of each line
            metadata['comment_text'] = re.sub(r'\s*$',
                                              '',
                                              metadata['comment_text'],
                                              flags=re.MULTILINE)

            #  - remove newline from the end
            metadata['comment_text'] = metadata['comment_text'].strip()

            if len(metadata['comment_text']) == 0:
                metadata['comment_text'] = None
        return metadata

    # pre-compile the {{...}} placeholder search expression
    # outside `do_replace` to avoid doing it multiple times
    p = re.compile(r'{{([\w\.]+)}}', re.VERBOSE)

    def process_string(yaml_dict, str, metadata):
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
                    # check annotations to determine appropriate
                    # behavior
                    if metadata is not None and\
                       'optional' in metadata['annotations']:
                        return None
                    else:
                        raise PlaceholderNotFoundError(r.group(1))
            return root

    def process_list(yaml_dict, list_in, metadata):
        list_out = []
        for v in list_in:
            # if v is a string process it
            if(isinstance(v, str)):
                list_out.append(process_string(yaml_dict, v, metadata))
            elif(isinstance(v, dict)):
                list_out.append(do_replace(yaml_dict, v))
            elif(isinstance(v, list)):
                list_out.append(process_list(yaml_dict, v, metadata))
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
            metadata = get_metadata(template_dict, key)
            if val is None:
                # NoneType - no value
                template_out[key] = None
            elif isinstance(val, str):
                # process string
                template_out[key] = process_string(yaml_dict,
                                                   val,
                                                   metadata)
            elif isinstance(val, dict):
                # process the dictionary recursively
                template_out[key] = do_replace(yaml_dict, val)
            elif isinstance(val, list):
                # process each list item
                template_out[key] = process_list(yaml_dict,
                                                 val,
                                                 metadata)
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
    args = parser.parse_args()

    try:
        # load the input YAML
        in_yaml = yaml.load(Path(args.input_yaml))

        # load template YAML
        in_template = yaml.load(Path(args.template))

        # replace placeholders in template
        out_yaml = replace(in_yaml, in_template)

        yaml.indent(mapping=2, sequence=4, offset=2)

        # save completed template in file or STDOUT
        if args.output is not None:
            with open(args.output, 'w') as output_file:
                yaml.dump(out_yaml, output_file)
        else:
            yaml.dump(out_yaml, sys.stdout)

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
