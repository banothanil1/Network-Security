import pandas as pd
import numpy as np
from dataclasses import dataclass
from network_security.entity.config_entity import DataIngestionConfig

#below class is only a data classes which doesnt contain any methods it just used to return the output of the data ingestion component
@dataclass
class DataIngestionEntity:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        self.training_file_path = data_ingestion_config.training_file_path
        self.testing_file_path = data_ingestion_config.testing_file_path
