from app.redis.redis_client import get_redis_client

client = get_redis_client()
print(client.ping())   # should print True
