
class CompleteJob(object):
    """Create and posts a message indicating that a job has been completed
    
    Arguments:
        message_router {MessageRouter} -- The message router with which to push the message with
        pipeline_context {PipelineContext} -- The pipeline context associated with the job
    """
    
    def __init__(self, message_router, pipeline_context):
        self._message_router = message_router
        self._pipeline_context = pipeline_context

    def push_message(self):
        """See above
        """

        self._message_router.push_message('complete_job', {'job_id': self._pipeline_context.file_name, 'project_name': self._pipeline_context.provenance.project_name})
