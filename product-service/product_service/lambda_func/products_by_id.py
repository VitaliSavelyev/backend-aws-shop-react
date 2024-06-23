import json
import boto3
import os

def handler(event, content):
    try:
        id = event.get('pathParameters', {}).get('id')

        dynamoDB = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))

        count_table_name = os.getenv('STOCK_TABLE_NAME')
        product_table_name = os.getenv('PRODUCTS_TABLE_NAME')

        count_table = dynamoDB.Table(count_table_name)
        product_table = dynamoDB.Table(product_table_name)

        count_item = count_table.get_item(Key={"product_id": id})
        product_item = product_table.get_item(Key={"id": id})

        if product_item: 
            product_item['count'] = count_item or 0
            return {
                "statusCode" : 200,
                "headers" : {
                    "Access-Control-Allow-Origin" : "*",
                    "Access-Control-Allow-Methods" : "GET",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "content-type" : "application/json"
                },
                "body": json.dumps(product_item)
            }
        
        return {
                "statusCode" : 404,
                "headers" : {
                    "Access-Control-Allow-Origin" : "*",
                    "Access-Control-Allow-Methods" : "GET",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "content-type" : "application/json"
                },
                "body": json.dumps("'message':'Product not found'")
            }
    except Exception as e:
        return {
            "statusCode" : 500,
            "body": json.dumps({'error': str(e)})
        }
