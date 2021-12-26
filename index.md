# Python REST Tool

## Objectives

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

* Provide a direct, straightforward method to interact with RESTful interfaces (`namshub`)
* Save typing time by DRY (*Don't Repeat Yourself*), enable templating(`Jinja2`) to prevent unnecessary repetition
* Retain settings between known good procedures, _without hard-coding actions_
* Enable rapid iteration, recording actions and procedures for later
* Enable users to save a simple library of actions for later. The objective here is *repeatability*.
* Provide acceptable quality error-handling and intuitive error exposure to the user

## Saved Libraries

* [NSX-T](https://github.com/ngschmidt/python-restify/blob/main/nsx-t/settings.json)

## API Documentation

* [Library](doc/)
* [NSX-T](doc/nsxt/)

## How to use this tool

### Building a Settings file, Environment Setup

Download the package:

```bash
python3 -m pip install restify-ENGYAK
```
To build a new settings file:

```bash
python3 -m restify create_settings > settings.json
```

To list plays provided by a settings file:

```bash
python3 -m restify -f settings.json list_plays
```

Set Environment Variables. `APIUSER` and `APIPASS` are mandatory.

```bash
export APIUSER=username
export APIPASS=password
export APIENDPOINT={{ API Full URL }}
```

### CLI Invocation

Invoke via the CLI:

```bash
python3 -m restify -f settings.json list_plays
```

Leverage the `help` file for more details on supported functions:

```bash
python3 -m restify --help
```

Congratulate yourself on your new responsibility as an automation maintainer!

### API Invocation

The package `restify-ENGYAK` provides two python classes:

* `restify.RuminatingCogitation.Settings`: Storage class for the endpoint definition and settings. Not used, it's just here to help generate settings files. Completely viable alternative to Jinja if that better fits consumption models
  * _This is not a mandatory attribute to `import` for API Invocation!_
* `restify.RuminatingCogitation.Reliiquary`: Storage class for saved plays. Has a "constructor" to connect to an endpoint, and functions (formatted as `do_api_<verb>`) invoke further actions from there.

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

## Customizing this tool

The primary value here is customization. This project will provide a limited subset of shared plays, but these `reliquaries` are the consumer's responsibility.

```bash
python3 -m restify create_settings > new_file.json
```

The vast majority of this generated file is for HTTP error handling - and won't need any work unless there are some idiosyncracies with the endpoint. `restify` will test access to all keys before starting, which should provide intuitive error handling if a file isn't formatted properly.

Customization for a new endpoint should begin here:

```json
    "settings": {
        "authentication": {
            "certificate": "",
            "key": ""
        },
        "tls": {
            "validation": false
        },
        "verbosity": 1,
        "headers": {
            "content-type": "application/json",
            "X-Allow-Overwrite": "true"
        },
    },
    "plays": {},
```

### Adding `namshubs`

Plays will have a common format:

```json
"get_tier0_routes": {
    "uri": "/policy/api/v1/infra/tier-0s/{{ id }}/forwarding-table",
    "description": "Get Tier-0 Logical Router Table (requires ID variable)",
    "method": "GET",
    "requiresvariables": true,
    "variables": { 
        "id": false
    }
}
```

* Name: The key for each _play_ is the name that the `namshub` API or the CLI will invoke
  * `uri`: The uniform resource indicator to access on a particular endpoint
  * `description`: This is for us - describe what the API endpoint does
  * `method`: Specify the HTTP verb. Acceptable parameters are `["GET", "POST", "PATCH", "PUT", "DELETE"]`
  * `requiresvariables`: Specify that the play will require `Jinja2` templating (*optional*)
  * `requirespayload`: Specify that the play will require a text body/payload (*optional*)
  * `variables`: Provide a `json dict` of key-value pairs to apply against the play
    * This structure will be used to validate what a user enters in, and isn't used directly
    * Example: `python3 -m restify -f settings.json --vars '{\"id\": \"deadbeef\"}`
  * `payload`: Provide a `document` to send to the API endpoint.
    * This is not processed as a dict, but instead as a string
    * Jinja2 will apply variables to both this and the URI
