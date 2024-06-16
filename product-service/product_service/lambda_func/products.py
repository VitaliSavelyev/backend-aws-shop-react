import json
from mock_products import MockProducts

def handler(event, content):
    products = MockProducts
    return {
        "statusCode" : 200,
        "headers" : {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Methods" : "GET",
            "content-type" : "application/json"
        },
        "body": json.dumps(products)
    }