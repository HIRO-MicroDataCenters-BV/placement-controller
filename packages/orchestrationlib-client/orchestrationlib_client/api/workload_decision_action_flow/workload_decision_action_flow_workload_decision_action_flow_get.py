from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.workload_action_type_enum import WorkloadActionTypeEnum
from ...models.workload_decision_action_flow_item import WorkloadDecisionActionFlowItem
from ...types import Unset
from uuid import UUID


def _get_kwargs(
    *,
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
    decision_id: Union[None, UUID, Unset] = UNSET,
    action_id: Union[None, UUID, Unset] = UNSET,
    pod_name: Union[None, Unset, str] = UNSET,
    namespace: Union[None, Unset, str] = UNSET,
    node_name: Union[None, Unset, str] = UNSET,
    action_type: Union[None, Unset, WorkloadActionTypeEnum] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["skip"] = skip

    params["limit"] = limit

    json_decision_id: Union[None, Unset, str]
    if isinstance(decision_id, Unset):
        json_decision_id = UNSET
    elif isinstance(decision_id, UUID):
        json_decision_id = str(decision_id)
    else:
        json_decision_id = decision_id
    params["decision_id"] = json_decision_id

    json_action_id: Union[None, Unset, str]
    if isinstance(action_id, Unset):
        json_action_id = UNSET
    elif isinstance(action_id, UUID):
        json_action_id = str(action_id)
    else:
        json_action_id = action_id
    params["action_id"] = json_action_id

    json_pod_name: Union[None, Unset, str]
    if isinstance(pod_name, Unset):
        json_pod_name = UNSET
    else:
        json_pod_name = pod_name
    params["pod_name"] = json_pod_name

    json_namespace: Union[None, Unset, str]
    if isinstance(namespace, Unset):
        json_namespace = UNSET
    else:
        json_namespace = namespace
    params["namespace"] = json_namespace

    json_node_name: Union[None, Unset, str]
    if isinstance(node_name, Unset):
        json_node_name = UNSET
    else:
        json_node_name = node_name
    params["node_name"] = json_node_name

    json_action_type: Union[None, Unset, str]
    if isinstance(action_type, Unset):
        json_action_type = UNSET
    elif isinstance(action_type, WorkloadActionTypeEnum):
        json_action_type = action_type.value
    else:
        json_action_type = action_type
    params["action_type"] = json_action_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/workload_decision_action_flow/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["WorkloadDecisionActionFlowItem"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = WorkloadDecisionActionFlowItem.from_dict(
                response_200_item_data
            )

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
) -> Response[Union[HTTPValidationError, list["WorkloadDecisionActionFlowItem"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
    decision_id: Union[None, UUID, Unset] = UNSET,
    action_id: Union[None, UUID, Unset] = UNSET,
    pod_name: Union[None, Unset, str] = UNSET,
    namespace: Union[None, Unset, str] = UNSET,
    node_name: Union[None, Unset, str] = UNSET,
    action_type: Union[None, Unset, WorkloadActionTypeEnum] = UNSET,
) -> Response[Union[HTTPValidationError, list["WorkloadDecisionActionFlowItem"]]]:
    """Workload Decision Action Flow

     Get list of workload decision and action flows with pagination.
    Args:
        decision_id (UUID, optional): Filter by decision ID.
        action_id (UUID, optional): Filter by action ID.
        pod_name (str, optional): Filter by pod name.
        namespace (str, optional): Filter by namespace.
        node_name (str, optional): Filter by node name.
        action_type (WorkloadActionTypeEnum, optional): Filter by action type.
        skip (int): Number of records to skip (default: 0)
        limit (int): Maximum number of records to return (default: 100)
        db (AsyncSession, optional): Database session dependency.
            Defaults to Depends(get_async_db).
    Returns:
        List[WorkloadDecisionActionFlow]
            A sequence of dictionaries containing the WorkloadDecisionActionFlow details.
    Raises:
        DatabaseConnectionException: If there is an error connecting to the database.

    Args:
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        decision_id (Union[None, UUID, Unset]):
        action_id (Union[None, UUID, Unset]):
        pod_name (Union[None, Unset, str]):
        namespace (Union[None, Unset, str]):
        node_name (Union[None, Unset, str]):
        action_type (Union[None, Unset, WorkloadActionTypeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['WorkloadDecisionActionFlowItem']]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        limit=limit,
        decision_id=decision_id,
        action_id=action_id,
        pod_name=pod_name,
        namespace=namespace,
        node_name=node_name,
        action_type=action_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
    decision_id: Union[None, UUID, Unset] = UNSET,
    action_id: Union[None, UUID, Unset] = UNSET,
    pod_name: Union[None, Unset, str] = UNSET,
    namespace: Union[None, Unset, str] = UNSET,
    node_name: Union[None, Unset, str] = UNSET,
    action_type: Union[None, Unset, WorkloadActionTypeEnum] = UNSET,
) -> Optional[Union[HTTPValidationError, list["WorkloadDecisionActionFlowItem"]]]:
    """Workload Decision Action Flow

     Get list of workload decision and action flows with pagination.
    Args:
        decision_id (UUID, optional): Filter by decision ID.
        action_id (UUID, optional): Filter by action ID.
        pod_name (str, optional): Filter by pod name.
        namespace (str, optional): Filter by namespace.
        node_name (str, optional): Filter by node name.
        action_type (WorkloadActionTypeEnum, optional): Filter by action type.
        skip (int): Number of records to skip (default: 0)
        limit (int): Maximum number of records to return (default: 100)
        db (AsyncSession, optional): Database session dependency.
            Defaults to Depends(get_async_db).
    Returns:
        List[WorkloadDecisionActionFlow]
            A sequence of dictionaries containing the WorkloadDecisionActionFlow details.
    Raises:
        DatabaseConnectionException: If there is an error connecting to the database.

    Args:
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        decision_id (Union[None, UUID, Unset]):
        action_id (Union[None, UUID, Unset]):
        pod_name (Union[None, Unset, str]):
        namespace (Union[None, Unset, str]):
        node_name (Union[None, Unset, str]):
        action_type (Union[None, Unset, WorkloadActionTypeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['WorkloadDecisionActionFlowItem']]
    """

    return sync_detailed(
        client=client,
        skip=skip,
        limit=limit,
        decision_id=decision_id,
        action_id=action_id,
        pod_name=pod_name,
        namespace=namespace,
        node_name=node_name,
        action_type=action_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
    decision_id: Union[None, UUID, Unset] = UNSET,
    action_id: Union[None, UUID, Unset] = UNSET,
    pod_name: Union[None, Unset, str] = UNSET,
    namespace: Union[None, Unset, str] = UNSET,
    node_name: Union[None, Unset, str] = UNSET,
    action_type: Union[None, Unset, WorkloadActionTypeEnum] = UNSET,
) -> Response[Union[HTTPValidationError, list["WorkloadDecisionActionFlowItem"]]]:
    """Workload Decision Action Flow

     Get list of workload decision and action flows with pagination.
    Args:
        decision_id (UUID, optional): Filter by decision ID.
        action_id (UUID, optional): Filter by action ID.
        pod_name (str, optional): Filter by pod name.
        namespace (str, optional): Filter by namespace.
        node_name (str, optional): Filter by node name.
        action_type (WorkloadActionTypeEnum, optional): Filter by action type.
        skip (int): Number of records to skip (default: 0)
        limit (int): Maximum number of records to return (default: 100)
        db (AsyncSession, optional): Database session dependency.
            Defaults to Depends(get_async_db).
    Returns:
        List[WorkloadDecisionActionFlow]
            A sequence of dictionaries containing the WorkloadDecisionActionFlow details.
    Raises:
        DatabaseConnectionException: If there is an error connecting to the database.

    Args:
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        decision_id (Union[None, UUID, Unset]):
        action_id (Union[None, UUID, Unset]):
        pod_name (Union[None, Unset, str]):
        namespace (Union[None, Unset, str]):
        node_name (Union[None, Unset, str]):
        action_type (Union[None, Unset, WorkloadActionTypeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['WorkloadDecisionActionFlowItem']]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        limit=limit,
        decision_id=decision_id,
        action_id=action_id,
        pod_name=pod_name,
        namespace=namespace,
        node_name=node_name,
        action_type=action_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
    decision_id: Union[None, UUID, Unset] = UNSET,
    action_id: Union[None, UUID, Unset] = UNSET,
    pod_name: Union[None, Unset, str] = UNSET,
    namespace: Union[None, Unset, str] = UNSET,
    node_name: Union[None, Unset, str] = UNSET,
    action_type: Union[None, Unset, WorkloadActionTypeEnum] = UNSET,
) -> Optional[Union[HTTPValidationError, list["WorkloadDecisionActionFlowItem"]]]:
    """Workload Decision Action Flow

     Get list of workload decision and action flows with pagination.
    Args:
        decision_id (UUID, optional): Filter by decision ID.
        action_id (UUID, optional): Filter by action ID.
        pod_name (str, optional): Filter by pod name.
        namespace (str, optional): Filter by namespace.
        node_name (str, optional): Filter by node name.
        action_type (WorkloadActionTypeEnum, optional): Filter by action type.
        skip (int): Number of records to skip (default: 0)
        limit (int): Maximum number of records to return (default: 100)
        db (AsyncSession, optional): Database session dependency.
            Defaults to Depends(get_async_db).
    Returns:
        List[WorkloadDecisionActionFlow]
            A sequence of dictionaries containing the WorkloadDecisionActionFlow details.
    Raises:
        DatabaseConnectionException: If there is an error connecting to the database.

    Args:
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        decision_id (Union[None, UUID, Unset]):
        action_id (Union[None, UUID, Unset]):
        pod_name (Union[None, Unset, str]):
        namespace (Union[None, Unset, str]):
        node_name (Union[None, Unset, str]):
        action_type (Union[None, Unset, WorkloadActionTypeEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['WorkloadDecisionActionFlowItem']]
    """

    return (
        await asyncio_detailed(
            client=client,
            skip=skip,
            limit=limit,
            decision_id=decision_id,
            action_id=action_id,
            pod_name=pod_name,
            namespace=namespace,
            node_name=node_name,
            action_type=action_type,
        )
    ).parsed
