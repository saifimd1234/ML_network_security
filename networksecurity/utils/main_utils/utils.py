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
            NetworkSecurityException: If any exception occurs during the saving process,
                                      it wraps the original exception in a NetworkSecurityException
                                      and re-raises it.
    """
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e