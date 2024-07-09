from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_lambda_event_sources as lambda_event_sources,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class PutBatchProcessor(Stack):

    def __init__(self, scope: Construct, construct_id: str, environment, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        create_product_topic = sns.Topic(self, 'CreateProductTopic', topic_name='CreateProductTopic')
        create_product_topic.add_subscription(subscriptions.EmailSubscription('vitalisavelyevsm@gmail.com'))
        create_product_topic.add_subscription(subscriptions.EmailSubscription(
            "vitalisavelyevpol@gmail.com",
            filter_policy={
                "price": sns.SubscriptionFilter.numeric_filter(greater_than_or_equal_to=100)
            }
        ))

        catalog_items_queue = sqs.Queue(self, "CatalogItemsQueue", queue_name='CatalogItemsQueue')

        event_source = lambda_event_sources.SqsEventSource(catalog_items_queue, batch_size=5)

        environment['SNS_TOPIC_ARN'] = create_product_topic.topic_arn



        self.put_batch = _lambda.Function(self, "PutBatch",
                                                  runtime=_lambda.Runtime.PYTHON_3_11,
                                                  code=_lambda.Code.from_asset('product_service/lambda_func/'),
                                                  handler="put_batch.handler", 
                                                  environment=environment)
        
        self.put_batch.add_event_source(event_source)
        catalog_items_queue.grant_consume_messages(self.put_batch)
        create_product_topic.grant_publish(self.put_batch)
