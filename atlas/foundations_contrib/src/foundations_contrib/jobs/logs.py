
def job_logs(job_id):
    from foundations_contrib.global_state import config_manager

    job_deployment_class = config_manager['deployment_implementation']['deployment_type']
    job_deployment = job_deployment_class(job_id, None, None)

    job_status = job_deployment.get_job_status()

    if job_status is None or job_status == 'queued':
        return None
    
    return job_deployment.get_job_logs()
