import os

S3_URL = os.getenv("S3_URL", default="s3.csh.rit.edu")
S3_KEY = os.getenv("S3_KEY", default="")
S3_SECRET = os.getenv("S3_SECRET", default="")
BUCKET_NAME = os.getenv("BUCKET_NAME", default="tunnelvision")

DEBUG = os.getenv("DEBUG", default=False)