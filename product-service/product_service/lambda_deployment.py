from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb
)
from product_service.api_gateway import ApiGateway
from product_service.get_products import Products
from product_service.get_product_by_id import ProductsById
from product_service.create_product import CreateProduct
from product_service.put_batch_processor import PutBatchProcessor
from constructs import Construct

class MyCdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        product_table_name = 'products'
        stock_table_name = 'stocks'

        product_table = dynamodb.Table.from_table_name(self, 'ProductTable', product_table_name)
        stock_table = dynamodb.Table.from_table_name(self, 'StockTable', stock_table_name)

        environment = {
            'STOCK_TABLE_NAME' : stock_table_name,
            'PRODUCTS_TABLE_NAME': product_table_name
        }

        get_products_lbd = Products(self, "Products", environment)
        get_products_by_id_lbd = ProductsById(self, "ProductsById", environment)
        create_product_lbd = CreateProduct(self, 'CreateProduct', environment)
        put_batch_processor_lbd = PutBatchProcessor(self, 'PutBatch', environment)

        ApiGateway(self, 
                   "ApiGateway", 
                   get_products_fn=get_products_lbd.get_products, 
                   get_products_by_id_fn=get_products_by_id_lbd.get_products_by_id, 
                   create_product_fn=create_product_lbd.create_product,
                   put_batch_processor_fn=put_batch_processor_lbd.put_batch)
        
        product_table.grant_read_write_data(get_products_lbd.get_products)
        stock_table.grant_read_write_data(get_products_lbd.get_products)
        product_table.grant_read_write_data(get_products_by_id_lbd.get_products_by_id)
        stock_table.grant_read_write_data(get_products_by_id_lbd.get_products_by_id)
        product_table.grant_read_write_data(create_product_lbd.create_product)
        stock_table.grant_read_write_data(create_product_lbd.create_product)
        product_table.grant_read_write_data(put_batch_processor_lbd.put_batch)
        stock_table.grant_read_write_data(put_batch_processor_lbd.put_batch)

