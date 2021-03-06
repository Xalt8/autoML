import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectFwe, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=None)

# Average CV score on the training set was: 0.784767616191904
exported_pipeline = make_pipeline(
    SelectFwe(score_func=f_classif, alpha=0.031),
    StackingEstimator(estimator=BernoulliNB(alpha=1.0, fit_prior=True)),
    StackingEstimator(estimator=LogisticRegression(C=5.0, dual=False, penalty="l2")),
    StackingEstimator(estimator=BernoulliNB(alpha=100.0, fit_prior=True)),
    PCA(iterated_power=5, svd_solver="randomized"),
    LogisticRegression(C=10.0, dual=False, penalty="l2")
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
