import json
import boto3
import os

def handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    print(f"Received context: {context}")
    
    try:
        id = event.get('pathParameters', {}).get('id')

        dynamoDB = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))

        count_table_name = os.getenv('STOCK_TABLE_NAME')
        product_table_name = os.getenv('PRODUCTS_TABLE_NAME')

        product_table = dynamoDB.Table(product_table_name)

        products_response = product_table.get_item(
            Key={'id': id}
        )

        product_item = products_response.get('Item')

        if not product_item:
            return {
                "statusCode" : 404,
                "headers" : {
                    "Access-Control-Allow-Origin" : "*",
                    "Access-Control-Allow-Methods" : "GET",
                    "Content-Type" : "application/json"
                },
                "body": json.dumps("'message':'Product not found'")
            }
        
        count_table = dynamoDB.Table(count_table_name)

        count_response = count_table.get_item(
            Key={'product_id': id}
        )

        count_item = count_response.get('Item', {})

        product = {
            "id" : product_item['id'],
            "title": product_item['title'],
            "description": product_item['description'],
            "price": int(product_item['price']),
            "count": int(count_item.get('count', 0))
        }

        return {
            "statusCode" : 200,
            "headers" : {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Methods" : "GET",
                "Content-Type" : "application/json"
            },
            "body": json.dumps(product)
        }
    except Exception as e:
        return {
            "statusCode" : 500,
            "body": json.dumps({'error': str(e)}),
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Methods" : "GET",
            "Content-Ttype" : "application/json"
        }
