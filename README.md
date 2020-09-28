### Installing from source code

To install the package from source code, run

```
$ git clone git@github.ibm.com:CODAIT/DAX-metadata-converter.git
$ cd DAX-metadata-converter
$ pip install .
```

## Running the template completer

Display help:

```
$ python template_completer/complete.py -h
```

Replace `{{...}}` placeholders in `my.template` with values from `my.yaml`. The completed template is displayed on STDOUT.

```
$ python template_completer/complete.py my.yaml my.template
```

Replace `{{...}}` placeholders in `my.template` with values from `my.yaml`. The completed template is stored in `my_completed.template`.

```
$ python template_completer/complete.py my.yaml my.template -o my_completed.template
```

## Examples

Example templates and YAML file can be found in [samples/](/samples).

## License

[Apache-2.0](LICENSE)
