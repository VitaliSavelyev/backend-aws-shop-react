import json
import os
import unittest
from unittest.mock import patch
import boto3
from moto import mock_dynamodb2, mock_sns
from product_service.lambda_func.put_batch import handler

class TestLambdaHandler(unittest.TestCase):
    
    @mock_dynamodb2
    @mock_sns
    @patch.dict(os.environ, {
        'PRODUCTS_TABLE_NAME': 'ProductsTable',
        'STOCKS_TABLE_NAME': 'StocksTable',
        'SNS_TOPIC_ARN': 'arn:aws:sns:us-east-1:123456789012:MyTopic'
    })
    def setUp(self):
        self.dynamodb = boto3.client('dynamodb')
        self.sns = boto3.client('sns')

        self.dynamodb.create_table(
            TableName=os.environ['PRODUCTS_TABLE_NAME'],
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        
        self.dynamodb.create_table(
            TableName=os.environ['STOCKS_TABLE_NAME'],
            KeySchema=[{'AttributeName': 'product_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'product_id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )

        self.sns.create_topic(Name='MyTopic')

    @mock_dynamodb2
    @mock_sns
    def test_missing_records(self):
        event = {}
        context = {}
        response = handler(event, context)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Records Not Found', response['body'])

    @mock_dynamodb2
    @mock_sns
    def test_invalid_product_data(self):
        event = {
            'Records': [{
                'body': json.dumps({
                    'title': '',
                    'price': -10,
                    'count': -5
                })
            }]
        }
        context = {}
        response = handler(event, context)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Incorrect data', response['body'])

    @mock_dynamodb2
    @mock_sns
    def test_successful_product_creation(self):
        event = {
            'Records': [{
                'body': json.dumps({
                    'title': 'Test Product',
                    'description': 'A test product',
                    'price': 100,
                    'count': 10
                })
            }]
        }
        context = {}
        response = handler(event, context)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Processed successfully', response['body'])
        
        # Verify DynamoDB
        product_response = self.dynamodb.get_item(
            TableName=os.environ['PRODUCTS_TABLE_NAME'],
            Key={'id': {'S': json.loads(event['Records'][0]['body'])['id']}}
        )
        stock_response = self.dynamodb.get_item(
            TableName=os.environ['STOCKS_TABLE_NAME'],
            Key={'product_id': {'S': json.loads(event['Records'][0]['body'])['id']}}
        )
        self.assertTrue('Item' in product_response)
        self.assertTrue('Item' in stock_response)

        # Verify SNS
        topics = self.sns.list_topics()
        self.assertEqual(len(topics['Topics']), 1)

if __name__ == '__main__':
    unittest.main()