import zipfile
import boto3
from io import BytesIO
import db_util as db


def lambda_handler(event, context):
    print('start of function zip_extractor')
    region = 'us-east-1'
    s3_resource = boto3.resource('s3')
    source = event['Records'][0]['s3']['bucket']['name']
    zip_key = event['Records'][0]['s3']['object']['key']
    zip_obj = s3_resource.Object(bucket_name=source, key=zip_key)
    destination = 'extract-file-destination-ashwin'
    buffer = BytesIO(zip_obj.get()["Body"].read())
    z = zipfile.ZipFile(buffer)
    print('before for loop')

    for i,filename in enumerate(z.namelist()):
        file_info = z.getinfo(filename)
        item = {}
        item['id']={'S':str(i)}
        item['file_name']={'S': zip_key}
        item['extracted_file']={'S': filename}
        print('before db_util print')
        db.db_util(item, 'file-meta-data',region)
        s3_resource.meta.client.upload_fileobj(
            z.open(filename),
            Bucket=destination,
            Key=f'{filename}'
        )