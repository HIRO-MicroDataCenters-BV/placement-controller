from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.workload_timing_schema import WorkloadTimingSchema
from ...types import Unset


def _get_kwargs(
    *,
    pod_name: Union[None, Unset, str] = UNSET,
    namespace: Union[None, Unset, str] = UNSET,
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

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

    params["skip"] = skip

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/workload_timing/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["WorkloadTimingSchema"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = WorkloadTimingSchema.from_dict(response_200_item_data)

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
) -> Response[Union[HTTPValidationError, list["WorkloadTimingSchema"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    pod_name: Union[None, Unset, str] = UNSET,
    namespace: Union[None, Unset, str] = UNSET,
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, list["WorkloadTimingSchema"]]]:
    """List Or Filter Workload Timings

     If pod_name & namespace provided -> filter; else return paginated list.

    Args:
        pod_name (Union[None, Unset, str]):
        namespace (Union[None, Unset, str]):
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['WorkloadTimingSchema']]]
    """

    kwargs = _get_kwargs(
        pod_name=pod_name,
        namespace=namespace,
        skip=skip,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    pod_name: Union[None, Unset, str] = UNSET,
    namespace: Union[None, Unset, str] = UNSET,
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, list["WorkloadTimingSchema"]]]:
    """List Or Filter Workload Timings

     If pod_name & namespace provided -> filter; else return paginated list.

    Args:
        pod_name (Union[None, Unset, str]):
        namespace (Union[None, Unset, str]):
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['WorkloadTimingSchema']]
    """

    return sync_detailed(
        client=client,
        pod_name=pod_name,
        namespace=namespace,
        skip=skip,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    pod_name: Union[None, Unset, str] = UNSET,
    namespace: Union[None, Unset, str] = UNSET,
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, list["WorkloadTimingSchema"]]]:
    """List Or Filter Workload Timings

     If pod_name & namespace provided -> filter; else return paginated list.

    Args:
        pod_name (Union[None, Unset, str]):
        namespace (Union[None, Unset, str]):
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['WorkloadTimingSchema']]]
    """

    kwargs = _get_kwargs(
        pod_name=pod_name,
        namespace=namespace,
        skip=skip,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    pod_name: Union[None, Unset, str] = UNSET,
    namespace: Union[None, Unset, str] = UNSET,
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, list["WorkloadTimingSchema"]]]:
    """List Or Filter Workload Timings

     If pod_name & namespace provided -> filter; else return paginated list.

    Args:
        pod_name (Union[None, Unset, str]):
        namespace (Union[None, Unset, str]):
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['WorkloadTimingSchema']]
    """

    return (
        await asyncio_detailed(
            client=client,
            pod_name=pod_name,
            namespace=namespace,
            skip=skip,
            limit=limit,
        )
    ).parsed
