from aws_cdk import (
    Stack,
    aws_lambda as _lambda
)
from constructs import Construct
import dotenv
import os

class AuthorizationServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dotenv.load_dotenv()
        login = 'VitaliSavelyev'
        SECRET_KEY = os.getenv(login)

        _lambda.Function(self, "AuthorizationLambda",
                        runtime=_lambda.Runtime.PYTHON_3_11,
                        code=_lambda.Code.from_asset('authorization_service/lambda_func/'),
                        handler="authorization.handler", 
                        environment= { login: SECRET_KEY },
                        function_name='AuthFunction'
                        )
