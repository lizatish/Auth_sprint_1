import aioredis
from redis import Redis

from core.app_factory import create_app
from core.settings import get_settings
from db import redis

settings = get_settings()
app = create_app(settings)

# todo переписать под асинхронный редис
# redis.cache = aioredis.from_url(
#     f"redis://{app.config['CACHE_HOST']}:{app.config['CACHE_PORT']}",
#     encoding="utf-8",
#     decode_responses=True,
# )
redis.cache =Redis(
        host=app.config['CACHE_HOST'],
        port=app.config['CACHE_PORT'],
    )

if __name__ == '__main__':
    app.run(port=5100)
