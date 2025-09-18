from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.application_report import ApplicationReport


def _get_kwargs(
    namespace: str,
    name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/applications/{namespace}/{name}/status".format(
            namespace=namespace,
            name=name,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApplicationReport]:
    if response.status_code == 200:
        response_200 = ApplicationReport.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApplicationReport]:
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
) -> Response[ApplicationReport]:
    """Get Application Status

    Args:
        namespace (str):
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApplicationReport]
    """

    kwargs = _get_kwargs(
        namespace=namespace,
        name=name,
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
) -> Optional[ApplicationReport]:
    """Get Application Status

    Args:
        namespace (str):
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApplicationReport
    """

    return sync_detailed(
        namespace=namespace,
        name=name,
        client=client,
    ).parsed


async def asyncio_detailed(
    namespace: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApplicationReport]:
    """Get Application Status

    Args:
        namespace (str):
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApplicationReport]
    """

    kwargs = _get_kwargs(
        namespace=namespace,
        name=name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    namespace: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApplicationReport]:
    """Get Application Status

    Args:
        namespace (str):
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApplicationReport
    """

    return (
        await asyncio_detailed(
            namespace=namespace,
            name=name,
            client=client,
        )
    ).parsed
