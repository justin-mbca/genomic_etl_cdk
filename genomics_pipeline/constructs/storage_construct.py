from aws_cdk import (
    aws_s3 as s3,
    RemovalPolicy,
    Duration
)
from constructs import Construct

class StorageConstruct(Construct):
    def __init__(self, scope: Construct, id: str, raw_bucket_name: str, processed_bucket_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        self.raw_bucket = s3.Bucket(
            self, "RawGenomicsBucket",
            bucket_name=raw_bucket_name,
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="DeleteOldRawData",
                    enabled=True,
                    expiration=Duration.days(7)
                )
            ]
        )
        
        self.processed_bucket = s3.Bucket(
            self, "ProcessedGenomicsBucket",
            bucket_name=processed_bucket_name,
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )
