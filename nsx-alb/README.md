# NSX Advanced Load Balancer

## Tested Versions

* NSX ALB 21.1.3

## Platform Idiosyncracies

* APIDocs do not include the root URI (`/api`)
* Basic Authentication must be globally enabled for the API to work
  * Under Settings -> Access Settings
* There's still some weird `json` formatting issue with this API
