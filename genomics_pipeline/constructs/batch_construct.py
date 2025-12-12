from aws_cdk import (
    aws_batch as batch,
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_ec2 as ec2,
    Size,
    Duration
)
from constructs import Construct

class BatchConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        ecr_repository_name: str,
        raw_data_bucket,
        processed_data_bucket,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)
        
        # Get ECR repository
        ecr_repo = ecr.Repository.from_repository_name(
            self, "PipelineECRRepo", ecr_repository_name
        )

        # Create a new VPC for Batch (or use ec2.Vpc.from_lookup for existing)
        vpc = ec2.Vpc(self, "BatchVpc", max_azs=2)

        # IAM role for Batch jobs
        batch_job_role = iam.Role(
            self, "BatchJobRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            description="Role for genomics pipeline batch jobs"
        )

        # Grant S3 permissions
        raw_data_bucket.grant_read(batch_job_role)
        processed_data_bucket.grant_read_write(batch_job_role)

        # Create Fargate compute environment (serverless, uses Spot for 70% savings)
        fargate_spot_environment = batch.FargateComputeEnvironment(
            self, "FargateSpotComputeEnv",
            vpc=vpc,
            spot=True,  # Critical for cost savings
            maxv_cpus=8  # Limit for free tier safety
        )

        # Job queue
        self.job_queue = batch.JobQueue(
            self, "GenomicsJobQueue",
            compute_environments=[
                batch.OrderedComputeEnvironment(
                    compute_environment=fargate_spot_environment,
                    order=1
                )
            ],
            priority=1
        )

        # Container definition
        container = batch.EcsFargateContainerDefinition(
            self, "BwaMemContainer",
            image=ecs.ContainerImage.from_ecr_repository(ecr_repo),
            memory=Size.mebibytes(8192),  # 8GB
            cpu=4,
            job_role=batch_job_role
        )

        # Job definition
        self.job_definition = batch.EcsJobDefinition(
            self, "BwaMemJobDef",
            container=container,
            timeout=Duration.hours(4)
        )

        # Data download Batch job definition
        data_download_container = batch.EcsFargateContainerDefinition(
            self, "DataDownloadContainer",
            image=ecs.ContainerImage.from_ecr_repository(ecr_repo),
            memory=Size.mebibytes(2048),
            cpu=1,
            job_role=batch_job_role,
            environment={
                "S3_BUCKET": raw_data_bucket.bucket_name
            }
        )
        self.data_download_job_definition = batch.EcsJobDefinition(
            self, "DataDownloadJobDef",
            container=data_download_container,
            timeout=Duration.minutes(30)
        )
