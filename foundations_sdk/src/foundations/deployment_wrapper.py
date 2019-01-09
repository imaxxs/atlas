"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class DeploymentWrapper(object):
    """
    ### The three numerals at the begining are a marker for not generating user documentation for the class.
    Provides user-facing functionality to deployment classes created through integrations (e.g. LocalShellJobDeployment, GCPJobDeployment)

    Arguments:
        deployment: {*JobDeployment} -- The integration-level job deployment to wrap
    """

    def __init__(self, deployment):
        self._deployment = deployment

    def job_name(self):
        """
        Gets the name of the job being run

        Arguments:
            - This method doesn't receive any arguments.

        Returns:
            job_name {string} -- The name of the job being run

        Raises:
            - This method doesn't raise any exception.
        """

        return self._deployment.job_name()

    def is_job_complete(self):
        """
        Returns whether the job being run has completed

        Arguments:
            - This method doesn't receive any arguments.

        Returns:
            is_job_complete {boolean} -- True if the job is done, False otherwise (regardless of success / failure)

        Raises:
            - This method doesn't raise any exception.
        """

        return self._deployment.is_job_complete()

    def fetch_job_results(self, wait_seconds=5):
        """
        Waits for the job to complete and then fetches the results for the job.
        It checks the status of the job periodically to test for completion.

        Arguments:
            wait_seconds {float} -- The number of seconds to wait between job status check attempts (defaults to 5)

        Returns:
            results_dict {dict} -- Dict containing results for the stages. See a description below in Notes.

        Raises:
            RemoteException -- In the event of an exception thrown in the execution environment

        Notes:
            A job is completed when it finishes running due to success or failure. This method will wait for
            any of these events to occur. It's a user responsibility to ensure his job is not programmed in a
            way that makes it run forever.

            The *results_dict* has three keys: *provenance*, *global_stage_context* and *stage_contexts*.
            The value of *provenance* is an object that contains internal information about the execution
            environment.

            The *global_stage_context* value is a dictionary containing the following keys and respective values

            - *uuid*: the universally unique identifier that identifies this stage
            - *stage_log*: log information about this stage
            - *meta_data*: metadata associated to this stage
            - *data_uuid*: the universally unique identifier that identifies data associated to this stage
            - *stage_output*: the stage output
            - *error_information*: any error information associated to this stage
            - *start_time*: the time at which this stage started execution
            - *end_time*: the time at which this stage finished execution
            - *delta_time*: the time difference between *end_time* and *start_time*
            - *is_context_aware*: if this stage is context aware
            - *used_cache*: if the stage is using cache
            - *cache_uuid*: the universally unique identifier that identifies this stage cache
            - *cache_read_time*: the time at which the cache was read
            - *cache_write_time*: the time at which the cache was written
            - *has_stage_output*: if the stage has output

            The *stage_contexts* value is a dictionary in which each key is a UUID identifiying the stages
            upon which this stage depends on. Each value associated to these keys correspond to the
            *global_stage_context* of the corresponding stage.
        """

        from foundations_internal.remote_exception import check_result

        if not self.is_job_complete():
            self.wait_for_deployment_to_complete(wait_seconds=wait_seconds)

        result = self._deployment.fetch_job_results()
        return check_result(self.job_name(), result)

    def wait_for_deployment_to_complete(self, wait_seconds=5):
        """
        Waits for the job to complete. It checks the status of the job periodically to test for completion.

        Arguments:
            wait_seconds {float} -- The number of seconds to wait between job status check attempts (defaults to 5)

        Returns:
            - This method doesn't return a value.

        Raises:
            - This method doesn't raise any exception.

        Notes:
            A job is completed when it finishes running due to success or failure. This method will wait for
            any of these events to occur. It's a user responsibility to ensure his job is not programmed in a
            way that makes it run forever.
        """

        import time
        from foundations.global_state import log_manager

        log = log_manager.get_logger(__name__)

        while not self.is_job_complete():
            log.info("waiting for job `" + self.job_name() + "` to finish")
            time.sleep(wait_seconds)

        log.info("job `" + self.job_name() + "` completed")

    def get_job_status(self):
        """
        Similar to is_job_complete, but with more information

        Arguments:
            - This method doesn't receive any arguments.

        Returns:
            status {string} -- String, which is either "Queued", "Running", "Completed", or "Error"

        Raises:
            - This method doesn't raise any exception.
        """

        return self._deployment.get_job_status()

    def _try_get_results(self, error_handler):
        from foundations.deployment_utils import extract_results

        try:
            return extract_results(self.fetch_job_results())
        except Exception as e:
            if error_handler is not None:
                error_handler(e)
            else:
                raise e
