import unittest
from unittest.mock import patch, MagicMock
import json
import boto3
from moto import mock_s3
import os
import io
import csv

from import_service.lambda_func.parser_file import handler

class TestHandler(unittest.TestCase):

    @mock_s3
    @patch.dict(os.environ, {"BUCKET_NAME": "test-bucket"})
    def test_handler_valid_event(self):

        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        s3.put_object(Bucket='test-bucket', Key='uploaded/test.csv', Body='name,age\nJohn,30\nJane,25')

        event = {
            'Records': [
                {
                    's3': {
                        'object': {
                            'key': 'uploaded/test.csv'
                        }
                    }
                }
            ]
        }

        context = {}

        response = handler(event, context)

        copied_object = s3.get_object(Bucket='test-bucket', Key='parsed/test.csv')
        self.assertEqual(copied_object['Body'].read().decode('utf-8'), 'name,age\nJohn,30\nJane,25')

        with self.assertRaises(s3.exceptions.NoSuchKey):
            s3.get_object(Bucket='test-bucket', Key='uploaded/test.csv')


        self.assertEqual(response, None)

    @mock_s3
    @patch.dict(os.environ, {"BUCKET_NAME": "test-bucket"})
    def test_handler_invalid_event(self):
        event = {} 
        context = {}

        response = handler(event, context)

        expected_response = {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "Content-Type",
                "content-type": "application/json"
            },
            "body": json.dumps("'message':'Incorrect data'")
        }

        self.assertEqual(response, expected_response)

    @mock_s3
    @patch.dict(os.environ, {"BUCKET_NAME": "test-bucket"})
    def test_handler_exception(self):

        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')

        event = {
            'Records': [
                {
                    's3': {
                        'object': {
                            'key': 'uploaded/nonexistent.csv'
                        }
                    }
                }
            ]
        }
        context = {}

        response = handler(event, context)

        expected_response = {
            "statusCode": 500,
            "body": json.dumps({'error': 'An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist.'})
        }

        self.assertEqual(response, expected_response)

if __name__ == '__main__':
    unittest.main()