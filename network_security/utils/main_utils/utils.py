import yaml
import sys
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.metrics import r2_score,precision_score,recall_score
from sklearn.model_selection import GridSearchCV
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

def load_pickle_file(filePath:str):
    """this function will load the object based on the fiePath given"""
    try:
        if not os.path.exists(filePath):
            raise Exception(f"No file found with given filePath")
        with open(filePath,'rb') as fileObj:
            return pickle.load(fileObj)
    except Exception as e:
        raise NetworkSecurityFException(e,sys)

def load_npy_array(filePath:str):
    """this helper function is used to load the npy files based on filePath given"""
    try:
        if not os.path.exists(filePath):
            raise Exception(f"no such file path found")
        with open(filePath, 'rb') as npy_array:
            return np.load(npy_array)
    except Exception as e:
        raise NetworkSecurityFException(e,sys)

def evaluate_model(X_train,y_train,X_test,y_test,models,params)->dict:
    """this function will basically train the model,hyperparameters it and gives the report"""
    try:
        report:dict = {}
        for model_name,model in models:
            logging.info("Model Training Started")
            grd = GridSearchCV(estimator=model,param_grid=params[model_name],n_jobs=-1,cv=3,verbose=1,scoring="accuracy")
            grd.fit(X=X_train,y=y_train)
            best_params = grd.best_params_
            model.set_params(**best_params)
            model.fit(X=X_train,y=y_train)
            y_test_pred = model.predict(X_test)
            f1 = r2_score(y_test,y_test_pred)
            report[model_name] = f1
        logging.info("Model Training Completed and Report Generated and retured.")
        return report
    except Exception as e:
        raise NetworkSecurityFException(e,sys)
    