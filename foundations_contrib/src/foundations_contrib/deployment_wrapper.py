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

        Example:
            ```python
            import foundations
            from algorithms import train_model

            train_model = foundations.create_stage(train_model)
            model = train_model()
            deployment = model.run()
            job_name = deployment.job_name()
            print('Running job:', job_name)
            ```
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

        Example:
            ```python
            import foundations
            from algorithms import train_model

            train_model = foundations.create_stage(train_model)
            model = train_model()
            deployment = model.run()
            if deployment.is_job_complete():
                print('Job has finished.')
            else:
                print('Job is still running.')
            ```
        """

        return self._deployment.is_job_complete()

    def get_job_details(self, wait_seconds=5):
        from foundations_contrib.job_data_redis import JobDataRedis
        from foundations_contrib.global_state import redis_connection

        self.wait_for_deployment_to_complete(wait_seconds=wait_seconds, log_output=False)

        pipe = JobDataRedis._create_redis_pipeline(redis_connection)
        formatted_job_data = JobDataRedis(pipe, self.job_name()).get_formatted_job_data()
        return formatted_job_data

    def get_metric(self, metric_name, wait_seconds=5):
        from foundations_contrib.job_data_redis import JobDataRedis
        from foundations_contrib.global_state import redis_connection

        self.wait_for_deployment_to_complete(wait_seconds=wait_seconds, log_output=False)

        pipe = JobDataRedis._create_redis_pipeline(redis_connection)
        metric = JobDataRedis(pipe, self.job_name()).get_job_metric(metric_name)
        return metric

    def get_param(self, param_name, wait_seconds=5):
        from foundations_contrib.job_data_redis import JobDataRedis
        from foundations_contrib.global_state import redis_connection

        self.wait_for_deployment_to_complete(wait_seconds=wait_seconds, log_output=False)

        pipe = JobDataRedis._create_redis_pipeline(redis_connection)
        param = JobDataRedis(pipe, self.job_name()).get_job_param(param_name)
        return param

    def wait_for_deployment_to_complete(self, wait_seconds=5, log_output=True):
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

        Example:
            ```python
            import foundations
            from algorithms import train_model

            train_model = foundations.create_stage(train_model)
            model = train_model()
            deployment = model.run()
            deployment.wait_for_deployment_to_complete(wait_seconds=3)
            print('Job has finished.')
            ```
        """

        import time
        from foundations_contrib.global_state import log_manager

        log = log_manager.get_logger(__name__)

        while not self.is_job_complete():
            if log_output:
                log.info("waiting for job `" + self.job_name() + "` to finish")
            time.sleep(wait_seconds)

        if log_output:
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

        Example:
            ```python
            import foundations
            from algorithms import train_model

            train_model = foundations.create_stage(train_model)
            model = train_model()
            deployment = model.run()
            status = deployment.get_job_status()
            print('Current job status:', status)
            ```
        """

        return self._deployment.get_job_status()

    def get_true_job_status(self):
        """
        Similar to get_job_status, but with more information

        Arguments:
            - This method doesn't receive any arguments.

        Returns:
            status {string} -- String, which is either "Queued", "Running", "Completed", or "Error"

        Raises:
            - This method doesn't raise any exception.

        Example:
            ```python
            import foundations
            from algorithms import train_model

            train_model = foundations.create_stage(train_model)
            model = train_model()
            deployment = model.run()
            status = deployment.get_job_status()
            print('Current job status:', status)
            ```
        """

        return self._deployment.get_true_job_status()

    def get_job_logs(self):
        """
        Get stdout log for job deployed with SSH job deployment

        Arguments:
            - This method doesn't receive any arguments.

        Returns:
            log {string} -- String, which is the contents of the stdout log stream
            
        Raises:
            - This method doesn't raise any exception.

        Example:
            ```python
            import foundations
            from algorithms import train_model

            train_model = foundations.create_stage(train_model)
            model = train_model()
            deployment = model.run()
            logs = deployment.get_job_logs()
            print('Stdout log:', logs)
            ```
        """

        if not hasattr(self._deployment, 'get_job_logs'):
            return 'Current deployment method does not support get_job_logs()'
        return self._deployment.get_job_logs()

    def stream_job_logs(self):
        if not hasattr(self._deployment, 'stream_job_logs'):
            raise NotImplementedError('Current deployment method does not support stream_job_logs()')
        return self._deployment.stream_job_logs()