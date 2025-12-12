from aws_cdk import (
    Stack,
    RemovalPolicy,
    Environment
)
from constructs import Construct
from .constructs.storage_construct import StorageConstruct
from .constructs.batch_construct import BatchConstruct
from .constructs.stepfunctions_construct import PipelineOrchestrationConstruct

class GenomicsPipelineStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # 1. Storage Layer: S3 buckets with lifecycle policies
        storage = StorageConstruct(
            self, "GenomicsStorage",
            raw_bucket_name="helix-raw-genomics-data",
            processed_bucket_name="helix-processed-genomics-data"
        )
        
        # 2. Compute Layer: AWS Batch with Fargate Spot for cost savings
        batch = BatchConstruct(
            self, "BatchCompute",
            ecr_repository_name="bwa-pipeline",
            raw_data_bucket=storage.raw_bucket,
            processed_data_bucket=storage.processed_bucket
        )
        
        # 3. Orchestration Layer: Step Functions state machine
        pipeline = PipelineOrchestrationConstruct(
            self, "PipelineOrchestration",
            batch_job_queue=batch.job_queue,
            batch_job_definition=batch.job_definition,
            raw_bucket=storage.raw_bucket,
            processed_bucket=storage.processed_bucket,
            data_download_job_definition=batch.data_download_job_definition
        )
        
        # Output important ARNs for reference
        self.state_machine_arn = pipeline.state_machine.state_machine_arn
        self.raw_bucket_name = storage.raw_bucket.bucket_name

        from aws_cdk import CfnOutput
        # Output Step Function ARN
        CfnOutput(self, "StepFunctionArn", value=pipeline.state_machine.state_machine_arn, description="Step Functions State Machine ARN")
        # Output Raw S3 Bucket Name
        CfnOutput(self, "RawGenomicsBucketName", value=storage.raw_bucket.bucket_name, description="Raw Genomics S3 Bucket Name")
        # Output Processed S3 Bucket Name
        CfnOutput(self, "ProcessedGenomicsBucketName", value=storage.processed_bucket.bucket_name, description="Processed Genomics S3 Bucket Name")
