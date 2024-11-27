from redis import Redis
from minio import Minio

import time
import os

# Connect to redis server

r = None

mini = Minio(
            endpoint=os.environ["S3_BUCKET_ADDRESS"],
            region=os.environ["S3_BUCKET_REGION"],
            access_key=os.environ["S3_BUCKET_ACCESS_KEY_ID"],
            secret_key=os.environ["S3_BUCKET_SECRET_ACCESS_KEY"]
            )

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

def handlePicture(pictureId):
    """Function used to handle the picture"""

    pass

def convertPicture(picture):
    """Function that converts the picture into jpeg"""

    pass
