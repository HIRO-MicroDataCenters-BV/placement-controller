from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.application_model import ApplicationModel
from ...models.http_validation_error import HTTPValidationError


def _get_kwargs(
    namespace: str,
    name: str,
    *,
    body: list[str],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/applications/{namespace}/{name}/placements".format(
            namespace=namespace,
            name=name,
        ),
    }

    _kwargs["json"] = body

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    body: list[str],
) -> Response[Union[ApplicationModel, HTTPValidationError]]:
    """Set Placements

    Args:
        namespace (str):
        name (str):
        body (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApplicationModel, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        namespace=namespace,
        name=name,
        body=body,
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
    body: list[str],
) -> Optional[Union[ApplicationModel, HTTPValidationError]]:
    """Set Placements

    Args:
        namespace (str):
        name (str):
        body (list[str]):

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
        body=body,
    ).parsed


async def asyncio_detailed(
    namespace: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list[str],
) -> Response[Union[ApplicationModel, HTTPValidationError]]:
    """Set Placements

    Args:
        namespace (str):
        name (str):
        body (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ApplicationModel, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        namespace=namespace,
        name=name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    namespace: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list[str],
) -> Optional[Union[ApplicationModel, HTTPValidationError]]:
    """Set Placements

    Args:
        namespace (str):
        name (str):
        body (list[str]):

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
            body=body,
        )
    ).parsed
