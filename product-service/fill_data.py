import boto3
from botocore.exceptions import ClientError
import uuid
import random

# Initialize a session using Amazon DynamoDB
session = boto3.Session(
    aws_access_key_id='ACCESS_KEY',       
    aws_secret_access_key='SECRET_KEY',   
    region_name='us-east-1'                  
)

# Initialize the DynamoDB resource
dynamodb = session.resource('dynamodb')

# Specify the table
table_products = dynamodb.Table('products')
table_stocks = dynamodb.Table('stocks')

# Function to generate a single item

def generate_products():
    number = random.randint(1, 10000)
    return {
        'id': str(uuid.uuid4()),
        'title': f"Title {number}",  
        'description': f"Description for item {number}",  
        'price': round(random.uniform(10, 500))
    }

# Generate 30 items
products = [generate_products() for _ in range(30)]


# Function to insert items
def insert_items(table_products, table_stocks, products):
    for item in products:
        try:
            print(item)
            table_products.put_item(Item=item)
            table_stocks.put_item(Item={'product_id': item['id'], 'count': round(random.uniform(10, 100))})
            print(f"Successfully inserted item: {item}")
        except ClientError as e:
            print(f"Error inserting item: {item}")
            print(e.response['Error']['Message'])


insert_items(table_products, table_stocks, products)