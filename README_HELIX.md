# Clinico-Genomic Data Pipeline (Helix Portfolio)

## Overview
This project demonstrates a professional-grade, cloud-native ETL pipeline for genomic data, built with AWS CDK, Docker, AWS Batch, and Step Functions. It is designed to showcase skills relevant to a Helix engineering position: reproducibility, cost-efficiency, security, and scalable genomics processing.

---

## Key Features
- **Infrastructure as Code:** All AWS resources (S3, Batch, Step Functions, IAM) are provisioned using AWS CDK (Python).
- **Reproducible Compute:** Bioinformatics tools (e.g., BWA-MEM) are containerized with Docker and run on AWS Batch Fargate Spot for cost savings.
- **Automated Data Ingestion:** Pipeline can download public genomic data directly within AWS, eliminating local data handling.
- **Orchestration:** Step Functions manage the ETL workflow, including error handling and retries.
- **Security Best Practices:**
  - IAM roles with least privilege
  - S3 encryption
  - Non-root Docker user
- **Cost Controls:**
  - Fargate Spot for Batch jobs
  - S3 lifecycle rules for auto-deletion
  - Budget alarms (recommended)

---

## Project Structure
```
genomics-pipeline-cdk/
├── app.py
├── cdk.json
├── requirements.txt
├── README.md
├── README_HELIX.md
├── genomics_pipeline/
│   ├── __init__.py
│   ├── genomics_pipeline_stack.py
│   ├── constructs/
│   │   ├── __init__.py
│   │   ├── batch_construct.py
│   │   ├── stepfunctions_construct.py
│   │   └── storage_construct.py
│   └── lambda_functions/
│       ├── __init__.py
│       ├── trigger_processor.py
│       └── quality_check.py
├── containers/
│   └── bwa-mem/
│       ├── Dockerfile
│       └── download_and_upload.sh
├── data/
├── tests/
│   └── test_stack.py
├── get_state_machine_info.py
└── trigger_pipeline.py
```

---

## How to Deploy and Run

### 1. **Set Up AWS Credentials**
- Use an IAM user or SSO (never root keys).
- Run `aws configure` or `aws configure sso` and `aws sso login`.


### 2. **Build and Push Docker Image**
```bash
docker build -t bwa-pipeline:latest ./containers/bwa-mem/
aws ecr get-login-password --region us-west-2 --profile jzhang2026 | docker login --username AWS --password-stdin 298843992168.dkr.ecr.us-west-2.amazonaws.com
docker tag bwa-pipeline:latest 298843992168.dkr.ecr.us-west-2.amazonaws.com/bwa-pipeline:latest
docker push 298843992168.dkr.ecr.us-west-2.amazonaws.com/bwa-pipeline:latest
```
### 5. **Alignment Step Output**
After running the pipeline, you will find a SAM file (e.g., `HG00100.sam`) in your processed S3 bucket. This file contains the alignment results and can be used for further analysis.

---

## Helix Interview Project Context
This project was built as a technical demonstration for the Senior Genomics Data Engineer position at Helix. It highlights:
- Cloud-native, reproducible genomics pipelines
- Secure, scalable, and cost-effective AWS infrastructure
- Integration of bioinformatics tools and best practices

See the job description and interview prep notes for more information.

### 3. **Deploy CDK Stack**
```
cd genomics-pipeline-cdk
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap aws://<ACCOUNT_ID>/<REGION>
cdk deploy --parameters RawBucketName=helix-raw-genomics-data
```

### 4. **Trigger the Pipeline**
- Find your Step Functions ARN (see `get_state_machine_info.py`).
- Edit `trigger_pipeline.py` with your ARN and run:
```
python trigger_pipeline.py
```

---

## What to Highlight in Your Interview
- **"I built this pipeline with AWS CDK, demonstrating Infrastructure-as-Code expertise."**
- **"I used Docker for reproducibility and AWS Batch with Spot instances for cost-efficient genomics processing."**
- **"The Step Functions state machine ensures robustness with built-in retry and error handling."**
- **"I implemented security best practices: IAM roles with least privilege, S3 encryption, and a non-root Docker user."**
- **"This mirrors Helix's need for scalable, secure pipelines that turn raw data into research-ready datasets."**

---

## Next Steps / Extensions
- Add a de-identification step using Spark on EMR Serverless
- Create an Athena table over output VCFs for SQL querying
- Build a simple React frontend for researchers to trigger pipelines
- Implement data quality dashboards using Amazon QuickSight

---

## Contact
For questions or a technical walkthrough, contact: [your-email@domain.com]
