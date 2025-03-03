import os
import sys

from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig



from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object, load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data, evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

class ModelTrainer:
    """
    ModelTrainer is responsible for training machine learning models for network security analysis.
    This class loads transformed data, trains a model, and evaluates its performance to generate model artifacts.
    Attributes:
        model_trainer_config (ModelTrainerConfig): Configuration settings for model training
        data_transformation_artifact (DataTransformationArtifact): Artifact containing paths to transformed data
    """
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """
        Initiates the model training process using transformed data.
        This method:
        1. Loads the transformed training and testing data
        2. Splits the data into features and target variables
        3. Trains a model using the specified configuration
        4. Evaluates model performance on test data
        Returns:
            ModelTrainerArtifact: Contains information about the trained model including:
                - Model file path
                - Performance metrics like accuracy, precision, recall
                - Training and testing metrics
        Raises:
            NetworkSecurityException: If any error occurs during model training
        """
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
           
            return model_trainer_artifact
 
        except Exception as e:
            raise NetworkSecurityException(e, sys)