# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [29-Dec-2021] v0.2.3

### Changed

- Applied `black` formatting
- Added idempotent function for NSX ALB Profiles

## [29-Dec-2021] v0.2.2

### Changed

- Added pretty-print function to `namshub`
- Added HTTP, TLS profiles to `nsx-alb`
- Fixed an issue where the URL validation function was always performed on `cogitation_endpoint`
- More JSON Double-Encoding fixes

## [28-Dec-2021] v0.2.1

### Changed

- Found an issue where double JSON encoding caused problems with the Avi API
- Avi API Library]

## [28-Dec-2021] v0.2.0

### Changed

- Fixed Typo in `namshub`
- Set `namshub` to process input for a given payload to be a file or a string
- Fixed an issue where `args.dryrun` wasn't processed by `main` due to overly complex flow logic
- Cleaned up `main`'s flow logic

## [25-Dec-2021] v0.1.13

### Added

- Provide a way to just dump a payload into the `namshub` function
- Function wrappers that return a `dict`
- Semantically versioned TLS settings

### Changed

- Set NSX Endpoint hostname via Environment Variable instead of in the settings file

## [21-Nov-2021] v0.1.12

### Changed

- Idiomatic if causes some issues, used a normal if

## [21-Nov-2021] v0.1.11

### Changed

- Modified payload API - it'll use `dict` member replacement from `vars` instead

## [21-Nov-2021] v0.1.10

### Changed

- `namshub` returns the API result

## [20-Nov-2021] v0.1.9

### Added

- `PUT` method
- More NSX-T Plays
- Error handling on templates, URI fetching
- Generic `requests` method wrapper, we'll use it for payload verbs for now

### Changed

- `namshub` restructured to make a bit more sense, be faster, less wordy

## [20-Nov-2021] v0.1.8

### Added

- Generic wrapper (`namshub`)
- Payload and URI templating
- `json` `file` or `string` function

### Changed

- Headers moved to settings file as a required attribute instead of hard-coding

## [07-Nov-2021] v0.1.6

### Added

- `POST` verb
- `PATCH` verb
- Dry Run Capability
- Overloading to support a message body

### Changed

- Error handling improvements everywhere.
- Look for username and password from system args instead of storing passwords

## [06-Mar-2021] v0.1.5

### Added

- Moved classes to external source (outside of main)

### Changed

- Moved settings files to GH Pages

## [14-Feb-2021] Added GPG signing

### Added

- GPG signature
- Markdownlint settings
- Python packaging

## [13-Feb-2021] Start of Changelog

### Added

- Reamde
