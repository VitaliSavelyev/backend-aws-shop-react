import unittest
from unittest.mock import patch
import json
from product_service.lambda_func.products import handler

MockProducts = [
    {"id": "1", "name": "Product 1", "price": 100},
    {"id": "2", "name": "Product 2", "price": 200}
]

class TestHandler(unittest.TestCase):

    def test_product_found(self):
        event = {
            'pathParameters': {
                'id': '1'
            }
        }
        context = None
        response = handler(event, context)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['headers']['content-type'], 'application/json')
        self.assertIn('Access-Control-Allow-Origin', response['headers'])
        self.assertIn('Access-Control-Allow-Methods', response['headers'])
        self.assertIn('Access-Control-Allow-Headers', response['headers'])
        self.assertEqual(json.loads(response['body']), {"id": "1", "name": "Product 1", "price": 100})

    def test_product_not_found(self):
        event = {
            'pathParameters': {
                'id': '3'
            }
        }
        context = None
        response = handler(event, context)
        self.assertEqual(response['statusCode'], 404)
        self.assertEqual(response['headers']['content-type'], 'application/json')
        self.assertIn('Access-Control-Allow-Origin', response['headers'])
        self.assertIn('Access-Control-Allow-Methods', response['headers'])
        self.assertIn('Access-Control-Allow-Headers', response['headers'])
        self.assertEqual(json.loads(response['body']), {"message": "Product not found"})

if __name__ == '__main__':
    unittest.main()