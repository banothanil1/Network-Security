import yaml
import sys
import pandas as pd
import numpy as np
import pickle
import os
from network_security.entity.data_ingestion_entity import ClassificationReportEntity
from network_security.exception.exception import NetworkSecurityFException
from network_security.logging.logger import logging
from sklearn.metrics import f1_score,precision_score,recall_score
def get_classification_score(y_true,y_pred):
    """this function is basically used to calculate the classification score"""
    try:
        f1 = f1_score(y_true,y_pred)
        precision = precision_score(y_true,y_pred)
        recall = recall_score(y_true,y_pred)
        classication_score_artifact = ClassificationReportEntity(
            f1_score=f1,
            precision=precision,
            recall=recall
        )
        return classication_score_artifact
    except Exception as e:
        raise NetworkSecurityFException(e,sys)