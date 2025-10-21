from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.workload_request_decision_update import WorkloadRequestDecisionUpdate
from uuid import UUID


def _get_kwargs(
    decision_id: UUID,
    *,
    body: WorkloadRequestDecisionUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/workload_request_decision/{decision_id}".format(
            decision_id=decision_id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, WorkloadRequestDecisionUpdate]]:
    if response.status_code == 200:
        response_200 = WorkloadRequestDecisionUpdate.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, WorkloadRequestDecisionUpdate]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    decision_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkloadRequestDecisionUpdate,
) -> Response[Union[HTTPValidationError, WorkloadRequestDecisionUpdate]]:
    """Update Workload Decision Route

     Update an existing WorkloadRequestDecision by ID.

    Args:
        decision_id (UUID): The ID of the pod decision to update.
        data (WorkloadRequestDecisionUpdate): Fields to update.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadDecisionSchema: The updated pod decision.

    Args:
        decision_id (UUID):
        body (WorkloadRequestDecisionUpdate): Schema for workload update decision.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, WorkloadRequestDecisionUpdate]]
    """

    kwargs = _get_kwargs(
        decision_id=decision_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    decision_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkloadRequestDecisionUpdate,
) -> Optional[Union[HTTPValidationError, WorkloadRequestDecisionUpdate]]:
    """Update Workload Decision Route

     Update an existing WorkloadRequestDecision by ID.

    Args:
        decision_id (UUID): The ID of the pod decision to update.
        data (WorkloadRequestDecisionUpdate): Fields to update.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadDecisionSchema: The updated pod decision.

    Args:
        decision_id (UUID):
        body (WorkloadRequestDecisionUpdate): Schema for workload update decision.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, WorkloadRequestDecisionUpdate]
    """

    return sync_detailed(
        decision_id=decision_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    decision_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkloadRequestDecisionUpdate,
) -> Response[Union[HTTPValidationError, WorkloadRequestDecisionUpdate]]:
    """Update Workload Decision Route

     Update an existing WorkloadRequestDecision by ID.

    Args:
        decision_id (UUID): The ID of the pod decision to update.
        data (WorkloadRequestDecisionUpdate): Fields to update.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadDecisionSchema: The updated pod decision.

    Args:
        decision_id (UUID):
        body (WorkloadRequestDecisionUpdate): Schema for workload update decision.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, WorkloadRequestDecisionUpdate]]
    """

    kwargs = _get_kwargs(
        decision_id=decision_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    decision_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkloadRequestDecisionUpdate,
) -> Optional[Union[HTTPValidationError, WorkloadRequestDecisionUpdate]]:
    """Update Workload Decision Route

     Update an existing WorkloadRequestDecision by ID.

    Args:
        decision_id (UUID): The ID of the pod decision to update.
        data (WorkloadRequestDecisionUpdate): Fields to update.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadDecisionSchema: The updated pod decision.

    Args:
        decision_id (UUID):
        body (WorkloadRequestDecisionUpdate): Schema for workload update decision.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, WorkloadRequestDecisionUpdate]
    """

    return (
        await asyncio_detailed(
            decision_id=decision_id,
            client=client,
            body=body,
        )
    ).parsed
