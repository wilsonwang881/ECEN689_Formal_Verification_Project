import os

class Config(object):
    REDIS_DB_IP = os.environ.get("REDIS_DB_IP") or "127.0.0.1"
    REDIS_DB_PORT = os.environ.get("REDIS_DB_PORT") or 6379