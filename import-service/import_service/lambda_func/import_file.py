import json
import os
import boto3

def handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    print(f"Received context: {context}")
    try:
        file_name = event.get('queryStringParameters', {}).get('name')

        if not(file_name):
            return {
                "statusCode" : 404,
                "headers" : {
                    "Access-Control-Allow-Origin" : "*",
                    "Access-Control-Allow-Methods" : "GET",
                    "Content-Type" : "application/json"
                },
                "body": json.dumps("'message':'File not found'")
            }
        
        bucket_name = os.getenv('BUCKET_NAME') or 'task-5-bucket'
        key = f"uploaded/{file_name}"

        params = {
            'Bucket': bucket_name,
            'Key': key,
            'ContentType': 'text/csv'
        }
        
        s3 = boto3.client('s3')

        signed_url = s3.generate_presigned_url('put_object', Params=params, ExpiresIn=3600)

        print(f"signed url: {signed_url}")

        return {
            "statusCode" : 200,
            "headers" : {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Methods" : "GET, PUT, POST, DELETE",
                "Access-Control-Allow-Headers": "Content-Type",
                "content-type" : "application/json"
            },
            "body": signed_url
        }
    except Exception as e:
        return {
            "statusCode" : 500,
            "body": json.dumps({'error': str(e)})
        }