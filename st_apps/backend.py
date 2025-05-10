from fastapi import FastAPI, Form, Body
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
# import wandb
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from xgboost import XGBClassifier

import joblib
import os


api = FastAPI()

# # name of the model artifact
artifact_model_name = "diabetes/model_export:latest"

# # initiate the wandb project
run = wandb.init(project="diabetes",job_type="api")



# model_path = ("final_model.pkl")

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Patient(BaseModel):
    HighBP: int
    HighChol: int
    CholCheck: int
    BMI: int
    Smoker: int
    Stroke: int
    HeartDiseaseorAttack: int
    PhysActivity: int
    Fruits: int
    Veggies: int
    HvyAlcoholConsump: int
    AnyHealthcare: int
    NoDocbcCost: int
    GenHlth: int
    MentHlth: int
    PhysHlth: int
    DiffWalk: int
    Sex: int
    Age: int
    Education: int
    Income: int
    

    # class Config:
    #     schema_extra = {
            # "example":{
            #     "HighBP": 1,
            #     "HighChol": 1,
            #     "CholCheck": 1,
            #     "BMI": 40,
            #     "Smoker": 1,
            #     "Stroke": 0,
            #     "HeartDiseaseorAttack": 0,
            #     "PhysActivity": 0,
            #     "Fruits": 0,
            #     "Veggies": 0,
            #     "HvyAlcoholConsump": 1,
            #     "AnyHealthcare": 1,
            #     "NoDocbcCost": 0,
            #     "GenHlth": 5,
            #     "MentHlth": 18,
            #     "PhysHlth": 15,
            #     "DiffWalk": 1,
            #     "Sex": 0,
            #     "Age": 9,
            #     "Education": 4,
            #     "Income": 3, 
            # }
    #     }

# give a greeting using GET
@api.get("/", response_class=HTMLResponse)
async def root():
    return """
    <p><span style="font-size:28px"><strong>Hello World</strong></span></p>"""\
    """<p><span style="font-size:20px">In this project, we will apply the skills """\
        """acquired in the Deploying a Scalable ML Pipeline in Production course to develop """\
        """a classification model on publicly available"""

@api.post("/predict")
async def get_prediction(patient: Patient):

    ## Dowload the model:
   
    model_path = run.use_artifact(artifact_model_name).file()
    pipe = joblib.load(model_path)

    # Change input into a data frame
    df = pd.DataFrame([patient.dict()])

    # Make prediction
    predict = pipe.predict(df)

    return {"result": "Congrats! You are diagnosed as no diabetes" if predict[0] <= 0.5 else "Unfortunately! Our prediction implies that you may have prediabetes or diabetes, you should go to the hospital for deeper medical diagnose."}
