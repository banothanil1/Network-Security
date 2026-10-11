import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
from network_security.exception.exception import NetworkSecurityFException
from network_security.logging.logger import logging
from network_security.entity.data_ingestion_entity import DataIngestionEntity 
from network_security.constant import training_pipeline
from network_security.utils.main_utils.utils import read_yaml_file,write_yaml_file
from network_security.entity.data_ingestion_entity import DataValidationEntity
from scipy.stats import ks_2samp
#now importing the DataValidation config file here so that data ingestion component can use it
from network_security.entity.config_entity import DataValidationConfig
from network_security.entity.config_entity import TrainingPipelineConfig

class DataValidation:
    def __init__(self,data_ingestion_entity:DataIngestionEntity,training_pipeline:training_pipeline,training_pipeline_config:TrainingPipelineConfig,):
        """in this constructor just intiating the required detailed to start data validation"""
        try:
            self.training_file_path = data_ingestion_entity.training_file_path
            self.training_pipeline_config = training_pipeline_config
            self.data_validation_config = DataValidationConfig(self.training_pipeline_config)
            self.testing_file_path = data_ingestion_entity.testing_file_path
            self.schema_file_path = training_pipeline.SCHEMA_FILE_PATH
            self._schema_config = read_yaml_file(filePath=self.schema_file_path)
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

    @staticmethod
    def read_data(filePath):
        """this function simply reads the data"""
        try:
            df = pd.read_csv(filePath)
            return df
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

    def validate_column_count(self,df):
        """this function validates the train data test data columns count with schema column count"""
        try:
            df_column_count = len(df.columns)
            schema_column_count = len(self._schema_config["columns"])
            if df_column_count == schema_column_count:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

    def validate_data_drift(self,baseData:pd.DataFrame,currentData:pd.DataFrame,threshold:float=0.5)->bool:
        """this function returns dict checking whether their is any data drift observed"""
        try:
            report:dict = {}
            status:bool = True
            is_found:bool = False
            for column in baseData.columns:
                score = ks_2samp(baseData[column],currentData[column])
                if score.pvalue  >= threshold:
                    is_found = False
                else :
                    is_found = True
                    status = False
                report.update({column:{
                    "is_drift_found" : is_found,
                    "sample_score" : score.pvalue
                }})

            #report content has been added to drift_report/report.yaml
            write_yaml_file(filePath=self.data_validation_config.data_validation_drift_report_file_path,content=report,replace=False)
            logging.info('report content has been added to drift_report/report.yaml')
            return status
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

    def initiate_data_validation(self):
        """Here starts the data validation steps"""
        try:
            #reading the data train test data
            train_data = DataValidation.read_data(filePath=self.training_file_path)
            test_data = DataValidation.read_data(filePath=self.testing_file_path)
            #validating column count for train test data
            train_column_validation_status = self.validate_column_count(train_data)
            if not train_column_validation_status:
                error_message = f"Train Data column validation level is Failed."
            test_column_validation_status = self.validate_column_count(test_data)
            if not test_column_validation_status:
                error_message = f"Test Data column validation level is Failed."

            status = self.validate_data_drift(baseData=train_data,currentData=test_data)
            ##now adding if data is validated then validated dir artifact
            if status:
                os.makedirs(self.data_validation_config.data_validation_valid_dir_path,exist_ok=True)
                train_data.to_csv(os.path.join(self.data_validation_config.data_validation_valid_dir_path,training_pipeline.TRAIN_FILE_NAME),index=False,header=True)
                test_data.to_csv(os.path.join(self.data_validation_config.data_validation_valid_dir_path,training_pipeline.TEST_FILE_NAME),index=False,header=True)
                logging.info(f"Validated Data has been stored in path: {self.data_validation_config.data_validation_valid_dir_path}")
            else :
                error = f"Validation Failed becouse of the data drift"
            data_validation_artifact = DataValidationEntity(
                validation_status=status,
                valid_train_file_path = os.path.join(self.data_validation_config.data_validation_valid_dir_path,training_pipeline.TRAIN_FILE_NAME),
                valid_test_file_path = os.path.join(self.data_validation_config.data_validation_valid_dir_path,training_pipeline.TEST_FILE_NAME),
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.data_validation_drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityFException(e,sys)
        

    