import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)

import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.utils.ml_utils.model.estimator import NetworkModel


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# This below code is to be written now to use the templates for table.html.
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    """
    Root endpoint that redirects to the API documentation.
    
    Returns:

        RedirectResponse: Redirects the user to the FastAPI Swagger documentation page.
    """
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    """
    Endpoint to initiate the training pipeline for the network security model.
    
    This endpoint creates a new instance of the TrainingPipeline class and runs
    the complete pipeline process including data ingestion, validation, transformation, model training, and evaluation.
    
    Returns:
        Response: A response indicating that the training was successful.
        
    Raises:
        NetworkSecurityException: If any error occurs during the training process.
    """
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        
        return Response("Training is successful")
    
    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    """
    Endpoint to make predictions using the trained network security model.
    
    This endpoint accepts a CSV file upload, processes it through the trained model, and returns predictions as an HTML table.
    
    Args:
        request (Request): The FastAPI request object.
        file (UploadFile): The uploaded CSV file containing features for prediction.
        
    Returns:
        TemplateResponse: HTML template with the prediction results displayed as a table.
        
    Raises:
        NetworkSecurityException: If any error occurs during the prediction process.
    """
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
# Entry point of this app
if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)