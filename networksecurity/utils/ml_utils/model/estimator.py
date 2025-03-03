from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME

import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkModel:
    """
    A class that combines a preprocessor and a machine learning model for network security classification tasks.
    This class encapsulates the preprocessing and prediction steps needed for making predictions
    with a trained model in a network security context.
    Attributes:
        preprocessor: An object that implements a transform method to preprocess input data
        model: A trained machine learning model that implements a predict method
    Methods:
        predict(x): Transform input data using the preprocessor and generate predictions using the model
    Raises:
        NetworkSecurityException: If any error occurs during initialization or prediction
    """
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            
            logging.info(f"Predictions made for input: {x}")
        
            return y_hat
        
        except Exception as e:
            logging.error(f"Prediction error for input: {x} - {str(e)}")
            raise NetworkSecurityException(e, sys)