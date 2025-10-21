from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.workload_timing_schema import WorkloadTimingSchema
from ...models.workload_timing_update import WorkloadTimingUpdate


def _get_kwargs(
    workload_timing_id: str,
    *,
    body: WorkloadTimingUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/workload_timing/{workload_timing_id}".format(
            workload_timing_id=workload_timing_id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, WorkloadTimingSchema]]:
    if response.status_code == 200:
        response_200 = WorkloadTimingSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, WorkloadTimingSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workload_timing_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkloadTimingUpdate,
) -> Response[Union[HTTPValidationError, WorkloadTimingSchema]]:
    """Update Workload Timing Route

     Update an existing WorkloadTiming entry.

    Args:
        workload_timing_id (str): The ID of the workload timing to update.
        data (WorkloadTimingCreate): The updated workload timing data.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadTimingSchema: The updated workload timing.

    Args:
        workload_timing_id (str):
        body (WorkloadTimingUpdate): Schema for updating a workload timing.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, WorkloadTimingSchema]]
    """

    kwargs = _get_kwargs(
        workload_timing_id=workload_timing_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workload_timing_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkloadTimingUpdate,
) -> Optional[Union[HTTPValidationError, WorkloadTimingSchema]]:
    """Update Workload Timing Route

     Update an existing WorkloadTiming entry.

    Args:
        workload_timing_id (str): The ID of the workload timing to update.
        data (WorkloadTimingCreate): The updated workload timing data.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadTimingSchema: The updated workload timing.

    Args:
        workload_timing_id (str):
        body (WorkloadTimingUpdate): Schema for updating a workload timing.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, WorkloadTimingSchema]
    """

    return sync_detailed(
        workload_timing_id=workload_timing_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    workload_timing_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkloadTimingUpdate,
) -> Response[Union[HTTPValidationError, WorkloadTimingSchema]]:
    """Update Workload Timing Route

     Update an existing WorkloadTiming entry.

    Args:
        workload_timing_id (str): The ID of the workload timing to update.
        data (WorkloadTimingCreate): The updated workload timing data.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadTimingSchema: The updated workload timing.

    Args:
        workload_timing_id (str):
        body (WorkloadTimingUpdate): Schema for updating a workload timing.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, WorkloadTimingSchema]]
    """

    kwargs = _get_kwargs(
        workload_timing_id=workload_timing_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workload_timing_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkloadTimingUpdate,
) -> Optional[Union[HTTPValidationError, WorkloadTimingSchema]]:
    """Update Workload Timing Route

     Update an existing WorkloadTiming entry.

    Args:
        workload_timing_id (str): The ID of the workload timing to update.
        data (WorkloadTimingCreate): The updated workload timing data.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadTimingSchema: The updated workload timing.

    Args:
        workload_timing_id (str):
        body (WorkloadTimingUpdate): Schema for updating a workload timing.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, WorkloadTimingSchema]
    """

    return (
        await asyncio_detailed(
            workload_timing_id=workload_timing_id,
            client=client,
            body=body,
        )
    ).parsed
