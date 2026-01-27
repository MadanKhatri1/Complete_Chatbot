import redis
import json

r = redis.Redis(host="localhost", port=6379, db=1, decode_responses=True)

def save_booking(user_id: str, booking: dict):
    """
    Save booking info in Redis.
    """
    key = f"booking:{user_id}"
    r.set(key, json.dumps(booking))
    return True

def get_booking(user_id: str):
    """
    Retrieve booking info from Redis.
    """
    key = f"booking:{user_id}"
    data = r.get(key)
    return json.loads(data) if data else None
