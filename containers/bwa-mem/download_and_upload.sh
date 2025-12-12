#!/bin/bash
set -e

# Download reference genome
echo "Downloading reference genome..."
wget -O /tmp/genome.fna.gz https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.26_GRCh38/GCF_000001405.26_GRCh38_genomic.fna.gz
gunzip /tmp/genome.fna.gz

# Download FASTQ
echo "Downloading FASTQ..."
wget -O /tmp/input.fastq.gz ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG00100/sequence_read/ERR243027.filt.fastq.gz

# Upload to S3 (requires AWS CLI and permissions)
echo "Uploading to S3..."
aws s3 cp /tmp/genome.fna s3://$S3_BUCKET/genome.fna
aws s3 cp /tmp/input.fastq.gz s3://$S3_BUCKET/input.fastq.gz
