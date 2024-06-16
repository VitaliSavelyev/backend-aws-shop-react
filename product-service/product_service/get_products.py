from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda
    # aws_sqs as sqs,
)
from constructs import Construct

class Products(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.get_products = _lambda.Function(self, "GetProductsHandler",
                                                  runtime=_lambda.Runtime.PYTHON_3_11,
                                                  code=_lambda.Code.from_asset('/backend_aws_shop_react/lambda_func'),
                                                  handler="products.handler")
