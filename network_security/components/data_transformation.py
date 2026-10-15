import pandas as pd
import numpy as np
import sys
import os
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from network_security.utils.main_utils.utils import store_pickle_file,create_npy_file
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityFException
from network_security.entity.data_ingestion_entity import DataValidationEntity,DataTransformationEntity
from network_security.entity.data_ingestion_entity import DataValidationEntity
from network_security.entity.config_entity import DataTransformationConfig
from network_security.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS , TARGET_COLUMN

class DataTransformation:
    """this constructor is used to get the data data transformation configuration details"""
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_entity:DataValidationEntity):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_entity = data_validation_entity
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

    def knnImputation(self)->Pipeline:
        """this function will do the knn imputatation and returns the object recived from and of type pipline"""
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor:Pipeline = Pipeline([("imputer",imputer)])
            logging.info("Preprocesser object created and returned.")
            return preprocessor
        except Exception as e:
            raise NetworkSecurityFException(e,sys)
    @staticmethod
    def read_data(filePath:str)->pd.DataFrame:
        """this function just reads the data using given filepath"""
        try:
            df = pd.read_csv(filePath)
            logging.info(f'Data frame read and returns using filePath {filePath}')
            return df
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

    def initiate_data_transformation(self):
        """this function initiates the data transeformation process"""
        try:
            train_data = self.read_data(self.data_validation_entity.valid_train_file_path)
            test_data = self.read_data(self.data_validation_entity.valid_test_file_path)

            #transforming the target features values as classification problem since it only -1,1 so making -1 to 0
            train_data[TARGET_COLUMN] = train_data[TARGET_COLUMN].replace(-1,0)
            test_data[TARGET_COLUMN] = test_data[TARGET_COLUMN].replace(-1,0)
            logging.info('Replaced Train and Test Targets -1 with 0')
            train_data_input_df = train_data.drop(TARGET_COLUMN,axis=1)
            train_data_output_df = train_data[TARGET_COLUMN]
            test_data_input_df = test_data.drop(TARGET_COLUMN,axis=1)
            test_data_output_df = test_data[TARGET_COLUMN]
            
            #applying the transformation on both train and test data
            preprocessor = self.knnImputation()
            trasformed_train_data_input_df = preprocessor.fit_transform(train_data_input_df)
            trasformed_test_data_input_df = preprocessor.transform(test_data_input_df)
            
            #just concatenating the transformed train and non transformed test data
            trained_np_df = np.c_[trasformed_train_data_input_df,train_data_output_df]
            test_np_df = np.c_[trasformed_test_data_input_df,test_data_output_df]
            
            #storing the transformed data to respective file paths
            create_npy_file(filePath=self.data_transformation_config.transformed_train_data_file_path, np_array=trained_np_df)
            create_npy_file(filePath=self.data_transformation_config.transformed_test_data_file_path, np_array=test_np_df)
            logging.info(f"Transformed Train and Test is stored in respective Folders. and in dir {self.data_transformation_config.trasformed_data_dir_path} ")
            
            #storing the preprocesser object in respective folder
            store_pickle_file(filePath=self.data_transformation_config.transformed_data_object_file_path,obj=preprocessor)
            logging.info(f"Preprocesser File has been stored in path {self.data_transformation_config.transformed_data_object_file_path}.")

            #storing preprocesser obj in final_model for the future prediction
            model_path = os.path.join("final_models", "preprocessor.pkl")
            store_pickle_file(filePath=model_path, obj=preprocessor)
                        
            #preparing the artifact
            data_transformation_artifact:DataTransformationEntity = DataTransformationEntity(
                data_transformation_dir_path=self.data_transformation_config.data_transformation_dir_path,
                trasformed_train_data_file_path=self.data_transformation_config.transformed_train_data_file_path,
                trasformed_test_data_file_path=self.data_transformation_config.transformed_test_data_file_path,
                trasformed_data_object_dir_path=self.data_transformation_config.transformed_data_object_dir_path,
                trasformed_data_object_file_path=self.data_transformation_config.transformed_data_object_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityFException(e,sys)
