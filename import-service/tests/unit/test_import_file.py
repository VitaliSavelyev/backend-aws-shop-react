import unittest
from unittest.mock import patch, MagicMock
import json
import os
import boto3
from moto import mock_s3

from import_service.lambda_func.import_file import handler

class TestHandler(unittest.TestCase):

    @mock_s3
    @patch.dict(os.environ, {"BUCKET_NAME": "test-bucket"})
    def test_handler_valid_event(self):
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')

        event = {
            'queryStringParameters': {
                'name': 'testfile.txt'
            }
        }
        context = {}

        response = handler(event, context)
        
        self.assertEqual(response['statusCode'], 200)
        self.assertIn("https://", response['body'])
        self.assertIn("testfile.txt", response['body'])

    def test_handler_missing_file_name(self):
        event = {
            'queryStringParameters': {}
        }
        context = {}

        response = handler(event, context)

        expected_response = {
            "statusCode": 404,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Content-Type": "application/json"
            },
            "body": json.dumps("'message':'File not found'")
        }

        self.assertEqual(response, expected_response)

    @mock_s3
    @patch.dict(os.environ, {"BUCKET_NAME": "test-bucket"})
    def test_handler_exception(self):
        with patch('boto3.client') as mock_client:
            mock_client.side_effect = Exception("Test exception")

            event = {
                'queryStringParameters': {
                    'name': 'testfile.txt'
                }
            }
            context = {}

            response = handler(event, context)

            expected_response = {
                "statusCode": 500,
                "body": json.dumps({'error': 'Test exception'})
            }

            self.assertEqual(response, expected_response)

if __name__ == '__main__':
    unittest.main()