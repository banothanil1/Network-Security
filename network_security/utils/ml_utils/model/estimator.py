import pandas as pd
import numpy as np
import sys
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityFException

class NetworkModel:
    def __init__(self,model,preprocesser):
        """this constructor just intializes the model and precessor"""
        try:
            self.model = model
            self.preprocesser = preprocesser
        except Exception as e:
            raise NetworkSecurityFException(e,sys)

    def predict(self,new_data):
        try:
            """this function basically transforms and predicts the using the new data"""
            transformed_new_data = self.preprocesser.transform(new_data)
            y_hat = self.model.predict(transformed_new_data)
            return y_hat
        except Exception as e:
            raise NetworkSecurityFException(e,sys)