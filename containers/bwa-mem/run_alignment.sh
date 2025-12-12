#!/bin/bash
set -e

# Variables (passed as environment variables)
RAW_BUCKET=${S3_BUCKET}
PROCESSED_BUCKET=${PROCESSED_BUCKET}
INPUT_FILE=${INPUT_FILE:-input.fastq.gz}
REFERENCE_FILE=genome.fna
OUTPUT_PREFIX=${OUTPUT_PREFIX:-sample}
REGION=us-west-2

# Download input FASTQ and reference from S3
aws s3 cp s3://$RAW_BUCKET/$INPUT_FILE /tmp/$INPUT_FILE --region $REGION
aws s3 cp s3://$RAW_BUCKET/$REFERENCE_FILE /tmp/$REFERENCE_FILE --region $REGION

# Run BWA alignment
bwa mem /tmp/$REFERENCE_FILE /tmp/$INPUT_FILE > /tmp/${OUTPUT_PREFIX}.sam

# Upload SAM to processed bucket
aws s3 cp /tmp/${OUTPUT_PREFIX}.sam s3://$PROCESSED_BUCKET/${OUTPUT_PREFIX}.sam --region $REGION

echo "Alignment complete. Results uploaded to s3://$PROCESSED_BUCKET/${OUTPUT_PREFIX}.sam"
