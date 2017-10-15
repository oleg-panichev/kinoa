import kinoa

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
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Make predictions
    p = model.predict_proba(X_test)
    p = p[:, 1]

    # Evaluate model
    fbeta = fbeta_score(y_test, np.round(p), 1)
    roc_auc = roc_auc_score(y_test, p)

    # Save experiment results with kinoa
    files = ['example.py']

    experiment_name = 'Logistic Regression'

    scores = {}
    scores['fbeta_score'] = fbeta
    scores['roc_auc'] = roc_auc
    scores['kaggle'] = 'Unknown'

    comments = 'Example with Logistic Regression.'

    kinoa.save(
        files,
        experiment_name=experiment_name,
        scores=scores,
        comments=comments,
        update_html_flag=True
    )


def example_dt():
    X_train, X_test, y_train, y_test = generate_data()

    # Train Logistic regression model
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # Make predictions
    p = model.predict_proba(X_test)
    p = p[:, 1]

    # Evaluate model
    logloss = log_loss(y_test, p)
    roc_auc = roc_auc_score(y_test, p)

    # Save experiment results with kinoa
    files = ['example.py']

    experiment_name = 'Decision Tree Classifier'

    scores = {}
    scores['log_loss'] = logloss
    scores['roc_auc'] = roc_auc
    scores['kaggle'] = 'Unknown'

    comments = 'Example with Decision Tree Classifier.'

    kinoa.save(
        files,
        experiment_name=experiment_name,
        scores=scores,
        comments=comments,
        update_html_flag=True
    )


if __name__ == '__main__':
    example_lr()
    example_dt()
