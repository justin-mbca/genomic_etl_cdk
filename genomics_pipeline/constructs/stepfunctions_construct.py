from aws_cdk import (
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    Duration
)
from constructs import Construct

class PipelineOrchestrationConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        batch_job_queue,
        batch_job_definition,
        raw_bucket,
        processed_bucket,
        **kwargs
    ):
        # Only pass scope and construct_id to the base Construct
        super().__init__(scope, construct_id)
        
        # 0. Data Download Task (Batch)
        # Expect: batch_data_download_job_definition passed in kwargs
        data_download_job_definition = kwargs.get('data_download_job_definition')
        data_download_task = tasks.BatchSubmitJob(
            self, "DataDownload",
            job_definition_arn=data_download_job_definition.job_definition_arn,
            job_queue_arn=batch_job_queue.job_queue_arn,
            job_name="data-download",
            container_overrides=tasks.BatchContainerOverrides(),
            result_path="$.data_download_result"
        )

        # 1. BWA Alignment Task
        bwa_alignment_task = tasks.BatchSubmitJob(
            self, "BwaAlignment",
            job_definition_arn=batch_job_definition.job_definition_arn,
            job_queue_arn=batch_job_queue.job_queue_arn,
            job_name="bwa-alignment",
            container_overrides=tasks.BatchContainerOverrides(
                environment={
                    "S3_BUCKET": raw_bucket.bucket_name,
                    "PROCESSED_BUCKET": processed_bucket.bucket_name,
                    "INPUT_FILE": sfn.JsonPath.string_at("$.input_key"),
                    "REFERENCE": "GRCh38",
                    "OUTPUT_PREFIX": sfn.JsonPath.string_at("$.sample_id")
                }
            ),
            result_path="$.bwa_result"
        )
        
        # 2. Quality Check Lambda Task (placeholder, needs lambda function)
        # quality_lambda = ... (define or import your Lambda function)
        # quality_check_task = tasks.LambdaInvoke(
        #     self, "QualityCheck",
        #     lambda_function=quality_lambda,
        #     result_path="$.qc_result"
        # )
        
        # 3. Create error handling
        failure_state = sfn.Fail(self, "PipelineFailed")
        
        # 4. Define the pipeline with retry logic (without Lambda for now)
        definition = (
            data_download_task
            .add_catch(
                handler=failure_state,
                errors=["States.ALL"],
                result_path="$.error"
            )
            .next(
                bwa_alignment_task
                .add_catch(
                    handler=failure_state,
                    errors=["States.ALL"],
                    result_path="$.error"
                )
            )
            #.next(quality_check_task.add_retry(max_attempts=3, backoff_rate=2.0, interval=Duration.seconds(30)))
        )
        
        # 5. Create state machine
        self.state_machine = sfn.StateMachine(
            self, "GenomicsPipeline",
            definition=definition,
            timeout=Duration.hours(24),
            tracing_enabled=True  # For X-Ray debugging
        )
