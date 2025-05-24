from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {"message": "Hello World!"}

@app.get("/about")
def about():
    return {"message": "This is a simple FastAPI application."}


@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str= Path(..., description="The ID of the patient to view", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    return  HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sorted_patients(sort_by: str = Query(..., description= 'Sort patient by age, weight, bmi'), order:str = Query('asc',description='order asc or desc')):
    valid_fields = ['age', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field, select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order, select from asc or desc')
    
    data = load_data()
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=(order == 'desc'))

    return sorted_data
