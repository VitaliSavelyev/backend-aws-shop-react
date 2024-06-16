from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from backend_aws_shop_react.api_gateway import ApiGateway
from backend_aws_shop_react.get_products import Products
from backend_aws_shop_react.get_product_by_id import ProductsById
from constructs import Construct

class MyCdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        get_products_lbd = Products(self, "Products")
        get_products_by_id_lbd = ProductsById(self, "ProductsById")

        ApiGateway(self, "ApiGateway", get_products_fn=get_products_lbd.get_products, get_products_by_id_fn=get_products_by_id_lbd.get_products_by_id)

