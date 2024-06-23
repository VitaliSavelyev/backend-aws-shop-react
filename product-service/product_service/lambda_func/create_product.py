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

        if not(body['title']) or not(body['price']):
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

        product_item = {'id': product_id, 'title': body['title'], 'price': body['price'], 'description': body['description'] or ''}
        count_item = {'product_id': product_id, 'count': body['count'] or 0}

        transact_items = [
            {
                "Put": {
                    "TableName": product_table_name,
                    "Item": {
                        "id": {"S": product_item["id"]},
                        "title": {"S": product_item["title"]},
                        "description": {"S": product_item["description"]},
                        "price":  {"N": str(product_item["price"])}
                    }
                }
            },
            {
                "Put": {
                    "TableName": count_table_name,
                    "Item": {
                        "product_id": {"S": count_item["product_id"]},
                        "count":  {"N": str(count_item["count"])}
                    }
                }
            }
        ]

        dynamoDB.transact_write_items(TransactItems=transact_items)
        
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