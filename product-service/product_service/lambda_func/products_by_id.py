import json
from mock_products import MockProducts

def handler(event, content):
    products = MockProducts

    id = event['pathParametrs']["productId"]
    product = next((obj for obj in products if obj["id"] == id), None)
    if product: 
        return {
            "statusCode" : 200,
            "headers" : {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Methods" : "GET",
                "Access-Control-Allow-Headers": "Content-Type",
                "content-type" : "application/json"
            },
            "body": json.dumps(product)
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