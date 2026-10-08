import pandas as pd
import numpy as np
import os
import pymongo
import json
import certifi
import sys
from network_security.exception.exception import NetworkSecurityFException
from network_security.logging.logger import logging
from dotenv import load_dotenv
load_dotenv()

ca = certifi.where()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class push_data :
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityFException(e,sys)
    
    def csv_to_json_converter(self,filePath):
        '''this function converts the csv data to json format'''
        try:
            df = pd.read_csv(filePath)
            df.reset_index(drop=True,inplace=True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

    def push_data_mongodb(self,records,database,collection):
        '''this functioin inserts the data to the mongo db and returns the length of inserted records'''
        try:
            self.records = records
            self.database = database
            self.collection = collection
            self.connection = pymongo.MongoClient(MONGO_DB_URL,tls=True,tlsCAFile=ca)
            self.connection.admin.command("ping")
            print("MongoDB connection successful!")
            self.database = self.connection[database]
            self.collection = self.database[collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

if __name__ == "__main__":
    push_data_obj = push_data()
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "ANIL_DB"
    COLLECTION = "PHISHING_NETWORK_DATA"
    list_of_json_data = push_data_obj.csv_to_json_converter('Network_Data\phisingData.csv')
    print(list_of_json_data)
    no_of_records = push_data_obj.push_data_mongodb(records=list_of_json_data,database=DATABASE,collection=COLLECTION)
    print(no_of_records)
