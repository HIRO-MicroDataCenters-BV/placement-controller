from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.application_model import ApplicationModel
from ...models.http_validation_error import HTTPValidationError


def _get_kwargs(
    namespace: str,
    name: str,
    *,
    owner: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["owner"] = owner

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/applications/{namespace}/{name}/owner".format(
            namespace=namespace,
            name=name,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ApplicationModel, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = ApplicationModel.from_dict(response.json())

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
) -> Response[Union[ApplicationModel, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    namespace: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    owner: str,
) -> Response[Union[ApplicationModel, HTTPValidationError]]:
    """Set Owner

    Args:
        namespace (str):
        name (str):
        owner (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApplicationModel, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        namespace=namespace,
        name=name,
        owner=owner,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    namespace: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    owner: str,
) -> Optional[Union[ApplicationModel, HTTPValidationError]]:
    """Set Owner

    Args:
        namespace (str):
        name (str):
        owner (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApplicationModel, HTTPValidationError]
    """

    return sync_detailed(
        namespace=namespace,
        name=name,
        client=client,
        owner=owner,
    ).parsed


async def asyncio_detailed(
    namespace: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    owner: str,
) -> Response[Union[ApplicationModel, HTTPValidationError]]:
    """Set Owner

    Args:
        namespace (str):
        name (str):
        owner (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApplicationModel, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        namespace=namespace,
        name=name,
        owner=owner,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    namespace: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    owner: str,
) -> Optional[Union[ApplicationModel, HTTPValidationError]]:
    """Set Owner

    Args:
        namespace (str):
        name (str):
        owner (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ApplicationModel, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            namespace=namespace,
            name=name,
            client=client,
            owner=owner,
        )
    ).parsed
