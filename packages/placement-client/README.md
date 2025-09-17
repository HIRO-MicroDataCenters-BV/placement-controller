# Python client
API version: 1.0.0

## Requirements

- Python 3.10+
- Docker engine. [Documentation](https://docs.docker.com/engine/install/)

## Installation & Usage

1. If you don't have `Poetry` installed run:

```bash
pip install poetry
```

2. Install dependencies:

```bash
poetry config virtualenvs.in-project true
poetry install --no-root
```

3. Running tests:

```bash
poetry run pytest
```

You can test the application for multiple versions of Python. To do this, you need to install the required Python versions on your operating system, specify these versions in the tox.ini file, and then run the tests:
```bash
poetry run tox
```
Add the tox.ini file to `client/.openapi-generator-ignore` so that it doesn't get overwritten during client generation.

4. Building package:

```bash
poetry build
```

5. Publishing
```bash
poetry config pypi-token.pypi <pypi token>
poetry publish
```

## Client generator
To generate the client, execute the following script from the project root folder
```bash
poetry --directory server run python ./tools/client_generator/generate.py ./api/openapi.yaml
```

### Command
```bash
generate.py <file> [--asyncio]
```

#### Arguments
**file**
Specifies the input OpenAPI specification file path or URL. This argument is required for generating the Python client. The input file can be either a local file path or a URL pointing to the OpenAPI schema.

**--asyncio**
Flag to indicate whether to generate asynchronous code. If this flag is provided, the generated Python client will include asynchronous features. By default, synchronous code is generated.

#### Configuration
You can change the name of the client package in the file `/tools/client_generator/config.json`.

Add file's paths to `client/.openapi-generator-ignore` so that it doesn't get overwritten during client generation.

#### Examples

```bash
python generate.py https://<domain>/openapi.json
python generate.py https://<domain>/openapi.json --asyncio
python generate.py /<path>/openapi.yaml
python generate.py /<path>/openapi.yaml --asyncio
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python

import placement_client
from placement_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = placement_client.Configuration(
    host = "http://localhost"
)



# Enter a context with an instance of the API client
async with placement_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = placement_client.DefaultApi(api_client)

    try:
        # List Applications
        api_response = await api_instance.list_applications_applications_get()
        print("The response of DefaultApi->list_applications_applications_get:\n")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->list_applications_applications_get: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *http://localhost*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*DefaultApi* | [**list_applications_applications_get**](docs/DefaultApi.md#list_applications_applications_get) | **GET** /applications/ | List Applications
*DefaultApi* | [**root_get**](docs/DefaultApi.md#root_get) | **GET** / | Root
*DefaultApi* | [**set_owner_applications_namespace_name_owner_put**](docs/DefaultApi.md#set_owner_applications_namespace_name_owner_put) | **PUT** /applications/{namespace}/{name}/owner | Set Owner
*DefaultApi* | [**set_placements_applications_namespace_name_placements_put**](docs/DefaultApi.md#set_placements_applications_namespace_name_placements_put) | **PUT** /applications/{namespace}/{name}/placements | Set Placements


## Documentation For Models

 - [ApplicationModel](docs/ApplicationModel.md)
 - [HTTPValidationError](docs/HTTPValidationError.md)
 - [ValidationError](docs/ValidationError.md)
 - [ValidationErrorLocInner](docs/ValidationErrorLocInner.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization

Endpoints do not require authorization.


## Author

all-hiro@hiro-microdatacenters.nl

