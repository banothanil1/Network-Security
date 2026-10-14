import os
import pandas as pd
import numpy as np

"""Defining common variable names for training pipeline"""
TARGET_COLUMN: str = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR : str = "Artifacts"
FILE_NAME: str = "PhishingData.csv"
TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

SCHEMA_FILE_PATH:str = os.path.join("data_schema","schema.yaml")

"""Data ingestion related constants starts with DATA_INGESTION VAR NAME"""
DATA_INGESTION_COLLECTION : str = "PHISHING_NETWORK_DATA"
DATA_INGESTION_DATABASE_NAME : str = "ANIL_DB"
DATA_INGESTION_DIRECTORY_NAME : str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

"""Data validation Related Constants starts with DATA_VALIDATION VAR NAME"""
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"

"""Data Transformation related constants starts with DATA_TRANFORMATION var name"""
DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR_NAME:str = "transformed_data"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object"
DATA_TRANSFORMATION_TRASFORMED_OBJECT_FILE_NAME:str = "preprocessor.pkl"

DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values" : np.nan,
    "n_neighbors" : 3,
    "weights" : "uniform",
}

"""Model Training related constants starts with MODAL_TRAINER VAR NAME"""
MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FILLING_THRESHOLD:float = 0.05