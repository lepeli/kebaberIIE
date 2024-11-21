from redis import Redis

import time

# Connect to redis server


# try:
#     r = Redis(host="redis", port=6379, decode_responses=True)
# except:
#     print("error")


while True:

    print("en attente de job...")
    time.sleep(1)