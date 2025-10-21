from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.placement_decision_out import PlacementDecisionOut


def _get_kwargs(
    namespace: str,
    name: str,
    decision_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/placement_decisions/{namespace}/{name}/{decision_id}".format(
            namespace=namespace,
            name=name,
            decision_id=decision_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PlacementDecisionOut]]:
    if response.status_code == 200:
        response_200 = PlacementDecisionOut.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, PlacementDecisionOut]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    namespace: str,
    name: str,
    decision_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, PlacementDecisionOut]]:
    """Get Decision

     Get a specific placement decision

    Args:
        namespace (str):
        name (str):
        decision_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PlacementDecisionOut]]
    """

    kwargs = _get_kwargs(
        namespace=namespace,
        name=name,
        decision_id=decision_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    namespace: str,
    name: str,
    decision_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, PlacementDecisionOut]]:
    """Get Decision

     Get a specific placement decision

    Args:
        namespace (str):
        name (str):
        decision_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PlacementDecisionOut]
    """

    return sync_detailed(
        namespace=namespace,
        name=name,
        decision_id=decision_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    namespace: str,
    name: str,
    decision_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, PlacementDecisionOut]]:
    """Get Decision

     Get a specific placement decision

    Args:
        namespace (str):
        name (str):
        decision_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PlacementDecisionOut]]
    """

    kwargs = _get_kwargs(
        namespace=namespace,
        name=name,
        decision_id=decision_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    namespace: str,
    name: str,
    decision_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, PlacementDecisionOut]]:
    """Get Decision

     Get a specific placement decision

    Args:
        namespace (str):
        name (str):
        decision_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PlacementDecisionOut]
    """

    return (
        await asyncio_detailed(
            namespace=namespace,
            name=name,
            decision_id=decision_id,
            client=client,
        )
    ).parsed
