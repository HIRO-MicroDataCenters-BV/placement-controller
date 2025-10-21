from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.workload_action import WorkloadAction
from uuid import UUID


def _get_kwargs(
    action_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/workload_action/{action_id}".format(
            action_id=action_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, WorkloadAction]]:
    if response.status_code == 200:
        response_200 = WorkloadAction.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, WorkloadAction]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    action_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, WorkloadAction]]:
    """Get Workload Action Route

     Retrieve a single workload action by ID.

    Args:
        action_id (UUID): The ID of the workload action to retrieve.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadAction: The workload action with the given ID.

    Args:
        action_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, WorkloadAction]]
    """

    kwargs = _get_kwargs(
        action_id=action_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    action_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, WorkloadAction]]:
    """Get Workload Action Route

     Retrieve a single workload action by ID.

    Args:
        action_id (UUID): The ID of the workload action to retrieve.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadAction: The workload action with the given ID.

    Args:
        action_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, WorkloadAction]
    """

    return sync_detailed(
        action_id=action_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    action_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, WorkloadAction]]:
    """Get Workload Action Route

     Retrieve a single workload action by ID.

    Args:
        action_id (UUID): The ID of the workload action to retrieve.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadAction: The workload action with the given ID.

    Args:
        action_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, WorkloadAction]]
    """

    kwargs = _get_kwargs(
        action_id=action_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    action_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, WorkloadAction]]:
    """Get Workload Action Route

     Retrieve a single workload action by ID.

    Args:
        action_id (UUID): The ID of the workload action to retrieve.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadAction: The workload action with the given ID.

    Args:
        action_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, WorkloadAction]
    """

    return (
        await asyncio_detailed(
            action_id=action_id,
            client=client,
        )
    ).parsed
