import redis

user_connection = redis.Redis(
    host='localhost', 
    port=6380, 
    username='dvora', 
    password='redis', 
    decode_responses=True
    )

user_connection.ping()
