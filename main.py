from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

import sys

if __name__ == '__main__':
    try:
        trainingpiprlineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpiprlineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Data Ingestion object created successfully.")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion process completed successfully.")

        print(dataingestionartifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
