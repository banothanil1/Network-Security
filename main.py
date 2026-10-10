import pandas as pd
import numpy as np
import sys
from network_security.components.data_ingestion import DataIngestion
from network_security.entity.config_entity import TrainingPipelineConfig
from network_security.entity.config_entity import DataIngestionConfig
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityFException

if __name__ == "__main__":
    try:
        logging.info("Started the Data ingestion")
        training_pipeline_obj = TrainingPipelineConfig()
        data_ingestion_config_obj = DataIngestionConfig(training_pipeline_obj)
        data_ingestion_obj = DataIngestion(data_ingestion_config=data_ingestion_config_obj)
        dataingestionentityData = data_ingestion_obj.initiate_data_ingestion()
        logging.info("Data ingestioin Completd.")

    except Exception as e:
        raise NetworkSecurityFException(e,sys)