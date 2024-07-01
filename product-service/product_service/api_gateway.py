from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway
    # aws_sqs as sqs,
)
from constructs import Construct

class ApiGateway(Stack):

    def __init__(self, scope: Construct, construct_id: str, get_products_fn: _lambda, get_products_by_id_fn: _lambda,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api = apigateway.RestApi(self, "ProductServiceApi", rest_api_name="Product Service", 
                                 default_cors_preflight_options = { 
                                     "allow_origins": apigateway.Cors.ALL_ORIGINS,
                                     "allow_methods": apigateway.Cors.ALL_METHODS
                                     })

        products_resource = api.root.add_resource('products')
        products_resource.add_method('GET', apigateway.LambdaIntegration(get_products_fn))

        products_by_id_resource = products_resource.add_resource('{id}')
        products_by_id_resource.add_method('GET', apigateway.LambdaIntegration(get_products_by_id_fn))