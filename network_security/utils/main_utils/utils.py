import yaml
import sys
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