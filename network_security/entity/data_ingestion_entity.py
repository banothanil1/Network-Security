import pandas as pd
import numpy as np
from dataclasses import dataclass
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.config_entity import DataValidationConfig
#below class is only a data classes which doesnt contain any methods it just used to return the output of the data ingestion component
@dataclass
class DataIngestionEntity:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        self.training_file_path = data_ingestion_config.training_file_path
        self.testing_file_path = data_ingestion_config.testing_file_path

@dataclass
class DataValidationEntity:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str
@dataclass
class DataTransformationEntity:
    data_transformation_dir_path: str
    trasformed_train_data_file_path: str
    trasformed_test_data_file_path: str
    trasformed_data_object_dir_path: str
    trasformed_data_object_file_path: str

@dataclass
class ClassificationReportEntity:
    f1_score:float
    precision:float
    recall: float
@dataclass
class ModelTrainerEntity:
    model_trainer_dir_path: str
    model_trainer_trained_model_dir_path: str
    model_trainer_trained_model_name_path: str
    trained_model_classification_report:ClassificationReportEntity
    test_model_classification_report:ClassificationReportEntity
