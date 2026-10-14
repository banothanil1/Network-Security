import pandas as pd
import numpy as np
import os
import sys
from network_security.entity.data_ingestion_entity import ClassificationReportEntity,ModelTrainerEntity
from network_security.entity.config_entity import ModelTrainerConfig
from network_security.exception.exception import NetworkSecurityFException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataTransformationConfig
from network_security.utils.ml_utils.model.estimator import NetworkModel
from network_security.entity.data_ingestion_entity import DataTransformationEntity
from network_security.utils.main_utils.utils import load_npy_array,load_pickle_file,evaluate_model,store_pickle_file
from network_security.utils.ml_utils.metrics.classification_score import get_classification_score
from sklearn.metrics import f1_score,precision_score,recall_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier,
)
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier  
class ModalTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_entity:DataTransformationEntity):
        """in here intializing the objects"""
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_entity = data_transformation_entity 
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

    def model_train(self,X_train,y_train,X_test,y_test):
        """this function will train the model using the given indep. and dependent data"""
        try:
            #list of classification models
            models = [
                ("Logistic Regression", LogisticRegression()),
                ("Decision Tree", DecisionTreeClassifier()),
                ("Random Forest", RandomForestClassifier()),
                ("AdaBoost", AdaBoostClassifier()),
                ("Gradient Boosting", GradientBoostingClassifier()),
                ("Gaussian Naive Bayes", GaussianNB()),
                ("KNN", KNeighborsClassifier())
            ]
           # List of hyperparameters
            params = {
                "Logistic Regression": {
                    "max_iter": [100, 200]
                },
                "Decision Tree": {
                    "max_depth": [5, 8]
                },
                "Random Forest": {
                    "n_estimators": [30, 50],
                    "max_depth": [5, 8]
                },
                "AdaBoost": {
                    "n_estimators": [30, 50],
                    "learning_rate": [0.5, 1.0]
                },
                "Gradient Boosting": {
                    "n_estimators": [30, 50],
                    "max_depth": [2, 3]
                },
                "Gaussian Naive Bayes": {
                    "var_smoothing": [1e-9, 1e-8]
                },
                "KNN": {
                    "n_neighbors": [3, 5],
                    "weights": ["uniform", "distance"]
                }
            }

            #evaluationg the model and training the model and getting report
            report = evaluate_model(X_train,y_train,X_test,y_test,models,params)
            best_score = max(sorted(report.values()))
            best_model_name = list(report.keys())[list(report.values()).index(best_score)]
            best_model = next(
                model for name, model in models
                if name == best_model_name
            )

            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            #getting the classification report
            classification_report_trained_data = get_classification_score(y_train,y_train_pred)
            classification_report_test_data = get_classification_score(y_test,y_test_pred)

            preprocesser = load_pickle_file(filePath=self.data_transformation_entity.trasformed_data_object_file_path)

            NetworkModel_obj = NetworkModel(model=best_model,preprocesser=preprocesser)

            #now store the preprocessor and model.pkl file
            store_pickle_file(filePath=self.model_trainer_config.model_trainer_trained_model_file_path,obj=NetworkModel_obj)
            logging.info('strored the trained model to the destination folder')

            #storing into the artifact and returning the artifact
            model_trainer_artifact = ModelTrainerEntity(
                model_trainer_dir_path=self.model_trainer_config.model_trainer_dir_path,
                model_trainer_trained_model_dir_path = self.model_trainer_config.model_trainer_trained_model_dir_path,
                model_trainer_trained_model_name_path = self.model_trainer_config.model_trainer_trained_model_file_path,
                trained_model_classification_report=classification_report_trained_data,
                test_model_classification_report=classification_report_test_data
            )
            logging.info("Model training artifact created and returned")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityFException(e,sys)


    def initialize_model_trainer(self):
        """here starts the model training"""

        try:
            #Reading the data from transformed data
            train_data_npy = load_npy_array(self.data_transformation_entity.trasformed_train_data_file_path)
            test_data_npy = load_npy_array(self.data_transformation_entity.trasformed_test_data_file_path)
            logging.info("Loaded the numpy train test arrays")
            X_train,y_train,X_test,y_test = (
                train_data_npy[:,:-1],
                train_data_npy[:,-1],
                test_data_npy[:,:-1],
                test_data_npy[:,-1]
            )
            model_trainer_artifact = self.model_train(X_train,y_train,X_test,y_test)
            logging.info("Finally Model Training completed")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityFException(e,sys)
