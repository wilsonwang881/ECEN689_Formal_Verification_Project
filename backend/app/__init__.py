from flask import Flask
import redis
import logging
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

# Database connection
redis_db = redis.Redis(
    host=app.config["REDIS_DB_IP"],
    port=app.config["REDIS_DB_PORT"]
)

# Set the logger to only output errors
logger = logging.getLogger(('werkzeug'))
logger.setLevel(logging.ERROR)

from app import routes