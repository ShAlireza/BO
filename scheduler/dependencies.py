from .internal import cron_handler


async def get_cron_handler():
    return cron_handler
