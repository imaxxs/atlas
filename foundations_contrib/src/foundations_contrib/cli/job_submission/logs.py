"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def stream_job_logs(deployment):
    from foundations_contrib.global_state import log_manager
    from os import environ
    import time
    
    logger = log_manager.get_logger(__name__)
    if environ.get('DISABLE_LOG_STREAMING', 'False') == 'False':
        logger.info('Job queued. Ctrl-C to stop streaming - job will not be interrupted or cancelled.')
        job_running = False

        time.sleep(1)

        try:
            for item in deployment.stream_job_logs():
                if not job_running:
                    logger.info('Job running, streaming logs.')
                    job_running = True
                print(item)
            logger.info("Job '{}' has finished.".format(deployment.job_name()))
        except TimeoutError:
            logger.info('Job cannot be found. Possibly because it has beeen removed from the queue.')
