import aiohttp

from fastapi import Header, Depends


# Todo
#  1. Catch and log errors

async def get_namespace(
        namespace_server_url: str,
        token: str
):
    async with aiohttp.ClientSession() as session:
        async with session.get(namespace_server_url) as response:
            json = await response.json()
            return json.get('name')


async def namespace_token_header(
        namespace_token: str = Header(
            ...,
            title='namespace token'
        )
):
    return namespace_token


async def handle_namespace_token(
        namespace_token: str = Depends(namespace_token_header)
):
    from config import NAMESPACE_SERVER_URL

    namespace_name = await get_namespace(NAMESPACE_SERVER_URL, namespace_token)

    return namespace_name
