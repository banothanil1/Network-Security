import pandas as pd
import numpy as np
import sys

from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModalTrainer

from network_security.entity.config_entity import (
    TrainingPipelineConfig,
    DataValidationConfig,
    DataIngestionConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)
from network_security.entity.data_ingestion_entity import (
    DataIngestionEntity,
    DataValidationEntity,
    DataTransformationEntity,
    ClassificationReportEntity,
    ModelTrainerEntity
)
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityFException
from network_security.constant import training_pipeline

class TrainingPipeline:
    def __init__(self):
        """this will intiate the base config"""
        try:
            self.training_pipeline_config_obj = TrainingPipelineConfig()
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

    def start_data_ingestion_pipeline(self)->DataIngestionEntity:
        """this function will start the data ingestion pipeline"""
        try:
            logging.info("Data ingestion Pipeline Started")
            data_ingestion_config_obj = DataIngestionConfig(self.training_pipeline_config_obj)
            data_ingestion_obj = DataIngestion(data_ingestion_config=data_ingestion_config_obj)
            dataingestionentityData = data_ingestion_obj.initiate_data_ingestion()
            logging.info("Data ingestion Pipeline Completed.")
            return dataingestionentityData
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

    def start_data_validation_pipeline(self,data_ingestion_entity:DataIngestionEntity)->DataValidationEntity:
        """this function start the data validation pipeline"""
        try:
            logging.info("Data Validation pipeline started.")
            data_validation_obj = DataValidation(data_ingestion_entity=data_ingestion_entity,training_pipeline_config=self.training_pipeline_config_obj,training_pipeline=training_pipeline)
            data_validation_artifact = data_validation_obj.initiate_data_validation()
            logging.info("Data Validation pipeline completed")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

    def start_data_transformation_pipeline(self,data_validation_entity:DataValidationEntity)->DataTransformationEntity:
        """this function starts the data transformation pipeline"""
        try:
            logging.info("Data Transformation Pipeline started")
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config_obj)
            data_transformation_object = DataTransformation(data_transformation_config=data_transformation_config,  data_validation_entity= data_validation_entity)
            data_transformation_artifact = data_transformation_object.initiate_data_transformation()
            logging.info("Data Transformation Pipeline completed")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

    def start_model_trainer_pipeline(self,data_transformation_entity:DataTransformationEntity)->ModelTrainerEntity:
        """this function starts the model training pipeline"""
        try:
            logging.info("Model Trainer Pipeline started")
            model_trainer_config_obj = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config_obj)
            model_trainer_obj = ModalTrainer(model_trainer_config=model_trainer_config_obj,data_transformation_entity=data_transformation_entity)
            model_trainer_artifact = model_trainer_obj.initialize_model_trainer()
            logging.info("Model Trainer Pipeline Completed")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

    def start_training_pipeline(self)->ModelTrainerEntity:
        """will use above functions and starts the pipeline step by step"""
        try:
            data_ingestion_artifact = self.start_data_ingestion_pipeline()
            data_validation_artifact = self.start_data_validation_pipeline(data_ingestion_entity=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation_pipeline(data_validation_entity=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer_pipeline(data_transformation_entity=data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityFException(e,sys)