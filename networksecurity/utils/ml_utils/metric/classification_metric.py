from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score,precision_score,recall_score
import sys

def get_classification_score(y_true,y_pred)->ClassificationMetricArtifact:
    """
    Calculate classification metrics for binary classification.
    This function computes F1 score, precision, and recall for a binary classification model.
    Parameters:
    ----------
    y_true : array-like, shape (n_samples,)
        Ground truth (correct) target values.
    y_pred : array-like, shape (n_samples,)
        Estimated targets as returned by a classifier.
    Returns:
    -------
    ClassificationMetricArtifact
        A named tuple containing the following classification metrics:
        - f1_score: The F1 score (harmonic mean of precision and recall)
        - precision_score: The precision score (ratio of true positives to predicted positives)
        - recall_score: The recall score (ratio of true positives to actual positives)
    Raises:
    ------
    NetworkSecurityException
        If any error occurs during metric calculation.
    """
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score=precision_score(y_true,y_pred)

        classification_metric =  ClassificationMetricArtifact(f1_score=model_f1_score,
                    precision_score=model_precision_score, 
                    recall_score=model_recall_score)
    
        return classification_metric
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)
