# Python REST Tool

## Software Objectives

* Provide a direct, straightforward method to interact with RESTful interfaces
* Save typing time by DRY (`Don't Repeat Yourself`)
* Retain settings between "plays"
* Enable rapid iteration, recording "plays" for later

## How to use this tool

Download the package:

```bash
python3 -m pip install restify-ENGYAK
```

Invoke via the CLI:

```bash
python3 -m restify -f settings.json get_api-object
```

To build a new settings file:

```bash
python3 -m restify create_settings > settings.json
```

To list plays provided by a settings file:

```bash
python3 -m restify -f settings.json list_plays
```

## Customizing this tool

The primary value here is customization. This project will provide a limited subset of shared plays, but these `reliquaries` are the consumer's responsibility.

To create a new custom `reliquary,` generate a new file:

```bash
python3 -m restify create_settings > new_file.json
```

The vast majority of this generated file is for HTTP error handling - and won't need any work unless there are some idiosyncracies with the endpoint. Customization for a new endpoint should begin here:

```json
    "settings": {
        "authentication": {
            "username": "admin",
            "password": "password",
            "method": "basic",
            "certificate": "",
            "key": ""
        },
        "tls": {
            "validation": false
        },
        "verbosity": 1,
        "endpoint": ""
    },
    "plays": {},
```

## Templating

Generally, this tool's design intent is to use a `settings file` per endpoint. With repeatable endpoints, it would be an opinionated recommendation to leverage Jinja2 templates as follows:

Create a new Jinja2 template

```bash
python3 -m restify create_settings | sed 's/"endpoint": "{{ endpoint }}" > endpoint_template.j2
```

Generate some Python templating code:

```python
# Import Jinja2 modules
from jinja2 import Environment, FileSystemLoader

# Create Environment
local_env = Environment(loader=FileSystemLoader("."))

# Load Endpoint Template
endpoint_template = local_env.get_template("endpoint_template.j2")
print(endpoint_template.render(endpoint="https://abcdef.engyak.net/"))
```

Congratulate yourself on your new responsibility as an automation maintainer!

## Leveraging this as a Python class

The package `restify-ENGYAK` provides two python classes:

* `RuminatingCogitationSettings`: Storage class for the endpoint definition and settings. Not used, it's just here to help generate settings files. Completely viable alternative to Jinja if that better fits consumption models
* `RuminatingCogitationReliiquary`: Storage class for saved plays. Has a "constructor" to connect to an endpoint, and functions (formatted as `do_api_<verb>`) invoke further actions from there.

These are freely available to customize.

## Saved Libraries

* [NSX-T](nsxt.json)
