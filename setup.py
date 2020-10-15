#
# Copyright 2018-2020 IBM Corporation
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
from setuptools import find_packages
from setuptools import setup

with open('README.md') as readme:
    README = readme.read()

setup(
  name='exchange-metadata-converter',
  packages=find_packages(),
  version='0.0.7',
  license='Apache-2.0',
  description='exchange metadata converters',
  long_description=README,
  long_description_content_type='text/markdown',
  author='CODAIT',
  author_email='ptitzler@us.ibm.com',
  url='https://github.com/CODAIT/exchange-metadata-converter',
  keywords=['YAML templating engine'],
  install_requires=[
    'importlib-resources',
    'ruamel.yaml'
  ],
  include_package_data=True,
  classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
  zip_safe=True
)
