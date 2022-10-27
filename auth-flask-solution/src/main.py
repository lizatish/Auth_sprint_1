import aioredis
from flask_jwt_extended import JWTManager

from core.app_factory import create_app
from core.settings import get_settings
from db import redis

settings = get_settings()
app = create_app(settings)

jwt = JWTManager(app)
redis.cache = aioredis.from_url(
    f"redis://{app.config['CACHE_HOST']}:{app.config['CACHE_PORT']}",
    encoding="utf-8",
    decode_responses=True,
)

if __name__ == '__main__':
    app.run(port=5100)
