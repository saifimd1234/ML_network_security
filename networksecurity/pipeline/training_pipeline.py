import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import(
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
)

from networksecurity.constant.training_pipeline import TRAINING_BUCKET_NAME
from networksecurity.cloud.s3_syncer import S3Sync
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR

import sys


class TrainingPipeline:
    """
    A pipeline class that orchestrates the end-to-end machine learning workflow for network security.
    
    This class manages and coordinates all stages of the ML pipeline including data ingestion, validation, transformation, model training, and artifact synchronization to AWS S3 storage.
    It serves as the central component for training a network security model with automated process management and cloud integration.
    
    Attributes:
        training_pipeline_config (TrainingPipelineConfig): Configuration for the overall training pipeline.
        s3_sync (S3Sync): Utility for synchronizing local files to AWS S3 storage.
    """
    def __init__(self):
        """
        Initialize the TrainingPipeline with default configuration and S3 synchronization utility.
        
        Creates a TrainingPipelineConfig instance that contains timing and path information for the current training run, and initializes the S3Sync utility for cloud storage.
        """
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()
        

    def start_data_ingestion(self):
        """
        Execute the data ingestion stage of the pipeline.
        
        This method initializes the DataIngestion component with appropriate configuration, executes the data ingestion process to extract and prepare raw data from sources, and returns the resulting artifacts.
        
        Returns:
            DataIngestionArtifact: Artifact containing paths to ingested training and test data.
            
        Raises:
            NetworkSecurityException: If data ingestion fails for any reason.
        """
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Start data Ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion completed and artifact: {data_ingestion_artifact}")
            
            return data_ingestion_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        """
        Execute the data validation stage of the pipeline.
        
        This method validates the ingested data by checking schema compliance,
        data quality, and potential data drift. It ensures the data meets
        quality requirements before proceeding with transformation.
        
        Args:
            data_ingestion_artifact (DataIngestionArtifact): Artifact containing paths to ingested data.
            
        Returns:
            DataValidationArtifact: Artifact containing validation results and paths to validated data.
            
        Raises:
            NetworkSecurityException: If data validation fails.
        """
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=data_validation_config)
            logging.info("Initiate the data Validation")
            data_validation_artifact = data_validation.initiate_data_validation()
            
            return data_validation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        """
        Execute the data transformation stage of the pipeline.
        
        This method applies necessary transformations to the validated data,
        such as imputation, scaling, encoding, and feature engineering to
        prepare the data for model training.
        
        Args:
            data_validation_artifact (DataValidationArtifact): Artifact containing paths to validated data.
            
        Returns:
            DataTransformationArtifact: Artifact containing paths to transformed data and preprocessing objects.
            
        Raises:
            NetworkSecurityException: If data transformation fails.
        """
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config)
            
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            
            return data_transformation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        """
        Execute the model training stage of the pipeline.
        
        This method trains a machine learning model using the transformed data,
        tunes hyperparameters, and evaluates model performance using classification metrics.
        It produces a trained model ready for deployment.
        
        Args:
            data_transformation_artifact (DataTransformationArtifact): Artifact containing paths to transformed data.
            
        Returns:
            ModelTrainerArtifact: Artifact containing the trained model path and performance metrics.
            
        Raises:
            NetworkSecurityException: If model training fails.
        """
        try:
            self.model_trainer_config: ModelTrainerConfig = ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config,
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer()

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)    
    
    def sync_artifact_dir_to_s3(self):
        """
        Synchronize local artifacts directory to S3 bucket.
        
        This method uploads all artifacts generated during the pipeline execution
        (including intermediate datasets, validation reports, and transformation objects) to a timestamped location in the configured S3 bucket for tracking and reproducibility.
        
        Raises:
            NetworkSecurityException: If synchronization to S3 fails
        """
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.artifact_dir, aws_bucket_url=aws_bucket_url)
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def sync_saved_model_dir_to_s3(self):
        """
        Synchronize local model directory to S3 bucket.
        
        This method uploads the final trained model to a timestamped location
        in the configured S3 bucket for later use in deployment or inference.
        This ensures model versioning and availability in the cloud.
        
        Raises:
            NetworkSecurityException: If synchronization to S3 fails
        """
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.model_dir, aws_bucket_url=aws_bucket_url)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def run_pipeline(self):
        """
        Execute the complete training pipeline from end to end.
        
        This method orchestrates the entire ML workflow by running all stages in sequence:
        1. Data Ingestion - Extract and prepare raw data
        2. Data Validation - Verify data quality and schema compliance
        3. Data Transformation - Apply preprocessing and feature engineering
        4. Model Training - Train and evaluate the model
        5. Artifact synchronization - Upload artifacts and model to S3
        
        Returns:
            ModelTrainerArtifact: Artifact containing the final trained model and performance metrics
            
        Raises:
            NetworkSecurityException: If any stage of the pipeline fails
        """
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()

            return model_trainer_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
