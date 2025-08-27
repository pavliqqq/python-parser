import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_SCHEME = os.getenv("REDIS_SCHEME")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_DATABASE = os.getenv("REDIS_DATABASE")

if REDIS_PASSWORD:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DATABASE}"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DATABASE}"

start_url = "https://www.kreuzwort-raetsel.net/uebersicht.html"

r = redis.StrictRedis.from_url(REDIS_URL)

r.lpush("kreuzwort:start_urls", start_url)

print("Start url have successfully added")