import unittest
from unittest.mock import patch
import json
from product_service.lambda_func.products import handler

MockProducts = [
    {"id": "1", "name": "Product 1", "price": 100},
    {"id": "2", "name": "Product 2", "price": 200}
]

class TestHandler(unittest.TestCase):

    @patch('__main__.MockProducts', [
        {"id": "1", "name": "Product 1", "price": 100},
        {"id": "2", "name": "Product 2", "price": 200}
    ])
    def test_handler_returns_all_products(self):
        event = {}
        context = None
        response = handler(event, context)
        
        expected_products = [
            {"id": "1", "name": "Product 1", "price": 100},
            {"id": "2", "name": "Product 2", "price": 200}
        ]
        
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['headers']['content-type'], 'application/json')
        self.assertIn('Access-Control-Allow-Origin', response['headers'])
        self.assertIn('Access-Control-Allow-Methods', response['headers'])
        self.assertIn('Access-Control-Allow-Headers', response['headers'])
        self.assertEqual(json.loads(response['body']), expected_products)

if __name__ == '__main__':
    unittest.main()