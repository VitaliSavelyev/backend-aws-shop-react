import json
import boto3
import os
import io
import csv

s3 = boto3.client('s3')

def handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    print(f"Received context: {context}")
    try:
        bucket_name = os.getenv('BUCKET_NAME')
        records = event.get('Records')

        if not(records):
            return {
                "statusCode" : 400,
                "headers" : {
                    "Access-Control-Allow-Origin" : "*",
                    "Access-Control-Allow-Methods" : "GET",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "content-type" : "application/json"
                },
                "body": json.dumps("'message':'Incorrect data'")
            }

        for record in records:
            key = record.get('s3', {}).get('object', {}).get('key')

            response = s3.get_object(Bucket=bucket_name, Key=key)

            body = response['Body']

            print(body)

            csv_file = io.StringIO(body.read().decode('utf-8'))
            reader = csv.DictReader(csv_file)
            print("File rows:")
            for row in reader:
                print(row)
            
            copy_source = {
            'Bucket': bucket_name,
            'Key': key
            }

            parsed_key = key.replace('uploaded/', 'parsed/')
            s3.copy_object(CopySource=copy_source, Bucket=bucket_name, Key=parsed_key)

            print(key, key != 'uploaded/')

            if key != 'uploaded/':
                s3.delete_object(Bucket=bucket_name, Key=key)
    except Exception as e:
        return {
            "statusCode" : 500,
            "body": json.dumps({'error': str(e)})
        }
