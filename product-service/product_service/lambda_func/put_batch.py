import json
import os
import boto3
import uuid

dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns')


def handler(event, context):
    table_name = os.getenv('PRODUCTS_TABLE_NAME')
    stocks_table_name = os.getenv('STOCKS_TABLE_NAME')
    sns_topic_arn = os.getenv('SNS_TOPIC_ARN')

    try:

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
                "body": json.dumps("'message':'Records Not Found'")
            }
        
        for record in records:
            body = json.loads(record['body'])
            print(f"item {body}")

            product_description = body.get('description', '')
            product_title = body.get('title', '')
            product_price = body.get('price', 0)
            product_count = body.get('count', 0)
            product_id = body.get('id', '') or str(uuid.uuid4())

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

            product_item = {
                'id': {'S': product_id},
                'title': {'S': product_title},
                'description': {'S': product_description},
                'price': {'N': str(product_price)}
            }

            stock_item = {
                'product_id': {'S': product_id},
                'count': {'N': str(product_count)}
            }

            transaction_items = [
                {
                    'Put': {
                        'TableName': table_name,
                        'Item': product_item
                    }
                },
                {
                    'Put': {
                        'TableName': stocks_table_name,
                        'Item': stock_item
                    }
                }
            ]

        dynamodb.transact_write_items(TransactItems=transaction_items)
        print(f"Product {product_id} added successfully")

        sns.publish(
            TopicArn=sns_topic_arn,
            Message=json.dumps({
                'default': json.dumps(body),
                'email': f"Product created: {json.dumps(body)}"
            }),
            Subject='Product Creation Notification',
            MessageStructure='json',
            MessageAttributes={
                'price': {
                    'DataType': 'Number',
                    'StringValue': product_price
                }
            }
        )
    except Exception as e:
        print(f"Error adding product {product_id}: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps('Processed successfully')
    }