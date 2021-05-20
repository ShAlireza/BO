import requests
from http.cookies import SimpleCookie
from typing import Dict, List, Any, Optional, Union, Tuple

import aiohttp

from multidict import CIMultiDictProxy

from fastapi import FastAPI, Query, Body, Path, APIRouter, Response


def merge_dicts(
        source: Union[Dict[str, Any], CIMultiDictProxy, SimpleCookie],
        destination: Union[Dict[str, Any], CIMultiDictProxy, SimpleCookie]
) -> Dict[str, Any]:
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            merge_dicts(value, node)
        else:
            destination[key] = value

    return destination


async def request(
        method: str,
        url: str,
        params: Dict[str, Union[str, int, float]] = None,
        json: Dict[str, Any] = None,
        headers: Dict[str, Union[str, int, float]] = None,
        cookies: Dict[str, Union[str, int, float]] = None,
        response: Response = None
) -> Tuple[Dict[str, Any], int, CIMultiDictProxy, SimpleCookie]:
    params = {} if not params else params
    json = {} if not json else json
    headers = {} if not headers else headers
    cookies = {} if not cookies else cookies

    async with aiohttp.ClientSession() as session:
        async with session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=headers,
                cookies=cookies
        ) as aio_response:

            data = await aio_response.json()
            status_code = aio_response.status
            response_headers = aio_response.headers
            response_cookies = aio_response.cookies

    if response:
        response.status = status_code
        # May be set headers, cookies, etc. in future

    return data, status_code, response_headers, response_cookies


def generate_openapi_with_external_apis(
        app: FastAPI,
        urls: List[str]
) -> Dict[str, Any]:
    current_open_api = app.openapi()
    for url in urls:
        open_api = requests.get(url)
        if open_api.status_code == 200:
            current_open_api = merge_dicts(open_api.json(), current_open_api)

    return current_open_api


def generate_routes_from_openapi(
        router: Union[FastAPI, APIRouter],
        openapi: Dict[str, Any],
        url: str = None
) -> None:
    def extract_params(params: List[Dict[str, Any]], with_body=False):
        fastapi_params = []

        separated_params = {
            'path': [],  # path
            'query': [],  # params
            'header': [],  # headers
            'cookie': [],  # cookies
            'body': []  # json
        }

        param_types = {
            'string': 'str',
            'integer': 'int',
            'number': 'float'
        }

        param_positions = {
            'path': 'Path',
            'query': 'Query',
            'header': 'header',
            'cookie': 'cookie',
            'body': 'Body'
        }
        if params:
            for param in params:
                param_position = param_positions.get(param.get('in'))
                param_type = param_types.get(param.get('schema').get('type'))

                if param.get('required'):
                    fastapi_param = f'{param_position}(...)'
                else:
                    fastapi_param = f'{param_position}(None)'

                param_str = f"""
                {param.get('name')}: {param_type} = {fastapi_param}
                """
                fastapi_params.append(param_str)
                key_value = f"'{param.get('name')}': {param.get('name')}"
                separated_params[param.get('in')].append(key_value)

        if with_body:
            fastapi_params.append(
                'body: Dict[str, Any] = Body(...)'
            )
            separated_params['body'].append(f"'body': body")

        separated_params_str = f"""{{
        'path': {{{', '.join(separated_params.get('path'))}}},
        'query': {{{', '.join(separated_params.get('query'))}}},
        'header': {{{', '.join(separated_params.get('header'))}}},
        'cookie': {{{', '.join(separated_params.get('cookie'))}}},
        'body': {{{', '.join(separated_params.get('body'))}}},
        }}
        """
        return fastapi_params, separated_params_str

    for path, methods in openapi.get('paths').items():
        for method_name, method_data in methods.items():
            # print(method_data)
            fastapi_params, separated_params_str = extract_params(
                params=method_data.get('parameters'),
                with_body=method_name in ['post', 'put', 'patch']
            )

            route = f"""@router.api_route(path='{path}', methods=['{method_name}'])
async def {method_data.get('operationId')}({', '.join(fastapi_params)}):
    separated_params = {separated_params_str}
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method={method_name},
            url='{url}{path}'.format(**separated_params.get('path')),
            headers=separated_params.get('header'),
            params=separated_params.get('query'),
            cookies=separated_params.get('cookie'),
            json=separated_params.get('body')
        ) as response:
            data = await response.json()
    return data
            """
            exec(route)
            # eval(route)
            print(route)
