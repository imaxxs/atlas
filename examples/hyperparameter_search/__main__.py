"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import vcat
import config
from staged_common.prep import union
from staged_common.models import train_logistic_regression
from staged_common.logging import log_formatted
from staged_titanic.etl import load_data, fill_categorical_nulls, split_inputs_and_targets, split_training_and_validation, impute, one_hot_encode, drop_non_numeric_columns, get_metrics


def main():
    # data prep
    data = load_data().enable_caching()
    data = fill_categorical_nulls(data).enable_caching()
    inputs, targets = split_inputs_and_targets(data).enable_caching().splice(2)

    # feature engineering
    x_train, x_valid, y_train, y_valid = split_training_and_validation(
        inputs, targets).enable_caching().splice(4)
    x_train, x_valid = impute(x_train, x_valid).enable_caching().splice(2)
    x_train, x_valid = one_hot_encode(x_train, x_valid).enable_caching().splice(2)
    x_train, x_valid = drop_non_numeric_columns(x_train, x_valid).enable_caching().splice(2)

    # model training and scoring
    params = {
        'C': vcat.Hyperparameter('C'),
        'max_iter': vcat.Hyperparameter('max_iter'),
    }

    model = train_logistic_regression(x_train, y_train, **params)
    y_train, train_score = get_metrics(model, x_train, y_train, 'Training').splice(2)
    y_valid, valid_score = get_metrics(model, x_valid, y_valid, 'Validation').splice(2)

    # print out the results
    log = log_formatted('\nTraining score was {}\nValidation score was {}', train_score, valid_score)
    for C in [0.25, 0.125, 1.0]:
        for max_iter in [100, 200]:
            log.run(C=C, max_iter=max_iter)

if __name__ == '__main__':
    main()
