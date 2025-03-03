import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
import dill
import pickle

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its contents as a dictionary.
    
    Args:
        file_path (str): Path to the YAML file.
        
    Returns:
        dict: Contents of the YAML file.
        
    Raises:
        NetworkSecurityException: If there is an error reading the file.
    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Writes content to a YAML file. Optionally replaces the file if it already exists.
    
    Args:
        file_path (str): Path to the YAML file.
        content (object): Content to write to the file.
        replace (bool, optional): Whether to replace the file if it exists. Defaults to False.
        
    Raises:
        NetworkSecurityException: If there is an error writing to the file.
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save a numpy array to a binary file at the specified path.
    The function creates any necessary directories in the file path if they
    don't exist already.

    Parameters
    ----------
    file_path : str
        The full path where the numpy array will be saved.
        If directories in the path don't exist, they will be created.
    array : np.array
        The numpy array to be saved.
    Raises
    ------
    NetworkSecurityException
        If there's an error during the saving process.
    Examples
    --------
    >>> import numpy as np
    >>> data = np.array([1, 2, 3])
    >>> save_numpy_array_data("path/to/save/array.npy", data)
    """

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def save_object(file_path: str, obj: object) -> None:
    """
        Saves a Python object to a file using pickle serialization.

        Args:
            file_path (str): The path to the file where the object will be saved.
                             The directory structure will be created if it doesn't exist.
            obj (object): The Python object to be saved.

        Raises:
            NetworkSecurityException: If any exception occurs during the saving process, it wraps the original exception in a NetworkSecurityException and re-raises it.
    """
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def load_object(file_path: str) -> object:
    """
    Load a serialized Python object from a pickle file.
    
    This function reads a serialized object from the specified file path
    using the pickle module and returns the deserialized object.
    
    Args:
        file_path (str): Path to the pickle file containing the serialized object
        
    Returns:
        object: The deserialized Python object
        
    Raises:
        NetworkSecurityException: If the file doesn't exist or cannot be properly loaded
        Exception: If the specified file path doesn't exist
    """
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def load_numpy_array_data(file_path: str) -> np.array:
    """
    Load numpy array data from a file.
    
    This function reads binary file data from the specified file path
    and loads it as a numpy array.
    
    Args:
        file_path (str): Path to the file containing numpy array data
        
    Returns:
        np.array: Numpy array loaded from the file
        
    Raises:
        NetworkSecurityException: If the file cannot be found or properly loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    

def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    """
    Evaluate multiple machine learning models with hyperparameter tuning.
    
    This function performs the following steps for each model:
    1. Performs grid search with cross-validation to find optimal hyperparameters
    2. Trains the model with the best hyperparameters
    3. Evaluates the model on both training and test data
    4. Computes R2 score for model performance evaluation
    
    Args:
        X_train (array-like): Feature matrix for training data
        y_train (array-like): Target values for training data
        X_test (array-like): Feature matrix for test data
        y_test (array-like): Target values for test data
        models (dict): Dictionary mapping model names to model objects
        param (dict): Dictionary mapping model names to their respective hyperparameter grids
        
    Returns:
        dict: Dictionary mapping model names to their test R2 scores
        
    Raises:
        NetworkSecurityException: If model evaluation fails for any reason
    """
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]

            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise NetworkSecurityException(e, sys)