# Python REST Tool

## Synopsis

Provide a python tool to quickly invoke REST calls with a pre-defined list of settings, plays.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## How to use this tool

Download the package:

```bash
python3 -m pip install restify-ENGYAK
```

Set Environment Variables. `APIUSER` and `APIPASS` are mandatory.

```bash
export APIUSER=username
export APIPASS=password
export APIENDPOINT={{ API Full URL }}
```

Invoke via the CLI:

```bash
python3 -m restify -f settings.json list_plays
```

To build a new settings file:

```bash
python3 -m restify create_settings > settings.json
```

To list plays provided by a settings file:

```bash
python3 -m restify -f settings.json list_plays
```

## API Invocation

Once the package is installed, the `namshub()` API can be used by:

```python
# Import Restify Library
from restify.RuminatingCogitation import Settings
from restify.RuminatingCogitation import Reliquary
# Set the interface - apply from variables no matter what
cogitation_interface = Reliquary(args.f, input_user=api_user, input_pass=api_pass)
# Exposed variables: def namshub(self, namshub_string, namshub_variables=False, namshub_dryrun=False):
cogitation_interface.namshub({{ }}, namshub_variables={{ }})
```

And then process data from there.
`namshub` currently exports text from the API, and may support a `dict` in the future.

## Notes

## Authors

* *Nick Schmidt*
