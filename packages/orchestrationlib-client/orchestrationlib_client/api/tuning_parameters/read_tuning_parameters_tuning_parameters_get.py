from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.tuning_parameter_response import TuningParameterResponse
from ...types import Unset
import datetime


def _get_kwargs(
    *,
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
    start_date: Union[None, Unset, datetime.datetime] = UNSET,
    end_date: Union[None, Unset, datetime.datetime] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["skip"] = skip

    params["limit"] = limit

    json_start_date: Union[None, Unset, str]
    if isinstance(start_date, Unset):
        json_start_date = UNSET
    elif isinstance(start_date, datetime.datetime):
        json_start_date = start_date.isoformat()
    else:
        json_start_date = start_date
    params["start_date"] = json_start_date

    json_end_date: Union[None, Unset, str]
    if isinstance(end_date, Unset):
        json_end_date = UNSET
    elif isinstance(end_date, datetime.datetime):
        json_end_date = end_date.isoformat()
    else:
        json_end_date = end_date
    params["end_date"] = json_end_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/tuning_parameters/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["TuningParameterResponse"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = TuningParameterResponse.from_dict(
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
) -> Response[Union[HTTPValidationError, list["TuningParameterResponse"]]]:
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
    start_date: Union[None, Unset, datetime.datetime] = UNSET,
    end_date: Union[None, Unset, datetime.datetime] = UNSET,
) -> Response[Union[HTTPValidationError, list["TuningParameterResponse"]]]:
    """Read Tuning Parameters

     Get a list of tuning parameters with pagination and date filtering.

    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 100)
        start_date: Filter records created after this date (optional)
        end_date: Filter records created before this date (optional)
        db (AsyncSession): Database session dependency

    Returns:
        List[TuningParameterResponse]: List of tuning parameters

    Raises:
        DatabaseConnectionException: If there's a database error

    Args:
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        start_date (Union[None, Unset, datetime.datetime]):
        end_date (Union[None, Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['TuningParameterResponse']]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
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
    start_date: Union[None, Unset, datetime.datetime] = UNSET,
    end_date: Union[None, Unset, datetime.datetime] = UNSET,
) -> Optional[Union[HTTPValidationError, list["TuningParameterResponse"]]]:
    """Read Tuning Parameters

     Get a list of tuning parameters with pagination and date filtering.

    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 100)
        start_date: Filter records created after this date (optional)
        end_date: Filter records created before this date (optional)
        db (AsyncSession): Database session dependency

    Returns:
        List[TuningParameterResponse]: List of tuning parameters

    Raises:
        DatabaseConnectionException: If there's a database error

    Args:
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        start_date (Union[None, Unset, datetime.datetime]):
        end_date (Union[None, Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['TuningParameterResponse']]
    """

    return sync_detailed(
        client=client,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
    start_date: Union[None, Unset, datetime.datetime] = UNSET,
    end_date: Union[None, Unset, datetime.datetime] = UNSET,
) -> Response[Union[HTTPValidationError, list["TuningParameterResponse"]]]:
    """Read Tuning Parameters

     Get a list of tuning parameters with pagination and date filtering.

    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 100)
        start_date: Filter records created after this date (optional)
        end_date: Filter records created before this date (optional)
        db (AsyncSession): Database session dependency

    Returns:
        List[TuningParameterResponse]: List of tuning parameters

    Raises:
        DatabaseConnectionException: If there's a database error

    Args:
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        start_date (Union[None, Unset, datetime.datetime]):
        end_date (Union[None, Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['TuningParameterResponse']]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
    start_date: Union[None, Unset, datetime.datetime] = UNSET,
    end_date: Union[None, Unset, datetime.datetime] = UNSET,
) -> Optional[Union[HTTPValidationError, list["TuningParameterResponse"]]]:
    """Read Tuning Parameters

     Get a list of tuning parameters with pagination and date filtering.

    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 100)
        start_date: Filter records created after this date (optional)
        end_date: Filter records created before this date (optional)
        db (AsyncSession): Database session dependency

    Returns:
        List[TuningParameterResponse]: List of tuning parameters

    Raises:
        DatabaseConnectionException: If there's a database error

    Args:
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        start_date (Union[None, Unset, datetime.datetime]):
        end_date (Union[None, Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['TuningParameterResponse']]
    """

    return (
        await asyncio_detailed(
            client=client,
            skip=skip,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
        )
    ).parsed
