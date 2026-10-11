import pandas as pd
import numpy as np
import sys
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation 
from network_security.entity.config_entity import TrainingPipelineConfig
from network_security.entity.config_entity import DataValidationConfig
from network_security.entity.config_entity import DataIngestionConfig
from network_security.logging.logger import logging
from network_security.entity.data_ingestion_entity import DataIngestionEntity
from network_security.exception.exception import NetworkSecurityFException
from network_security.constant import training_pipeline


if __name__ == "__main__":
    try:
        logging.info("Started the Data ingestion")
        training_pipeline_config_obj = TrainingPipelineConfig()
        data_ingestion_config_obj = DataIngestionConfig(training_pipeline_config_obj)
        data_ingestion_obj = DataIngestion(data_ingestion_config=data_ingestion_config_obj)
        dataingestionentityData = data_ingestion_obj.initiate_data_ingestion()
        logging.info("Data ingestioin Completd.")
        ##now starting the data validation
        data_ingestion_entity_obj = DataIngestionEntity(data_ingestion_config_obj)
        data_validation_obj = DataValidation(data_ingestion_entity_obj,training_pipeline,training_pipeline_config_obj)
        data_validation_artifact = data_validation_obj.initiate_data_validation()
        print(data_validation_artifact)
    except Exception as e:
        raise NetworkSecurityFException(e,sys)