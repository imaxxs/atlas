"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def run_prediction(model_package, data):
    return model_package.model.predict(data)

def run_model_package(model_package_id, queue):
    from foundations_production import load_model_package
    load_model_package(model_package_id)

    