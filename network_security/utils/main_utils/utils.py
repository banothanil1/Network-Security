import yaml
import sys
import pandas as pd
import numpy as np
import pickle
import os
from network_security.exception.exception import NetworkSecurityFException
from network_security.logging.logger import logging
def read_yaml_file(filePath:str):
    """this file reads the schema using the filePath given and returns the schema config"""
    try:
        with open (filePath,'rb') as schema:
            schema = yaml.safe_load(schema)
            return schema
    except Exception as e:
        raise NetworkSecurityFException(e,sys)

def write_yaml_file(filePath:str,content:dict,replace:bool = False):
    """this function takes the filePath and creates the yaml file"""
    try:
        if replace:
            if os.path.exists(filePath):
                os.remove(filePath)
        os.makedirs(os.path.dirname(filePath),exist_ok=True)
        with open(filePath, 'w') as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityFException(e,sys)

def create_npy_file(filePath:str,np_array):
    """this helper function stores the numpy array to the given filePath"""
    try:
        dir_name = os.path.dirname(filePath)
        os.makedirs(dir_name,exist_ok=True)
        with open (filePath,'wb') as file:
            np.save(file,np_array)
        logging.info(f"np array is stored into path {filePath}")
    except Exception as e:
        raise NetworkSecurityFException(e,sys)

def store_pickle_file(filePath:str,obj):
    """this helper function is used to create pickle file in given filePath"""
    try:
        dir_name = os.path.dirname(filePath)
        os.makedirs(dir_name,exist_ok=True)
        with open (filePath, 'wb') as file:
            pickle.dump(obj,file)
        logging.info(f"pickle file has been stored into path {filePath}")
    except Exception as e:
        raise NetworkSecurityFException(e,sys)