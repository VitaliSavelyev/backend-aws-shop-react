from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway
)
from constructs import Construct

class ApiGateway(Stack):

    def __init__(self, scope: Construct, construct_id: str, import_product__fn=_lambda, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        basic_authorizier_lambda = _lambda.Function.from_function_name(self, 'authFunction', 'AuthFunction')

        api = apigateway.RestApi(self, "ImportServiceApi", rest_api_name="Import Service", 
                                 default_cors_preflight_options = { 
                                     "allow_origins": apigateway.Cors.ALL_ORIGINS,
                                     "allow_methods": apigateway.Cors.ALL_METHODS,
                                     "allow_headers": ["Content-Type", "X-Amz-Date", "Authorization", "X-Api-Key", "X-Amz-Security-Token"]
                                     })
        
        authorizer = apigateway.TokenAuthorizer(self, 'Authorizier',
                                   handler=basic_authorizier_lambda,
                                   identity_source='method.request.header.Authorization')
        
        import_resource = api.root.add_resource('import')
        import_resource.add_method('GET', apigateway.LambdaIntegration(import_product__fn),
                                   authorization_type=apigateway.AuthorizationType.CUSTOM,
                                   authorizer=authorizer)


