import asyncio
import logging

import aioredis

from tests.functional.settings import get_settings
from tests.functional.logger import get_logger
from tests.functional.utils.connection import backoff

conf = get_settings()
logger = get_logger()
backoff_logger = logging.getLogger(__name__)


@backoff(
    Exception,
    backoff_logger=logger,
)
async def connect_redis():
    """Ожидание подключения к redis"""
    redis_client = aioredis.from_url(
        f"redis://{conf.CACHE_HOST}:{conf.CACHE_PORT}", encoding="utf-8", decode_responses=True
    )
    logger.debug('Connection established!')
    await redis_client.close()


if __name__ == '__main__':
    asyncio.run(connect_redis())
