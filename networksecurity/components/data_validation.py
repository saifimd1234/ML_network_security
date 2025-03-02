from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact

from scipy.stats import ks_2samp
 
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging 
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
import pandas as pd
import os,sys
from networksecurity.utils.main_utils.utils import read_yaml_file

class DataValidation:
    """
    Class responsible for validating data quality and detecting data drift
    between training and testing datasets.
    """

    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        """
        Initialize the DataValidation with artifacts and configuration.
        
        Args:
            data_ingestion_artifact (DataIngestionArtifact): Contains paths to ingested data files
            data_validation_config (DataValidationConfig): Configuration for validation process
            
        Raises:
            NetworkSecurityException: If initialization fails
        """   
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    