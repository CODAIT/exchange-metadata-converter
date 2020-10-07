[![Build Status](https://travis-ci.org/CODAIT/exchange-metadata-converter.svg?branch=main)](https://travis-ci.org/CODAIT/exchange-metadata-converter)

## Setup

### Installing from source code

To install the package from source code, run

```
$ git clone https://github.com/CODAIT/exchange-metadata-converter.git
$ cd exchange-metadata-converter
$ pip install .
```

### Validation

The package should pass flake8 and the unit tests in the [`/tests`](/tests) directory.

 ```
 $ pip install -r test_requirements.txt
 $ flake8 .
 $ python -m unittest tests/*.py
 ```

## Running the converter

Display help:

```
$ python metadata_converter/apply.py -h
```

Replace `{{...}}` placeholders in `my.template` with values from `my.yaml`. The completed template is displayed on STDOUT.

```
$ python metadata_converter/apply.py my.yaml my.template
```

Replace `{{...}}` placeholders in `my.template` with values from `my.yaml`. The completed template is stored in `my_completed.template`.

```
$ python metadata_converter/apply.py my.yaml my.template -o my_completed.template
```

## Templates

Example template files for DLF and OpenAIHub can be found in the [templates/](/templates) directory.

## DAX data set descriptors

Descriptor files for DAX data sets can be found in the [dax-data-set-descriptors/](/dax-data-set-descriptors) directory.

## License

[Apache-2.0](LICENSE)
