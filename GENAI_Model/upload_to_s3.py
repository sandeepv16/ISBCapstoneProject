import boto3
from datetime import datetime
import os
import configparser



config = configparser.ConfigParser()
config.read('config.ini')

region = config["AWS_REGION"]["aws_region"]

os.environ["AWS_ACCESS_KEY_ID"] = "AKIAVY2PGM2A652MXQMG"
os.environ["AWS_SECRET_ACCESS_KEY"]="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"
os.environ["AWS_DEFAULT_REGION"] =region



def uploadToS3(file_name, bucket):
    s3 = boto3.client('s3')
    # s3.meta.client.upload_file(file_name, bucket, {datetime.now().year}/{datetime.now().month}/{datetime.now().day}/{file_name})

    with open(file_name, "rb") as f:
        s3.upload_fileobj(f, bucket, "{0}/{1}/{2}/{3}".format(datetime.now().year,datetime.now().month,datetime.now().day,file_name))