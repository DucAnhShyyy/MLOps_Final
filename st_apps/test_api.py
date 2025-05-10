from fastapi.testclient import TestClient
from st_apps.backend import api
import os
import pathlib

# Instantiate the testing client with our app.
client = TestClient(api)

# a unit test that tests the status code of the root path
def test_root():
    r = client.get("/")
    assert r.status_code == 200

# a unit test that tests the status code and response 
# for an instance diagnosed with diabetes
def test_get_inference_diabetes():
    patient = {
                "HighBP": 1,
                "HighChol": 1,
                "CholCheck": 1,
                "BMI": 40,
                "Smoker": 1,
                "Stroke": 0,
                "HeartDiseaseorAttack": 0,
                "PhysActivity": 0,
                "Fruits": 0,
                "Veggies": 0,
                "HvyAlcoholConsump": 1,
                "AnyHealthcare": 1,
                "NoDocbcCost": 0,
                "GenHlth": 5,
                "MentHlth": 18,
                "PhysHlth": 15,
                "DiffWalk": 1,
                "Sex": 0,
                "Age": 9,
                "Education": 4,
                "Income": 3, 
            }
    r = client.post("/predict", json=patient)
    # print(r.json())
    assert r.status_code == 200
    assert r.json()['result'] == "Unfortunately! Our prediction implies that you may have prediabetes or diabetes, you should go to the hospital for deeper medical diagnose."

# a unit test that tests the status code and response 
# for an instance diagnosed with no diabetes (healthy)
def test_get_inference_heart_disease():
    patient = {
                "HighBP": 0,
                "HighChol": 0,
                "CholCheck": 0,
                "BMI": 25,
                "Smoker": 1,
                "Stroke": 0,
                "HeartDiseaseorAttack": 0,
                "PhysActivity": 1,
                "Fruits": 0,
                "Veggies": 0,
                "HvyAlcoholConsump": 0,
                "AnyHealthcare": 1,
                "NoDocbcCost": 0,
                "GenHlth": 3,
                "MentHlth": 5,
                "PhysHlth": 4,
                "DiffWalk": 0,
                "Sex": 0,
                "Age": 3,
                "Education": 5,
                "Income": 5, 
    }
    r = client.post("/predict", json=patient)
    print(r.json())
    assert r.status_code == 200
    assert r.json()['result'] == "Congrats! You are diagnosed as no diabetes"

    