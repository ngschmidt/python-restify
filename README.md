# Python REST Tool

## Synopsis

Provide a python tool to quickly invoke REST calls with a pre-defined list of settings, plays.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## How to use this tool

Invoke via the CLI:

```bash
python3 resttool.py -f settings.json get_api-object
```

To build a new settings file:

```bash
python3 resttool.py create_settings > settings.json
```

To list plays provided by a settings file:

```bash
python3 resttool.py -f settings.json list_plays
```

## Notes

I'm working on module packaging.

## TODO

* Module-level invocation
* More Content
* Automated testing

## Authors

* *Nick Schmidt*
