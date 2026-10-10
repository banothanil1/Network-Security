import os
import sys
import pymongo
import pandas as pd
import numpy as np
from typing import List
from datetime import datetime
from network_security.exception.exception import NetworkSecurityFException
from network_security.logging.logger import logging
from network_security.entity.data_ingestion_entity import DataIngestionEntity 

#now importing the Dataingestion config file here so that data ingestion component can use it
from network_security.entity.config_entity import DataIngestionConfig
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

#load the mongo db url for the mongo db connection
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

#now intiate the class
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        """load the Dataingestion config inside constructor """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

    def export_data_as_dataframe(self):
        """this function reads the data from mongodb and return it converting to Dataframe after removing id column and replacing na with nan"""
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            data = pymongo.MongoClient(MONGO_DB_URL)
            collection = data[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            logging.info("Data Retreived from Mongodb and converted to Dataframe")
            for column in df.columns:
                if column == "_id":
                    df = df.drop(column,axis=1)
            df.replace('na',np.nan,inplace=True)
            logging.info("_id column removed and na replaced with nan")
            return df 
            
        except Exception as e:
            raise NetworkSecurityFException(e,sys)
    
    def export_data_to_future_store(self,dataframe):
        """this function will export the data future store"""
        try:
            future_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_name = os.path.dirname(future_store_file_path)
            os.makedirs(dir_name,exist_ok=True)
            dataframe.to_csv(future_store_file_path,index=False,header=True)
            logging.info("Data stored in Future store successfully")
            return dataframe
        
        except Exception as e:
            raise NetworkSecurityFException(e,sys)
        
    def perform_train_test_split(self,dataframe):
        """this function will devide the data into train test split and stores it in the respective folder"""
        try:
            train_data, test_data = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)
            training_file_dir = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(training_file_dir,exist_ok=True)
            testing_file_dir = os.path.dirname(self.data_ingestion_config.testing_file_path)
            os.makedirs(testing_file_dir,exist_ok=True)
            train_data.to_csv(self.data_ingestion_config.training_file_path,header=True,index=False)
            test_data.to_csv(self.data_ingestion_config.testing_file_path,header=True,index=False)
            logging.info('Train Test Split Completed and stored to respective paths')
            return [train_data,test_data]
        
        except Exception as e:
            raise NetworkSecurityFException(e,sys)
    
    def initiate_data_ingestion(self):
        """this function is used to intialize the data ingestion"""
        try:
            df = self.export_data_as_dataframe()
            df = self.export_data_to_future_store(df)
            self.perform_train_test_split(df)
            dataingestionentityData = DataIngestionEntity(self.data_ingestion_config)
            return dataingestionentityData
        
        except Exception as e:
            raise NetworkSecurityFException(e,sys)