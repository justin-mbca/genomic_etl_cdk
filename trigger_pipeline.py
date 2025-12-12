

import boto3
import json
import botocore
import os

# Set your region and state machine ARN
# Set your region and AWS profile
region = 'us-west-2'
aws_profile = 'jzhang2026'

# Create a boto3 session with the specified profile
session = boto3.Session(profile_name=aws_profile, region_name=region)
#state_machine_arn = 'arn:aws:states:us-west-2:298843992168:stateMachine:EmbeddingStateMachine79E88DC2-0e2aLe9aVVoH'  # Paste your ARN here
state_machine_arn = 'arn:aws:states:us-west-2:298843992168:stateMachine:PipelineOrchestrationGenomicsPipelineEC158AFD-v93EDL9LgwKO'  # Paste your ARN here


# Define your pipeline input
input_data = {
    "sample_id": "HG00100",
    "input_bucket": "helix-raw-genomics-data",  # RawGenomicsBucketName
    "processed_bucket": "helix-processed-genomics-data",  # ProcessedGenomicsBucketName
    "input_key": "ERR243027.filt.fastq.gz",
    "reference": "GRCh38"
}

def print_identity_and_region():
    sts = session.client('sts')
    identity = sts.get_caller_identity()
    print(f"AWS Account: {identity['Account']}")
    print(f"User ARN: {identity['Arn']}")
    print(f"Region: {region}")

def main():
    print_identity_and_region()
    stepfunctions = session.client('stepfunctions')
    try:
        response = stepfunctions.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(input_data)
        )
        print("Pipeline started:", response['executionArn'])
    except botocore.exceptions.ClientError as e:
        print("Error starting execution:", e)
    except Exception as e:
        print("Unexpected error:", e)

if __name__ == "__main__":
    main()
