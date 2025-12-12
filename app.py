#!/usr/bin/env python3
import aws_cdk as cdk
from genomics_pipeline.genomics_pipeline_stack import GenomicsPipelineStack

app = cdk.App()
GenomicsPipelineStack(app, "GenomicsPipelineStack")
app.synth()
