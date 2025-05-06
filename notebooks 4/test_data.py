import wandb
import os
import pandas as pd 
import pytest

if not os.getenv("TEST_MODE"):
    WANDB_API_KEY = "1d620fa1eff54f2f0ba01b14c81969f4ce70bd6c"
    wandb.login(key=WANDB_API_KEY)

PROJECT_NAME = "diabetes"

@pytest.fixture(scope="session")
def wandb_run():
    run = wandb.init(project=PROJECT_NAME, job_type="data_check")
    yield run
    run.finish()

def load_artifact_csv(run, artifact_name: str):
    try:
        artifact_ref = f"{PROJECT_NAME}/{artifact_name}:latest"
        artifact = run.use_artifact(artifact_ref)
        artifact_dir = artifact.download()
        
        files = os.listdir(artifact_dir)
        if not files:
            raise ValueError(f"No files found in artifact {artifact_name}")
            
        file_path = os.path.join(artifact_dir, files[0])
        return pd.read_csv(file_path)
    except Exception as e:
        pytest.skip(f"Could not load artifact {artifact_name}: {str(e)}")

@pytest.fixture(scope="session")
def X_train(wandb_run):
    return load_artifact_csv(wandb_run, "X_train.csv")

@pytest.fixture(scope="session")
def y_train(wandb_run):
    return load_artifact_csv(wandb_run, "y_train.csv")

@pytest.fixture(scope="session")
def X_val(wandb_run):
    return load_artifact_csv(wandb_run, "X_val.csv")

@pytest.fixture(scope="session")
def y_val(wandb_run):
    return load_artifact_csv(wandb_run, "y_val.csv")

@pytest.fixture(scope="session")
def X_test(wandb_run):
    return load_artifact_csv(wandb_run, "X_test.csv")

@pytest.fixture(scope="session")
def y_test(wandb_run):
    return load_artifact_csv(wandb_run, "y_test.csv")


def test_X_y_train_same_length(X_train, y_train):
    assert len(X_train) == len(y_train)

def test_X_y_val_same_length(X_val, y_val):
    assert len(X_val) == len(y_val)

def test_X_y_test_same_length(X_test, y_test):
    assert len(X_test) == len(y_test)

def test_y_train_values(y_train):
    assert set(y_train.iloc[:, 0].unique()).issubset({0, 1}) 

@pytest.mark.parametrize("dataset", ["X_train", "X_test"])
def test_number_of_columns(request, dataset):
    data = request.getfixturevalue(dataset)
    assert data.shape[1] == 21

@pytest.mark.parametrize("dataset", ["X_train", "X_test"])
def test_column_presence_and_type(request, dataset):
    data = request.getfixturevalue(dataset)
    required_columns = {
        'HighBP': pd.api.types.is_float_dtype,                 
        'HighChol': pd.api.types.is_float_dtype,                
        'CholCheck': pd.api.types.is_float_dtype,               
        'BMI': pd.api.types.is_float_dtype,                     
        'Smoker': pd.api.types.is_float_dtype,                  
        'Stroke': pd.api.types.is_float_dtype,                  
        'HeartDiseaseorAttack': pd.api.types.is_float_dtype,    
        'PhysActivity': pd.api.types.is_float_dtype,            
        'Fruits': pd.api.types.is_float_dtype,                  
        'Veggies': pd.api.types.is_float_dtype,                 
        'HvyAlcoholConsump': pd.api.types.is_float_dtype,       
        'AnyHealthcare': pd.api.types.is_float_dtype,           
        'NoDocbcCost': pd.api.types.is_float_dtype,             
        'GenHlth': pd.api.types.is_float_dtype,                 
        'MentHlth': pd.api.types.is_float_dtype,                
        'PhysHlth': pd.api.types.is_float_dtype,                
        'DiffWalk': pd.api.types.is_float_dtype,                
        'Sex': pd.api.types.is_float_dtype,                     
        'Age': pd.api.types.is_float_dtype,                     
        'Education': pd.api.types.is_float_dtype,               
        'Income': pd.api.types.is_float_dtype,   
    }

    assert set(data.columns.values).issuperset(set(required_columns.keys()))

    for col_name, format_verification_funct in required_columns.items():

        assert format_verification_funct(data[col_name]), f"Column {col_name} failed test {format_verification_funct}"

def teardown_module(module):
    wandb.finish()
