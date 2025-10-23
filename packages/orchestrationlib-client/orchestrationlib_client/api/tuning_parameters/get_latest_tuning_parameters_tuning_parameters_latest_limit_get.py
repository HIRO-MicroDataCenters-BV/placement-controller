from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.tuning_parameter_response import TuningParameterResponse


def _get_kwargs(
    limit: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/tuning_parameters/latest/{limit}".format(
            limit=limit,
        ),
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
    limit: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, list["TuningParameterResponse"]]]:
    """Get Latest Tuning Parameters

     Get the latest N tuning parameters based on creation time.

    Args:
        limit (int): Number of latest parameters to return
        db (AsyncSession): Database session dependency

    Returns:
        List[TuningParameterResponse]: List of the N most recent tuning parameters

    Raises:
        DatabaseConnectionException: If there's a database error

    Args:
        limit (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['TuningParameterResponse']]]
    """

    kwargs = _get_kwargs(
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    limit: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, list["TuningParameterResponse"]]]:
    """Get Latest Tuning Parameters

     Get the latest N tuning parameters based on creation time.

    Args:
        limit (int): Number of latest parameters to return
        db (AsyncSession): Database session dependency

    Returns:
        List[TuningParameterResponse]: List of the N most recent tuning parameters

    Raises:
        DatabaseConnectionException: If there's a database error

    Args:
        limit (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['TuningParameterResponse']]
    """

    return sync_detailed(
        limit=limit,
        client=client,
    ).parsed


async def asyncio_detailed(
    limit: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, list["TuningParameterResponse"]]]:
    """Get Latest Tuning Parameters

     Get the latest N tuning parameters based on creation time.

    Args:
        limit (int): Number of latest parameters to return
        db (AsyncSession): Database session dependency

    Returns:
        List[TuningParameterResponse]: List of the N most recent tuning parameters

    Raises:
        DatabaseConnectionException: If there's a database error

    Args:
        limit (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['TuningParameterResponse']]]
    """

    kwargs = _get_kwargs(
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    limit: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, list["TuningParameterResponse"]]]:
    """Get Latest Tuning Parameters

     Get the latest N tuning parameters based on creation time.

    Args:
        limit (int): Number of latest parameters to return
        db (AsyncSession): Database session dependency

    Returns:
        List[TuningParameterResponse]: List of the N most recent tuning parameters

    Raises:
        DatabaseConnectionException: If there's a database error

    Args:
        limit (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['TuningParameterResponse']]
    """

    return (
        await asyncio_detailed(
            limit=limit,
            client=client,
        )
    ).parsed
