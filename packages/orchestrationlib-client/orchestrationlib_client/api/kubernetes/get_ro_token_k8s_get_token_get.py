from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...types import Unset


def _get_kwargs(
    *,
    namespace: Union[Unset, str] = "hiros",
    service_account_name: Union[Unset, str] = "readonly-user",
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["namespace"] = namespace

    params["service_account_name"] = service_account_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/k8s_get_token/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    namespace: Union[Unset, str] = "hiros",
    service_account_name: Union[Unset, str] = "readonly-user",
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Ro Token

     Get a read-only token for a specific service account in a namespace.
    If no namespace or service account name is provided, it returns an error.

    Args:
        namespace (str): The namespace of the service account.
        service_account_name (str): The name of the service account.

    Returns:
        JSONResponse: A response containing the read-only token or an error message.

    Args:
        namespace (Union[Unset, str]):  Default: 'hiros'.
        service_account_name (Union[Unset, str]):  Default: 'readonly-user'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        namespace=namespace,
        service_account_name=service_account_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    namespace: Union[Unset, str] = "hiros",
    service_account_name: Union[Unset, str] = "readonly-user",
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Ro Token

     Get a read-only token for a specific service account in a namespace.
    If no namespace or service account name is provided, it returns an error.

    Args:
        namespace (str): The namespace of the service account.
        service_account_name (str): The name of the service account.

    Returns:
        JSONResponse: A response containing the read-only token or an error message.

    Args:
        namespace (Union[Unset, str]):  Default: 'hiros'.
        service_account_name (Union[Unset, str]):  Default: 'readonly-user'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        namespace=namespace,
        service_account_name=service_account_name,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    namespace: Union[Unset, str] = "hiros",
    service_account_name: Union[Unset, str] = "readonly-user",
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Ro Token

     Get a read-only token for a specific service account in a namespace.
    If no namespace or service account name is provided, it returns an error.

    Args:
        namespace (str): The namespace of the service account.
        service_account_name (str): The name of the service account.

    Returns:
        JSONResponse: A response containing the read-only token or an error message.

    Args:
        namespace (Union[Unset, str]):  Default: 'hiros'.
        service_account_name (Union[Unset, str]):  Default: 'readonly-user'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        namespace=namespace,
        service_account_name=service_account_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    namespace: Union[Unset, str] = "hiros",
    service_account_name: Union[Unset, str] = "readonly-user",
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Ro Token

     Get a read-only token for a specific service account in a namespace.
    If no namespace or service account name is provided, it returns an error.

    Args:
        namespace (str): The namespace of the service account.
        service_account_name (str): The name of the service account.

    Returns:
        JSONResponse: A response containing the read-only token or an error message.

    Args:
        namespace (Union[Unset, str]):  Default: 'hiros'.
        service_account_name (Union[Unset, str]):  Default: 'readonly-user'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            namespace=namespace,
            service_account_name=service_account_name,
        )
    ).parsed
