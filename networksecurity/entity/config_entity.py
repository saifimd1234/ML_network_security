# here all my config details will be here
from datetime import datetime
import os
from networksecurity.constant import training_pipeline

print(training_pipeline.PIPELINE_NAME)

class TrainingPipelineConfig:
    
    """
    Configuration class for the ML network security training pipeline.
    This class manages the directory structure and timestamping for training artifacts,
    providing a consistent way to organize outputs across training runs. It creates
    timestamped directories for artifacts and establishes paths for saving models and
    other outputs.
    Attributes:
        pipeline_name (str): Name of the training pipeline from configuration.
        artifact_name (str): Base directory name for artifacts from configuration.
        artifact_dir (str): Full path to timestamped artifact directory.
        model_dir (str): Directory path for storing the final trained models.
        timestamp (str): Formatted timestamp string (MM_DD_YYYY_HH_MM_SS).
    Example:
        >>> config = TrainingPipelineConfig()
        >>> print(config.artifact_dir)  # Shows timestamped artifact directory
        >>> print(config.model_dir)     # Shows model directory path
    """

    def __init__(self, timestamp=datetime.now()):
        """
        Initialize the TrainingPipelineConfig with timestamp and directory paths.
        
        Args:
            timestamp (datetime, optional): Timestamp for identifying artifacts. Defaults to current time.
        """
        
        if timestamp is None:
            timestamp = datetime.now()
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)
        self.model_dir = os.path.join("final_model")
        self.timestamp: str = timestamp



class DataIngestionConfig:
    
    """
    Configuration class for managing data ingestion parameters and file paths.
    This class handles all configuration related to the data extraction, storage, and splitting
    process during the data ingestion phase of the machine learning pipeline. It defines the directory
    structure for storing raw and processed data, as well as parameters for the train-test split
    and database connection details.
    Attributes:
        data_ingestion_dir (str): Base directory for all data ingestion artifacts.
        feature_store_file_path (str): Path to store the extracted feature data.
        training_file_path (str): Path to store the training dataset after train-test split.
        testing_file_path (str): Path to store the testing dataset after train-test split.
        train_test_split_ratio (float): Ratio to split data into training and testing sets.
        collection_name (str): MongoDB collection name to extract data from.
        database_name (str): MongoDB database name containing the collection.
    Note:
        This class requires a TrainingPipelineConfig instance to initialize its paths relative
        to the main artifact directory of the training pipeline.
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        """
        Initialize the DataIngestionConfig with necessary file paths and parameters.
        
        Args:
            training_pipeline_config (TrainingPipelineConfig): Configuration object containing base artifact directory and other pipeline settings.
        """
        
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str = os.path.join(
                self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME
            )
        self.training_file_path: str = os.path.join(
                self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME
            )
        self.testing_file_path: str = os.path.join(
                self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME
            )
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME


class DataValidationConfig:
    """
    Configuration class for the data validation process.
    This class defines the file paths for storing validation results, drift reports, and valid/invalid data sets.
    It initializes these paths based on the provided TrainingPipelineConfig object.
    
    Attributes:
        data_validation_dir (str): Directory for storing data validation artifacts.
        valid_data_dir (str): Directory for storing valid data sets.
        invalid_data_dir (str): Directory for storing invalid data sets.
        valid_train_file_path (str): File path for storing the valid training data set.
        valid_test_file_path (str): File path for storing the valid test data set.
        invalid_train_file_path (str): File path for storing the invalid training data set.
        invalid_test_file_path (str): File path for storing the invalid test data set.
        drift_report_file_path (str): File path for storing the data drift report.
        training_pipeline_config (TrainingPipelineConfig): Configuration object containing 
        the base artifact directory and other pipeline settings.
    """
    
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        """
        Initialize the DataValidationConfig with necessary file paths.
        
        Args:
            training_pipeline_config (TrainingPipelineConfig): Configuration object containing base artifact directory and other pipeline settings.
        """

        self.data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )

class DataTransformationConfig:
    """
    DataTransformationConfig is a configuration class for data transformation process in the machine learning pipeline.

    Attributes:
        data_transformation_dir (str): Directory where the data transformation artifacts will be stored.
        transformed_train_file_path (str): File path for the transformed training data.
        transformed_test_file_path (str): File path for the transformed test data.
        transformed_object_file_path (str): File path for the transformed preprocessing object.

    Args:
        training_pipeline_config (TrainingPipelineConfig): Configuration for the training pipeline.
    """
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),
        )
        self.transformed_test_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy"),
        )
        self.transformed_object_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME,
        )
