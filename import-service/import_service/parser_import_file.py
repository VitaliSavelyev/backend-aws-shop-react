from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_iam as iam
)
from constructs import Construct


class ParserImportFile(Stack):

    def __init__(self, scope: Construct, id: str, bucket_name: str,  **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket.from_bucket_name(self, 'ImportBucket', bucket_name)

        self.parser_import_file = _lambda.Function(self, "ParserImportFile",
                                                  runtime=_lambda.Runtime.PYTHON_3_11,
                                                  code=_lambda.Code.from_asset('import_service/lambda_func/'),
                                                  handler="parser_file.handler",
                                                  environment= {
                                                      "BUCKET_NAME": bucket.bucket_name
                                                  })
        
        bucket.grant_put(self.parser_import_file)
        bucket.grant_read_write(self.parser_import_file)
        bucket.grant_delete(self.parser_import_file)

        notification = s3n.LambdaDestination(self.parser_import_file)
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, notification, s3.NotificationKeyFilter(prefix="uploaded/"))