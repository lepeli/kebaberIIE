from redis import Redis

import time

# Connect to redis server

r = None

try:
    r = Redis(host="redis", port=6379, decode_responses=True)
    print("The redis device has been connected successfuly")
except:
    print("error")


while True:
    try:
        job = r.brpop("compressing_queue", timeout=60)
        if job == None:
            print("Didn't have a job, going to France emploi (asking redis for a new job)")
        else:
            print(f"Received job: {job}")
    except Exception as e:
        print(f"Got error: {e}")