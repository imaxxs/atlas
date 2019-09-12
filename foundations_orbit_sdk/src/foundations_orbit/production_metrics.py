"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def track_production_metrics(metric_name, metric_values):
    _track_production_metrics_for_job(_redis_key(), metric_name, metric_values)

def _track_production_metrics_for_job(redis_key, metric_name, metric_values):
    import pickle
    from foundations_contrib.global_state import redis_connection

    metrics_list = list(map(_metric_pair_with_normalized_type, metric_values.items()))

    existing_metrics = _existing_metrics_from_redis(redis_key, metric_name)
    metrics_to_store = existing_metrics + metrics_list

    metrics = {metric_name: pickle.dumps(metrics_to_store)}

    redis_connection.hmset(redis_key, metrics)

def _metric_pair_with_normalized_type(key_value_pair):
    column_name, column_value = key_value_pair
    return (column_name, _with_normalized_type(column_value))

def _with_normalized_type(value):
    import numpy

    if isinstance(value, numpy.float32) or isinstance(value, numpy.float64):
        return float(value)

    if isinstance(value, float):
        return value

    try:
        return int(value)
    except (ValueError, TypeError):
        pass

    try:
        return float(value)
    except (ValueError, TypeError):
        pass

    return value

def _existing_metrics_from_redis(redis_key, metric_name):
    import pickle
    from foundations_contrib.global_state import redis_connection

    existing_metrics_from_redis = redis_connection.hmget(redis_key, metric_name)[0]

    if existing_metrics_from_redis is None:
        return []

    return pickle.loads(existing_metrics_from_redis)

def _redis_key():
    import os

    model_name = os.environ['MODEL_NAME']
    project_name = os.environ['PROJECT_NAME']

    if not model_name:
        raise RuntimeError('Model name not set')
    if not project_name:
        raise RuntimeError('Project name not set')
    
    return f'projects:{project_name}:models:{model_name}:production_metrics'