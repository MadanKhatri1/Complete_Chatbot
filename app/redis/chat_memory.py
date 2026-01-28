
from .redis_client import get_redis_client
 
redis_client = get_redis_client() 

def add_message(user_id: str , message:str):
    key = f"chat:{user_id}" 
    redis_client.lpush(key,message) 
    redis_client.ltrim(key, 0, 19)  # Keep only last 20 messages
    #Auto expire after 24 hours
    redis_client.expire(key, 86400)

def get_recent_messages(user_id:str, limit: int=5):
    key = f"chat:{user_id}" 
    return redis_client.lrange(key,0,limit-1) 