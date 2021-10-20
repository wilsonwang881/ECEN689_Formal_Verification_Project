from flask import Flask
import redis
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

redis_db = redis.Redis(
    host=app.config["REDIS_DB_IP"],
    port=app.config["REDIS_DB_PORT"]
)

from app import routes