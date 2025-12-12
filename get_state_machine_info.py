import boto3
import json
import os

# Get default region from environment or AWS config
region = os.environ.get('AWS_REGION')
if not region:
    import configparser
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.aws/config'))
    region = config.get('default', 'region', fallback=None)
    if not region:
        region = input('Enter your AWS region (e.g., us-east-1): ')

# List Step Functions state machines
sf = boto3.client('stepfunctions', region_name=region)
response = sf.list_state_machines()

print(f"Region: {region}\n")
print("Available State Machines:")
for sm in response['stateMachines']:
    print(f"- Name: {sm['name']}")
    print(f"  ARN:  {sm['stateMachineArn']}\n")

if response['stateMachines']:
    print("Copy the ARN above and use it in your pipeline trigger script.")
else:
    print("No state machines found in this region.")
