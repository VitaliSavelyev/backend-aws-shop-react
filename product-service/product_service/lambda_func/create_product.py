import json
import boto3
import os
import uuid
from botocore.exceptions import ClientError

def handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    print(f"Received context: {context}")
    try:
        body = json.loads(event['body'])

        product_description = body.get('description', '')
        product_title = body.get('title', '')
        product_price = body.get('price', 0)
        product_count = body.get('count', 0)

        if not(product_title) or not(product_price) or product_price < 0 or product_count < 0:
            return {
                "statusCode" : 400,
                "headers" : {
                    "Access-Control-Allow-Origin" : "*",
                    "Access-Control-Allow-Methods" : "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "content-type" : "application/json"
                },
                "body": json.dumps("'message':'Incorrect data'")
            }
        

        dynamoDB = boto3.client('dynamodb', region_name=os.getenv('AWS_REGION'))

        count_table_name = os.getenv('STOCK_TABLE_NAME')
        product_table_name = os.getenv('PRODUCTS_TABLE_NAME')

        product_id = str(uuid.uuid4())

        transact_items = [
            {
                "Put": {
                    "TableName": product_table_name,
                    "Item": {
                        "id": {"S": product_id},
                        "title": {"S": product_title},
                        "description": {"S": product_description},
                        "price":  {"N": str(product_price)}
                    }
                }
            },
            {
                "Put": {
                    "TableName": count_table_name,
                    "Item": {
                        "product_id": {"S": product_id},
                        "count":  {"N": str(product_count)}
                    }
                }
            }
        ]

        dynamoDB.transact_write_items(TransactItems=transact_items)

        product_item = {'id': product_id, 'title': product_title, 'price': product_price, 'description': product_description}
        
        return {
                "statusCode" : 201,
                "headers" : {
                    "Access-Control-Allow-Origin" : "*",
                    "Access-Control-Allow-Methods" : "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "content-type" : "application/json",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type"
                },
                "body": json.dumps(product_item)
            }
    except ClientError as e:
        return {
            "statusCode": 500,
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Methods" : "POST, OPTIONS",
            "body": json.dumps({"message": "Failed to record transaction", "error": str(e)})
        }
    except Exception as e:
        return {
            "statusCode" : 500,
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Methods" : "POST, OPTIONS",
            "body": json.dumps({'error': str(e)})
        }