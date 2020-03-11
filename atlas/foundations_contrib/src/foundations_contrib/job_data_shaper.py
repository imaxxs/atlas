

class JobDataShaper(object):
    """
    As below
    """
    @staticmethod
    def shape_data(jobs_data):
        """
        This class (hopefully soon deprecated) takes the shape of the Redis data and massages it to look like
        data from the CompletedJobData class

        Arguments:
            jobs_data {list of dictionaries} - List of job data

        Return:
            jobs_data {list of dictionaries} - List of job data, format changed
        """
        for job in jobs_data:
            job['output_metrics'] = JobDataShaper._change_list_to_dict(
                job['output_metrics'])
            job['input_params'] = JobDataShaper._flatten_argument(
                job['input_params'])

        return jobs_data
    
    @staticmethod
    def shape_output_metrics(output_metrics):
        """
        Changes a list to a dict

        Arguments:
            output_metrics {list} -- List of a job's output_metrics
        
        Return:
            output_metrics {dict} -- Dictionary of a job's output metrics
        """
        return JobDataShaper._change_list_to_dict(output_metrics)

    @staticmethod
    def _change_list_to_dict(output_metrics):
        output_dict = {}
        for metric in output_metrics:
            output_dict.update({metric[1]: metric[2]})
        return output_dict

    @staticmethod
    def _flatten_argument(params):
        for param in params:
            param.update(param['argument'])
            del param['argument']
        return params
