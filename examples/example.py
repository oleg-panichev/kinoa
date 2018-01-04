from kinoa import kinoa

import numpy as np

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import fbeta_score, log_loss, roc_auc_score
from sklearn.model_selection import train_test_split


def generate_data():
    # Generate dataset
    X, y = make_classification(random_state=0)

    # Split dataset on train and test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0)

    return X_train, X_test, y_train, y_test


def example_lr():
    X_train, X_test, y_train, y_test = generate_data()

    # Train Logistic regression model
    model_params = {
        'C': 1.0,
        'max_iter': 100,
    }
    model = LogisticRegression(**model_params)
    model.fit(X_train, y_train)

    # Make predictions
    p = model.predict_proba(X_test)
    p = p[:, 1]

    # Evaluate model
    fbeta = fbeta_score(y_test, np.round(p), 1)
    roc_auc = roc_auc_score(y_test, p)

    # Save experiment results with kinoa
    files = [
        'example.py',
        'example_directory_0',
        'example_directory_1/example_file_in_directory_0.txt'
    ]

    experiment_name = 'Logistic Regression'

    params = {}
    for k in model_params:
        params['lr.' + str(k)] = model_params[k]

    scores = {}
    scores['fbeta_score'] = fbeta
    scores['roc_auc'] = roc_auc
    scores['kaggle'] = np.nan

    other = {}
    other['some_value'] = 13

    comments = 'Example with Logistic Regression.'

    kinoa.save(
        files,
        experiment_name=experiment_name,
        params=params,
        scores=scores,
        other=other,
        comments=comments,
        update_html_flag=True,
        working_dir='', 
        sort_log_by='experiment_datetime', 
        sort_log_ascending=True,
        columns_order=[]
    )


def example_dt():
    X_train, X_test, y_train, y_test = generate_data()

    # Train Logistic regression model
    model_params = {
        'max_depth': 6,
        'min_samples_split': 2,
    }
    model = DecisionTreeClassifier(**model_params)
    model.fit(X_train, y_train)

    # Make predictions
    p = model.predict_proba(X_test)
    p = p[:, 1]

    # Evaluate model
    logloss = log_loss(y_test, p)
    roc_auc = roc_auc_score(y_test, p)

    # Save experiment results with kinoa
    files = [
        'example.py',
        'example_directory_0',
        'example_directory_1/example_file_in_directory_1.txt'
    ]

    experiment_name = 'Decision Tree Classifier'

    params = {}
    for k in model_params:
        params['dt.' + str(k)] = model_params[k]

    scores = {}
    scores['log_loss'] = logloss
    scores['roc_auc'] = roc_auc
    scores['kaggle'] = np.nan

    other = {}
    other['some_value'] = 42

    comments = 'Example with Decision Tree Classifier.'

    kinoa.save(
        files,
        experiment_name=experiment_name,
        params=params,
        scores=scores,
        other=other,
        comments=comments,
        update_html_flag=True,
        working_dir='', 
        sort_log_by='experiment_datetime', 
        sort_log_ascending=True,
        columns_order={'scores.kaggle': -1}
    )


if __name__ == '__main__':
    example_lr()
    example_dt()
