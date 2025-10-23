from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.tuning_parameter_create import TuningParameterCreate
from ...models.tuning_parameter_response import TuningParameterResponse


def _get_kwargs(
    *,
    body: TuningParameterCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/tuning_parameters/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, TuningParameterResponse]]:
    if response.status_code == 200:
        response_200 = TuningParameterResponse.from_dict(response.json())

        return response_200

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, HTTPValidationError, TuningParameterResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TuningParameterCreate,
) -> Response[Union[Any, HTTPValidationError, TuningParameterResponse]]:
    """Create Tuning Parameter

     Create a new tuning parameter.

    Args:
        tuning_parameter (TuningParameterCreate): The tuning parameter data to create
        db (AsyncSession): Database session dependency

    Returns:
        TuningParameterResponse: The created tuning parameter

    Raises:
        DatabaseConnectionException: If there's a database error

    Args:
        body (TuningParameterCreate): Schema for creating a tuning parameter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, TuningParameterResponse]]
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
    body: TuningParameterCreate,
) -> Optional[Union[Any, HTTPValidationError, TuningParameterResponse]]:
    """Create Tuning Parameter

     Create a new tuning parameter.

    Args:
        tuning_parameter (TuningParameterCreate): The tuning parameter data to create
        db (AsyncSession): Database session dependency

    Returns:
        TuningParameterResponse: The created tuning parameter

    Raises:
        DatabaseConnectionException: If there's a database error

    Args:
        body (TuningParameterCreate): Schema for creating a tuning parameter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, TuningParameterResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TuningParameterCreate,
) -> Response[Union[Any, HTTPValidationError, TuningParameterResponse]]:
    """Create Tuning Parameter

     Create a new tuning parameter.

    Args:
        tuning_parameter (TuningParameterCreate): The tuning parameter data to create
        db (AsyncSession): Database session dependency

    Returns:
        TuningParameterResponse: The created tuning parameter

    Raises:
        DatabaseConnectionException: If there's a database error

    Args:
        body (TuningParameterCreate): Schema for creating a tuning parameter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, TuningParameterResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: TuningParameterCreate,
) -> Optional[Union[Any, HTTPValidationError, TuningParameterResponse]]:
    """Create Tuning Parameter

     Create a new tuning parameter.

    Args:
        tuning_parameter (TuningParameterCreate): The tuning parameter data to create
        db (AsyncSession): Database session dependency

    Returns:
        TuningParameterResponse: The created tuning parameter

    Raises:
        DatabaseConnectionException: If there's a database error

    Args:
        body (TuningParameterCreate): Schema for creating a tuning parameter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, TuningParameterResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
