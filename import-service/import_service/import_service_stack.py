from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from import_service.import_file import ImportFile
from import_service.parser_import_file import ParserImportFile
from import_service.api_gateway import ApiGateway

class ImportServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket_name = 'task-5-bucket-import'

        import_product_lambda__lbd = ImportFile(self, 'ImportLambda', bucket_name)
        ParserImportFile(self, 'ParserLambda', bucket_name)
        ApiGateway(self, 'ApiGateway', import_product__fn = import_product_lambda__lbd.import_file)

