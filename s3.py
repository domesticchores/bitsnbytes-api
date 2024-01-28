import boto3
import logging
from botocore.exceptions import ClientError

def get_file_s3(s3_client, bucket_name, file_hash, expiration=90):

    try:
        resp = s3_client.generate_presigned_url('get_object',
                                             Params={
                                                 'Bucket': bucket_name,
                                                 'Key': file_hash},
                                                 ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return resp

def get_s3_client(s3_url, s3_key, s3_secret):
    s3_client = boto3.client("s3",
                            endpoint_url = s3_url,
                            aws_access_key_id = s3_key,
                            aws_secret_access_key = s3_secret
                             )
    
    return s3_client

def get_bucket(s3_url, s3_key, s3_secret, bucket_name):
    s3 = boto3.resource('s3', 
                        endpoint_url = s3_url,
                        aws_access_key_id = s3_key,
                        aws_secret_access_key = s3_secret
                        )
    
    return s3.Bucket(bucket_name)