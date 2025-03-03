import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file, save_numpy_array_data, save_object

class DataTransformation:
    """
    This class handles the data transformation step in the network security ML pipeline.
    
    It applies necessary transformations on the validated data to prepare it for model training,
    including handling missing values and feature engineering.
    
    Attributes:
        data_validation_artifact (DataValidationArtifact): Artifact containing paths to validated data
        data_transformation_config (DataTransformationConfig): Configuration for data transformation
    """
    def __init__(self, data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        """
        Initialize the DataTransformation class with validation artifacts and configuration.
        
        Args:
            data_validation_artifact (DataValidationArtifact): Contains paths to validated training and test data
            data_transformation_config (DataTransformationConfig): Contains configuration parameters for transformation
            
        Raises:
            NetworkSecurityException: If initialization fails
        """
        try:
            self.data_validation_artifact: DataValidationArtifact = data_validation_artifact
            self.data_transformation_config: DataTransformationConfig = data_transformation_config
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        """
        Read CSV data from a given file path into a pandas DataFrame.
        
        Args:
            file_path (str): Path to the CSV file
            
        Returns:
            pd.DataFrame: Pandas DataFrame containing the data
            
        Raises:
            NetworkSecurityException: If file reading fails
        """
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def get_data_transformer_object(cls) -> Pipeline:
        """
        Create and return a data transformation pipeline.
        
        The pipeline includes a KNNImputer to handle missing values based on
        the parameters defined in DATA_TRANSFORMATION_IMPUTER_PARAMS.
        
        Returns:
            Pipeline: Scikit-learn pipeline with data transformation steps
            
        Raises:
            NetworkSecurityException: If creation of the transformer object fails
        """
        logging.info("Entered the get_data_transformer_object method of Data Transformation class")
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("Data transformation object created successfully.")
            processor: Pipeline = Pipeline([
                ("imputer", imputer)
            ])
            logging.info("Data transformation pipeline created successfully.")
            
            return processor

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Execute the data transformation process on validated data.
        
        This method:
        1. Loads the validated training and test data
        2. Separates features and target variables
        3. Handles class imbalance by replacing -1 with 0 in the target variable
        4. Applies the transformation pipeline to the input features
        5. Combines transformed features with target variables
        6. Saves the transformed data and the preprocessor object
        
        Returns:
            DataTransformationArtifact: Contains paths to transformed data and preprocessor object
            
        Raises:
            NetworkSecurityException: If the transformation process fails
        """
        logging.info("Entered the initiate_data_transformation method of Data Transformation class")
        try:
            logging.info("Starting data transformation.")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            # test dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor = self.get_data_transformer_object()

            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)


            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df) ]
            test_arr = np.c_[ transformed_input_test_feature, np.array(target_feature_test_df) ]

            #save numpy array data
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object( self.data_transformation_config.transformed_object_file_path, preprocessor_object,)

            save_object( "final_model/preprocessor.pkl", preprocessor_object,)


            #preparing artifacts

            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            
            logging.info("Data transformation artifact created successfully.")
            
            return data_transformation_artifact
    
        except Exception as e:
            raise NetworkSecurityException(e,sys)