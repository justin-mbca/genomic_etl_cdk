import aws_cdk as cdk
from genomics_pipeline.genomics_pipeline_stack import GenomicsPipelineStack

def test_stack_synthesizes():
    app = cdk.App()
    stack = GenomicsPipelineStack(app, "TestStack")
    template = app.synth().get_stack_by_name("TestStack").template
    assert "Resources" in template
