import os

S3_URL = os.getenv("S3_URL", default="s3.csh.rit.edu")
S3_KEY = os.getenv("S3_KEY", default="")
S3_SECRET = os.getenv("S3_SECRET", default="")
BUCKET_NAME = os.getenv("BUCKET_NAME", default="tunnelvision")

DBNAME = os.getenv("DBNAME", default="imagine2024")
DBUSER = os.getenv("DBUSER", default="")
DBPWD =  os.getenv("DBPWD", default="")
DBHOST = os.getenv("DBHOST", default="postgres.csh.rit.edu")
DBPORT = os.getenv("DBPORT", default="5432")

UI_KEY = os.getenv("UI_KEY", default="")
AI_KEY = os.getenv("AI_KEY", default="")
EXTRA_KEY = os.getenv("EXTRA_KEY", default="")

IP = os.getenv("IP", default="")
PORT = os.getenv("PORT", default="")

DEBUG = os.getenv("DEBUG", default=False)