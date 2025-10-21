from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.pod_parent_type_enum import PodParentTypeEnum
from ...models.workload_action import WorkloadAction
from ...models.workload_action_status_enum import WorkloadActionStatusEnum
from ...models.workload_action_type_enum import WorkloadActionTypeEnum
from ...types import Unset
from uuid import UUID
import datetime


def _get_kwargs(
    *,
    created_pod_name: Union[None, Unset, str] = UNSET,
    created_pod_namespace: Union[None, Unset, str] = UNSET,
    created_node_name: Union[None, Unset, str] = UNSET,
    deleted_pod_name: Union[None, Unset, str] = UNSET,
    deleted_pod_namespace: Union[None, Unset, str] = UNSET,
    deleted_node_name: Union[None, Unset, str] = UNSET,
    bound_pod_name: Union[None, Unset, str] = UNSET,
    bound_pod_namespace: Union[None, Unset, str] = UNSET,
    bound_node_name: Union[None, Unset, str] = UNSET,
    action_type: Union[None, Unset, WorkloadActionTypeEnum] = UNSET,
    action_status: Union[None, Unset, WorkloadActionStatusEnum] = UNSET,
    action_start_time: Union[None, Unset, datetime.datetime] = UNSET,
    action_end_time: Union[None, Unset, datetime.datetime] = UNSET,
    action_reason: Union[None, Unset, str] = UNSET,
    pod_parent_name: Union[None, Unset, str] = UNSET,
    pod_parent_type: Union[None, PodParentTypeEnum, Unset] = UNSET,
    pod_parent_uid: Union[None, UUID, Unset] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created_pod_name: Union[None, Unset, str]
    if isinstance(created_pod_name, Unset):
        json_created_pod_name = UNSET
    else:
        json_created_pod_name = created_pod_name
    params["created_pod_name"] = json_created_pod_name

    json_created_pod_namespace: Union[None, Unset, str]
    if isinstance(created_pod_namespace, Unset):
        json_created_pod_namespace = UNSET
    else:
        json_created_pod_namespace = created_pod_namespace
    params["created_pod_namespace"] = json_created_pod_namespace

    json_created_node_name: Union[None, Unset, str]
    if isinstance(created_node_name, Unset):
        json_created_node_name = UNSET
    else:
        json_created_node_name = created_node_name
    params["created_node_name"] = json_created_node_name

    json_deleted_pod_name: Union[None, Unset, str]
    if isinstance(deleted_pod_name, Unset):
        json_deleted_pod_name = UNSET
    else:
        json_deleted_pod_name = deleted_pod_name
    params["deleted_pod_name"] = json_deleted_pod_name

    json_deleted_pod_namespace: Union[None, Unset, str]
    if isinstance(deleted_pod_namespace, Unset):
        json_deleted_pod_namespace = UNSET
    else:
        json_deleted_pod_namespace = deleted_pod_namespace
    params["deleted_pod_namespace"] = json_deleted_pod_namespace

    json_deleted_node_name: Union[None, Unset, str]
    if isinstance(deleted_node_name, Unset):
        json_deleted_node_name = UNSET
    else:
        json_deleted_node_name = deleted_node_name
    params["deleted_node_name"] = json_deleted_node_name

    json_bound_pod_name: Union[None, Unset, str]
    if isinstance(bound_pod_name, Unset):
        json_bound_pod_name = UNSET
    else:
        json_bound_pod_name = bound_pod_name
    params["bound_pod_name"] = json_bound_pod_name

    json_bound_pod_namespace: Union[None, Unset, str]
    if isinstance(bound_pod_namespace, Unset):
        json_bound_pod_namespace = UNSET
    else:
        json_bound_pod_namespace = bound_pod_namespace
    params["bound_pod_namespace"] = json_bound_pod_namespace

    json_bound_node_name: Union[None, Unset, str]
    if isinstance(bound_node_name, Unset):
        json_bound_node_name = UNSET
    else:
        json_bound_node_name = bound_node_name
    params["bound_node_name"] = json_bound_node_name

    json_action_type: Union[None, Unset, str]
    if isinstance(action_type, Unset):
        json_action_type = UNSET
    elif isinstance(action_type, WorkloadActionTypeEnum):
        json_action_type = action_type.value
    else:
        json_action_type = action_type
    params["action_type"] = json_action_type

    json_action_status: Union[None, Unset, str]
    if isinstance(action_status, Unset):
        json_action_status = UNSET
    elif isinstance(action_status, WorkloadActionStatusEnum):
        json_action_status = action_status.value
    else:
        json_action_status = action_status
    params["action_status"] = json_action_status

    json_action_start_time: Union[None, Unset, str]
    if isinstance(action_start_time, Unset):
        json_action_start_time = UNSET
    elif isinstance(action_start_time, datetime.datetime):
        json_action_start_time = action_start_time.isoformat()
    else:
        json_action_start_time = action_start_time
    params["action_start_time"] = json_action_start_time

    json_action_end_time: Union[None, Unset, str]
    if isinstance(action_end_time, Unset):
        json_action_end_time = UNSET
    elif isinstance(action_end_time, datetime.datetime):
        json_action_end_time = action_end_time.isoformat()
    else:
        json_action_end_time = action_end_time
    params["action_end_time"] = json_action_end_time

    json_action_reason: Union[None, Unset, str]
    if isinstance(action_reason, Unset):
        json_action_reason = UNSET
    else:
        json_action_reason = action_reason
    params["action_reason"] = json_action_reason

    json_pod_parent_name: Union[None, Unset, str]
    if isinstance(pod_parent_name, Unset):
        json_pod_parent_name = UNSET
    else:
        json_pod_parent_name = pod_parent_name
    params["pod_parent_name"] = json_pod_parent_name

    json_pod_parent_type: Union[None, Unset, str]
    if isinstance(pod_parent_type, Unset):
        json_pod_parent_type = UNSET
    elif isinstance(pod_parent_type, PodParentTypeEnum):
        json_pod_parent_type = pod_parent_type.value
    else:
        json_pod_parent_type = pod_parent_type
    params["pod_parent_type"] = json_pod_parent_type

    json_pod_parent_uid: Union[None, Unset, str]
    if isinstance(pod_parent_uid, Unset):
        json_pod_parent_uid = UNSET
    elif isinstance(pod_parent_uid, UUID):
        json_pod_parent_uid = str(pod_parent_uid)
    else:
        json_pod_parent_uid = pod_parent_uid
    params["pod_parent_uid"] = json_pod_parent_uid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/workload_action/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["WorkloadAction"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = WorkloadAction.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[HTTPValidationError, list["WorkloadAction"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    created_pod_name: Union[None, Unset, str] = UNSET,
    created_pod_namespace: Union[None, Unset, str] = UNSET,
    created_node_name: Union[None, Unset, str] = UNSET,
    deleted_pod_name: Union[None, Unset, str] = UNSET,
    deleted_pod_namespace: Union[None, Unset, str] = UNSET,
    deleted_node_name: Union[None, Unset, str] = UNSET,
    bound_pod_name: Union[None, Unset, str] = UNSET,
    bound_pod_namespace: Union[None, Unset, str] = UNSET,
    bound_node_name: Union[None, Unset, str] = UNSET,
    action_type: Union[None, Unset, WorkloadActionTypeEnum] = UNSET,
    action_status: Union[None, Unset, WorkloadActionStatusEnum] = UNSET,
    action_start_time: Union[None, Unset, datetime.datetime] = UNSET,
    action_end_time: Union[None, Unset, datetime.datetime] = UNSET,
    action_reason: Union[None, Unset, str] = UNSET,
    pod_parent_name: Union[None, Unset, str] = UNSET,
    pod_parent_type: Union[None, PodParentTypeEnum, Unset] = UNSET,
    pod_parent_uid: Union[None, UUID, Unset] = UNSET,
) -> Response[Union[HTTPValidationError, list["WorkloadAction"]]]:
    """Get All Workload Actions Route

     Retrieve all workload actions with optional filters.

    Args:
        db_session (AsyncSession): Database session dependency.
        filters (WorkloadActionFilters): Filters to apply to the workload actions.

    Returns:
        list[WorkloadAction]: List of workload actions matching the filters.

    Args:
        created_pod_name (Union[None, Unset, str]):
        created_pod_namespace (Union[None, Unset, str]):
        created_node_name (Union[None, Unset, str]):
        deleted_pod_name (Union[None, Unset, str]):
        deleted_pod_namespace (Union[None, Unset, str]):
        deleted_node_name (Union[None, Unset, str]):
        bound_pod_name (Union[None, Unset, str]):
        bound_pod_namespace (Union[None, Unset, str]):
        bound_node_name (Union[None, Unset, str]):
        action_type (Union[None, Unset, WorkloadActionTypeEnum]):
        action_status (Union[None, Unset, WorkloadActionStatusEnum]):
        action_start_time (Union[None, Unset, datetime.datetime]):
        action_end_time (Union[None, Unset, datetime.datetime]):
        action_reason (Union[None, Unset, str]):
        pod_parent_name (Union[None, Unset, str]):
        pod_parent_type (Union[None, PodParentTypeEnum, Unset]):
        pod_parent_uid (Union[None, UUID, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['WorkloadAction']]]
    """

    kwargs = _get_kwargs(
        created_pod_name=created_pod_name,
        created_pod_namespace=created_pod_namespace,
        created_node_name=created_node_name,
        deleted_pod_name=deleted_pod_name,
        deleted_pod_namespace=deleted_pod_namespace,
        deleted_node_name=deleted_node_name,
        bound_pod_name=bound_pod_name,
        bound_pod_namespace=bound_pod_namespace,
        bound_node_name=bound_node_name,
        action_type=action_type,
        action_status=action_status,
        action_start_time=action_start_time,
        action_end_time=action_end_time,
        action_reason=action_reason,
        pod_parent_name=pod_parent_name,
        pod_parent_type=pod_parent_type,
        pod_parent_uid=pod_parent_uid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    created_pod_name: Union[None, Unset, str] = UNSET,
    created_pod_namespace: Union[None, Unset, str] = UNSET,
    created_node_name: Union[None, Unset, str] = UNSET,
    deleted_pod_name: Union[None, Unset, str] = UNSET,
    deleted_pod_namespace: Union[None, Unset, str] = UNSET,
    deleted_node_name: Union[None, Unset, str] = UNSET,
    bound_pod_name: Union[None, Unset, str] = UNSET,
    bound_pod_namespace: Union[None, Unset, str] = UNSET,
    bound_node_name: Union[None, Unset, str] = UNSET,
    action_type: Union[None, Unset, WorkloadActionTypeEnum] = UNSET,
    action_status: Union[None, Unset, WorkloadActionStatusEnum] = UNSET,
    action_start_time: Union[None, Unset, datetime.datetime] = UNSET,
    action_end_time: Union[None, Unset, datetime.datetime] = UNSET,
    action_reason: Union[None, Unset, str] = UNSET,
    pod_parent_name: Union[None, Unset, str] = UNSET,
    pod_parent_type: Union[None, PodParentTypeEnum, Unset] = UNSET,
    pod_parent_uid: Union[None, UUID, Unset] = UNSET,
) -> Optional[Union[HTTPValidationError, list["WorkloadAction"]]]:
    """Get All Workload Actions Route

     Retrieve all workload actions with optional filters.

    Args:
        db_session (AsyncSession): Database session dependency.
        filters (WorkloadActionFilters): Filters to apply to the workload actions.

    Returns:
        list[WorkloadAction]: List of workload actions matching the filters.

    Args:
        created_pod_name (Union[None, Unset, str]):
        created_pod_namespace (Union[None, Unset, str]):
        created_node_name (Union[None, Unset, str]):
        deleted_pod_name (Union[None, Unset, str]):
        deleted_pod_namespace (Union[None, Unset, str]):
        deleted_node_name (Union[None, Unset, str]):
        bound_pod_name (Union[None, Unset, str]):
        bound_pod_namespace (Union[None, Unset, str]):
        bound_node_name (Union[None, Unset, str]):
        action_type (Union[None, Unset, WorkloadActionTypeEnum]):
        action_status (Union[None, Unset, WorkloadActionStatusEnum]):
        action_start_time (Union[None, Unset, datetime.datetime]):
        action_end_time (Union[None, Unset, datetime.datetime]):
        action_reason (Union[None, Unset, str]):
        pod_parent_name (Union[None, Unset, str]):
        pod_parent_type (Union[None, PodParentTypeEnum, Unset]):
        pod_parent_uid (Union[None, UUID, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['WorkloadAction']]
    """

    return sync_detailed(
        client=client,
        created_pod_name=created_pod_name,
        created_pod_namespace=created_pod_namespace,
        created_node_name=created_node_name,
        deleted_pod_name=deleted_pod_name,
        deleted_pod_namespace=deleted_pod_namespace,
        deleted_node_name=deleted_node_name,
        bound_pod_name=bound_pod_name,
        bound_pod_namespace=bound_pod_namespace,
        bound_node_name=bound_node_name,
        action_type=action_type,
        action_status=action_status,
        action_start_time=action_start_time,
        action_end_time=action_end_time,
        action_reason=action_reason,
        pod_parent_name=pod_parent_name,
        pod_parent_type=pod_parent_type,
        pod_parent_uid=pod_parent_uid,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    created_pod_name: Union[None, Unset, str] = UNSET,
    created_pod_namespace: Union[None, Unset, str] = UNSET,
    created_node_name: Union[None, Unset, str] = UNSET,
    deleted_pod_name: Union[None, Unset, str] = UNSET,
    deleted_pod_namespace: Union[None, Unset, str] = UNSET,
    deleted_node_name: Union[None, Unset, str] = UNSET,
    bound_pod_name: Union[None, Unset, str] = UNSET,
    bound_pod_namespace: Union[None, Unset, str] = UNSET,
    bound_node_name: Union[None, Unset, str] = UNSET,
    action_type: Union[None, Unset, WorkloadActionTypeEnum] = UNSET,
    action_status: Union[None, Unset, WorkloadActionStatusEnum] = UNSET,
    action_start_time: Union[None, Unset, datetime.datetime] = UNSET,
    action_end_time: Union[None, Unset, datetime.datetime] = UNSET,
    action_reason: Union[None, Unset, str] = UNSET,
    pod_parent_name: Union[None, Unset, str] = UNSET,
    pod_parent_type: Union[None, PodParentTypeEnum, Unset] = UNSET,
    pod_parent_uid: Union[None, UUID, Unset] = UNSET,
) -> Response[Union[HTTPValidationError, list["WorkloadAction"]]]:
    """Get All Workload Actions Route

     Retrieve all workload actions with optional filters.

    Args:
        db_session (AsyncSession): Database session dependency.
        filters (WorkloadActionFilters): Filters to apply to the workload actions.

    Returns:
        list[WorkloadAction]: List of workload actions matching the filters.

    Args:
        created_pod_name (Union[None, Unset, str]):
        created_pod_namespace (Union[None, Unset, str]):
        created_node_name (Union[None, Unset, str]):
        deleted_pod_name (Union[None, Unset, str]):
        deleted_pod_namespace (Union[None, Unset, str]):
        deleted_node_name (Union[None, Unset, str]):
        bound_pod_name (Union[None, Unset, str]):
        bound_pod_namespace (Union[None, Unset, str]):
        bound_node_name (Union[None, Unset, str]):
        action_type (Union[None, Unset, WorkloadActionTypeEnum]):
        action_status (Union[None, Unset, WorkloadActionStatusEnum]):
        action_start_time (Union[None, Unset, datetime.datetime]):
        action_end_time (Union[None, Unset, datetime.datetime]):
        action_reason (Union[None, Unset, str]):
        pod_parent_name (Union[None, Unset, str]):
        pod_parent_type (Union[None, PodParentTypeEnum, Unset]):
        pod_parent_uid (Union[None, UUID, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['WorkloadAction']]]
    """

    kwargs = _get_kwargs(
        created_pod_name=created_pod_name,
        created_pod_namespace=created_pod_namespace,
        created_node_name=created_node_name,
        deleted_pod_name=deleted_pod_name,
        deleted_pod_namespace=deleted_pod_namespace,
        deleted_node_name=deleted_node_name,
        bound_pod_name=bound_pod_name,
        bound_pod_namespace=bound_pod_namespace,
        bound_node_name=bound_node_name,
        action_type=action_type,
        action_status=action_status,
        action_start_time=action_start_time,
        action_end_time=action_end_time,
        action_reason=action_reason,
        pod_parent_name=pod_parent_name,
        pod_parent_type=pod_parent_type,
        pod_parent_uid=pod_parent_uid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    created_pod_name: Union[None, Unset, str] = UNSET,
    created_pod_namespace: Union[None, Unset, str] = UNSET,
    created_node_name: Union[None, Unset, str] = UNSET,
    deleted_pod_name: Union[None, Unset, str] = UNSET,
    deleted_pod_namespace: Union[None, Unset, str] = UNSET,
    deleted_node_name: Union[None, Unset, str] = UNSET,
    bound_pod_name: Union[None, Unset, str] = UNSET,
    bound_pod_namespace: Union[None, Unset, str] = UNSET,
    bound_node_name: Union[None, Unset, str] = UNSET,
    action_type: Union[None, Unset, WorkloadActionTypeEnum] = UNSET,
    action_status: Union[None, Unset, WorkloadActionStatusEnum] = UNSET,
    action_start_time: Union[None, Unset, datetime.datetime] = UNSET,
    action_end_time: Union[None, Unset, datetime.datetime] = UNSET,
    action_reason: Union[None, Unset, str] = UNSET,
    pod_parent_name: Union[None, Unset, str] = UNSET,
    pod_parent_type: Union[None, PodParentTypeEnum, Unset] = UNSET,
    pod_parent_uid: Union[None, UUID, Unset] = UNSET,
) -> Optional[Union[HTTPValidationError, list["WorkloadAction"]]]:
    """Get All Workload Actions Route

     Retrieve all workload actions with optional filters.

    Args:
        db_session (AsyncSession): Database session dependency.
        filters (WorkloadActionFilters): Filters to apply to the workload actions.

    Returns:
        list[WorkloadAction]: List of workload actions matching the filters.

    Args:
        created_pod_name (Union[None, Unset, str]):
        created_pod_namespace (Union[None, Unset, str]):
        created_node_name (Union[None, Unset, str]):
        deleted_pod_name (Union[None, Unset, str]):
        deleted_pod_namespace (Union[None, Unset, str]):
        deleted_node_name (Union[None, Unset, str]):
        bound_pod_name (Union[None, Unset, str]):
        bound_pod_namespace (Union[None, Unset, str]):
        bound_node_name (Union[None, Unset, str]):
        action_type (Union[None, Unset, WorkloadActionTypeEnum]):
        action_status (Union[None, Unset, WorkloadActionStatusEnum]):
        action_start_time (Union[None, Unset, datetime.datetime]):
        action_end_time (Union[None, Unset, datetime.datetime]):
        action_reason (Union[None, Unset, str]):
        pod_parent_name (Union[None, Unset, str]):
        pod_parent_type (Union[None, PodParentTypeEnum, Unset]):
        pod_parent_uid (Union[None, UUID, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['WorkloadAction']]
    """

    return (
        await asyncio_detailed(
            client=client,
            created_pod_name=created_pod_name,
            created_pod_namespace=created_pod_namespace,
            created_node_name=created_node_name,
            deleted_pod_name=deleted_pod_name,
            deleted_pod_namespace=deleted_pod_namespace,
            deleted_node_name=deleted_node_name,
            bound_pod_name=bound_pod_name,
            bound_pod_namespace=bound_pod_namespace,
            bound_node_name=bound_node_name,
            action_type=action_type,
            action_status=action_status,
            action_start_time=action_start_time,
            action_end_time=action_end_time,
            action_reason=action_reason,
            pod_parent_name=pod_parent_name,
            pod_parent_type=pod_parent_type,
            pod_parent_uid=pod_parent_uid,
        )
    ).parsed
