from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.workload_request_decision_create import WorkloadRequestDecisionCreate
from ...models.workload_request_decision_schema import WorkloadRequestDecisionSchema


def _get_kwargs(
    *,
    body: WorkloadRequestDecisionCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/workload_request_decision/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, WorkloadRequestDecisionSchema]]:
    if response.status_code == 200:
        response_200 = WorkloadRequestDecisionSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, WorkloadRequestDecisionSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkloadRequestDecisionCreate,
) -> Response[Union[HTTPValidationError, WorkloadRequestDecisionSchema]]:
    """Create Workload Request Decision Route

     Create a new WorkloadRequestDecision entry.

    Args:
        data (WorkloadRequestDecisionSchema): The pod decision data to create.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadRequestDecisionSchema: The newly created pod decision.

    Args:
        body (WorkloadRequestDecisionCreate): Schema for creating a workload decision.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, WorkloadRequestDecisionSchema]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkloadRequestDecisionCreate,
) -> Optional[Union[HTTPValidationError, WorkloadRequestDecisionSchema]]:
    """Create Workload Request Decision Route

     Create a new WorkloadRequestDecision entry.

    Args:
        data (WorkloadRequestDecisionSchema): The pod decision data to create.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadRequestDecisionSchema: The newly created pod decision.

    Args:
        body (WorkloadRequestDecisionCreate): Schema for creating a workload decision.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, WorkloadRequestDecisionSchema]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkloadRequestDecisionCreate,
) -> Response[Union[HTTPValidationError, WorkloadRequestDecisionSchema]]:
    """Create Workload Request Decision Route

     Create a new WorkloadRequestDecision entry.

    Args:
        data (WorkloadRequestDecisionSchema): The pod decision data to create.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadRequestDecisionSchema: The newly created pod decision.

    Args:
        body (WorkloadRequestDecisionCreate): Schema for creating a workload decision.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, WorkloadRequestDecisionSchema]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkloadRequestDecisionCreate,
) -> Optional[Union[HTTPValidationError, WorkloadRequestDecisionSchema]]:
    """Create Workload Request Decision Route

     Create a new WorkloadRequestDecision entry.

    Args:
        data (WorkloadRequestDecisionSchema): The pod decision data to create.
        db_session (AsyncSession): Database session dependency.

    Returns:
        WorkloadRequestDecisionSchema: The newly created pod decision.

    Args:
        body (WorkloadRequestDecisionCreate): Schema for creating a workload decision.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, WorkloadRequestDecisionSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
