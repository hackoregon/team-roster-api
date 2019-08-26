# Adapted from https://deployeveryday.com/2017/07/25/building-image-resizer-serverless.html

import boto3
from PIL import Image
import PIL.Image
from io import BytesIO
from os import path, environ

s3 = boto3.resource("s3")
origin_bucket = "hacko-profiles-original"
destination_bucket = "hacko-profiles-resized"
width_size = environ.get("IMAGE_WIDTH") or 600


def lambda_handler(event, context):
    for key in event.get("Records"):
        object_key = key["s3"]["object"]["key"]
        extension = path.splitext(object_key)[1].lower()

        # Grabs the source file
        obj = s3.Object(bucket_name=origin_bucket, key=object_key)
        obj_body = obj.get()["Body"].read()

        # Checking the extension and defining the buffer format
        if extension in [".jpeg", ".jpg"]:
            format = "JPEG"
        if extension in [".png"]:
            format = "PNG"

        # Resizing the image
        img = Image.open(BytesIO(obj_body))
        wpercent = width_size / float(img.size[0])
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((width_size, hsize), Image.ANTIALIAS)
        buffer = BytesIO()
        img.save(buffer, format)
        buffer.seek(0)

        # Uploading the image
        obj = s3.Object(bucket_name=destination_bucket, key=object_key)
        obj.put(Body=buffer)

        # Printing to CloudWatch
        print("File saved at {}/{}".format(destination_bucket, object_key))

