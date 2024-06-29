from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway
)
from constructs import Construct

class ApiGateway(Stack):

    def __init__(self, scope: Construct, id: str, import_product__fn=_lambda, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        api = apigateway.RestApi(self, "ImportServiceApi", rest_api_name="Import Service", 
                                 default_cors_preflight_options = { 
                                     "allow_origins": apigateway.Cors.ALL_ORIGINS,
                                     "allow_methods": apigateway.Cors.ALL_METHODS,
                                     "allow_headers": ["Content-Type", "X-Amz-Date", "Authorization", "X-Api-Key", "X-Amz-Security-Token"]
                                     })
        
        import_resource = api.root.add_resource('import')
        import_resource.add_method('GET', apigateway.LambdaIntegration(import_product__fn))


