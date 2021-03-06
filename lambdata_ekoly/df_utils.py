"""
    Utility functions for working with dataframes
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from scipy.stats import t, ttest_1samp


TEST_DF = pd.DataFrame([1, 2, 3])


def train_validate_test_split(df, train_size=0.6):
    """
        Splits the {df} into a training set, a val set, and a test set.

        @type df: DataFrame
        @type train_size: float
        @param train_size: The size of the training set. The val and test sets
            will be split 50:50 among the rest
        @returns: tuple of three dataframes
    """
    train, val_test = train_test_split(df, train_size=train_size)
    val, test = train_test_split(val_test, train_size=0.5)

    return train, val, test


def confidenceInterval(data, confidence=0.95):
    """
        Returns the confidence interval and mean for the data within the given
        {confidence}.

        @type data: DataFrame
        @type confidence: float

        @returns: tuple of 3 floats representing the left confidence interval,
            the median, and the right confidence interval for the data.
    """
    data = np.array(data)
    data = data[~np.isnan(data)]
    mean = np.mean(data)
    n = len(data)
    stderr = np.std(data, ddof=1)/np.sqrt(n)
    moe = stderr * t.ppf((1.+confidence)/2., n-1)

    ci1, ci2 = t.interval(confidence, n-1, loc=mean, scale=stderr)
    return (ci1, mean, ci2)


def bayesConfidenceInterval(data, confidence=0.95):
    """
        Returns the confidence interval and mean for the data within the given
        {confidence}.

        @type data: DataFrame
        @type confidence: float

        @returns: tuple of 3 floats representing the left confidence interval,
            the median, and the right confidence interval for the data.
    """
    data = np.array(data)
    data = data[~np.isnan(data)]
    means, _, _ = bayes_mvs(data)
    mean, moe = means
    return (moe[0], mean, moe[1])
