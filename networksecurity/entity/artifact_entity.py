from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    """
    Data class representing the artifact produced by the data ingestion process.

    This artifact contains paths to the trained and test data files created during data ingestion.

    Attributes:
        trained_file_path (str): Path to the file containing the training dataset.
        test_file_path (str): Path to the file containing the test dataset.
    """
    trained_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    """
    A dataclass representing the artifact produced by the data validation component.

    Attributes:
        validation_status (bool): Indicates whether the data validation process was successful.
        valid_train_file_path (str): Path to the validated training dataset.
        valid_test_file_path (str): Path to the validated test dataset.
        invalid_train_file_path (str): Path to the invalid training dataset records.
        invalid_test_file_path (str): Path to the invalid test dataset records.
        drift_report_file_path (str): Path to the data drift analysis report file.
    """
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

@dataclass
class DataTransformationArtifact:
    """
DataTransformationArtifact class to store paths to transformed artifacts.

This dataclass encapsulates the file paths for artifacts generated during the data transformation phase
of the machine learning pipeline.

    Attributes:
        transformed_object_file_path (str): Path to the serialized transformation object (e.g., preprocessor, feature transformer).

        transformed_train_file_path (str): Path to the transformed training dataset.

        transformed_test_file_path (str): Path to the transformed testing dataset.
    """
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str

@dataclass
class ClassificationMetricArtifact:
    """
    Entity class for storing classification metrics artifacts.

    This class encapsulates the key performance metrics for a classification model.

    Attributes:
        f1_score (float): The F1 score, which is the harmonic mean of precision and recall.
            F1 = 2 * (precision * recall) / (precision + recall)

        precision_score (float): The precision score representing the ratio of true positives to the sum of true and false positives.

        recall_score (float): The recall score representing the ratio of true positives to the sum of true positives and false negatives.
    """
    f1_score: float
    precision_score: float
    recall_score: float
    
@dataclass
class ModelTrainerArtifact:
    """
    Represents the artifacts generated during the model training phase.

    This class encapsulates the path to the trained model file, as well as
    metrics calculated on training and test datasets.

    Attributes:
        trained_model_file_path (str): Path to the saved trained model file.
        train_metric_artifact (ClassificationMetricArtifact): Performance metrics of the model on the training dataset.
        test_metric_artifact (ClassificationMetricArtifact): Performance metrics of the model on the test dataset.
    """
    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact
