import json
import boto3
import os

def handler(event, content):

    try:

        dynamoDB = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))
        count_table_name = os.getenv('STOCK_TABLE_NAME')
        product_table_name = os.getenv('PRODUCTS_TABLE_NAME')

        count_table = dynamoDB.Table(count_table_name)
        product_table = dynamoDB.Table(product_table_name)

        count_response = count_table.scan()
        count_items = count_response.get('Items', [])
        product_response = product_table.scan()
        product_items = product_response.get('Items', [])

        product_dict = {item['id']: item for item in product_items}

        for count_item in count_items:
            product_id = count_item['product_id']
            if product_id in product_dict:
                product_dict[product_id]['count'] = str(count_item['count'])
                product_dict[product_id]['price'] = str(product_dict[product_id]['price'])
            else:
                product_dict[product_id] = {
                    'id': product_id,
                    'count': count_item['count']
                }

        products = list(product_dict.values())

        return {
            "statusCode" : 200,
            "headers" : {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Methods" : "GET",
                "Access-Control-Allow-Headers": "Content-Type",
                "content-type" : "application/json"
            },
            "body": json.dumps(products)
        }
    except Exception as e:
        return {
            "statusCode" : 500,
            "body": json.dumps({'error': str(e)})
        }
