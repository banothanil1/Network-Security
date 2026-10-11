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

