from aws_lambda_powertools import Logger, Tracer
from aws_xray_sdk.core import xray_recorder

logger = Logger()
tracer = Tracer()


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def process_sample_topic(event, context):
    logger.structure_logs(append=True,
                          AWSTraceHeader=None,
                          traceId=xray_recorder.current_segment().trace_id)
    logger.debug(event)
