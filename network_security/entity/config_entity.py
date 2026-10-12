from datetime import datetime
import os
import sys
from network_security.constant import training_pipeline
from network_security.exception.exception import NetworkSecurityFException

class TrainingPipelineConfig:
    def __init__ (self, timestamp = datetime.now()):
        """this constructor will have the base setup which will be used by Data ingestion config class"""
        self.timestamp:str = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.artifact_name  = training_pipeline.ARTIFACT_DIR
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_dir = os.path.join(self.artifact_name,self.timestamp)

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        """this function is used to crate child files inside above artifact_dir such as train.csv and test.csv"""
        self.data_ingestion_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIRECTORY_NAME)
        self.training_file_path = os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME)
        self.testing_file_path = os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TEST_FILE_NAME)
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME)
        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION

class DataValidationConfig:
    def __init__ (self,training_pipeline_config:TrainingPipelineConfig):
        """this constructor intiates the constants and configures them"""
        try: 
            self.data_validation_dir_path = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME)
            self.data_validation_valid_dir_path = os.path.join(self.data_validation_dir_path,training_pipeline.DATA_VALIDATION_VALID_DIR)
            self.data_validation_invalid_dir_path = os.path.join(self.data_validation_dir_path,training_pipeline.DATA_VALIDATION_INVALID_DIR)
            self.data_validation_drift_report_dir = os.path.join(self.data_validation_dir_path,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR)
            self.data_validation_drift_report_file_path = os.path.join(self.data_validation_dir_path,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
        
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

class DataTransformationConfig:
    """this constructor Reads the constants and configures the path"""
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
            try:
                self.data_transformation_dir_path = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
                self.trasformed_data_dir_path = os.path.join(self.data_transformation_dir_path,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR_NAME)
                self.transformed_train_data_file_path = os.path.join(self.trasformed_data_dir_path,training_pipeline.TRAIN_FILE_NAME.replace("csv","npy"))
                self.transformed_test_data_file_path = os.path.join(self.trasformed_data_dir_path,training_pipeline.TEST_FILE_NAME.replace("csv","npy"))
                self.transformed_data_object_dir_path = os.path.join(self.data_transformation_dir_path,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR)
                self.transformed_data_object_file_path = os.path.join(self.transformed_data_object_dir_path,training_pipeline.DATA_TRANSFORMATION_TRASFORMED_OBJECT_FILE_NAME)
            except Exception as e:
                raise NetworkSecurityFException(e,sys)
                


        