from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
)
from constructs import Construct


class ImportFile(Stack):

    def __init__(self, scope: Construct, id: str, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket.from_bucket_name(self, 'ImportBucket', bucket_name)

        self.import_file = _lambda.Function(self, "ImportFile",
                                                  runtime=_lambda.Runtime.PYTHON_3_11,
                                                  code=_lambda.Code.from_asset('import_service/lambda_func/'),
                                                  handler="import_file.handler", 
                                                  environment= {
                                                      "BUCKET_NAME": bucket.bucket_name
                                                  })
        
        bucket.grant_put(self.import_file)
        bucket.grant_read_write(self.import_file)