from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Literal, List, Dict, Optional, Annotated
import json

app = FastAPI()

# --- Data Persistence Functions ---

def load_data():
    """Loads patient data from a JSON file."""
    try:
        with open('patients.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, return an empty dictionary
        return {}

def save_data(data):
    """Saves patient data to a JSON file."""
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=4) # Use indent for better readability

# --- Pydantic Model ---

class Patient(BaseModel):
    """Represents a single patient record."""
    id: Annotated[str, Field(..., description='The unique id of the patient', example='P001')]
    name: Annotated[str, Field(..., max_length=50, description='Name of the patient')]
    city: Annotated[str, Field(..., description="City of the patient", example='kathmandu')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in cm')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kg')]

    # Corrected: Use the lowercase 'computed_field' decorator
    @computed_field
    @property
    def bmi(self) -> float:
        """Calculates the Body Mass Index (BMI)."""
        # Added a check to prevent division by zero
        if self.height > 0:
            bmi = self.weight / ((self.height / 100) ** 2)
            return round(bmi, 2)
        return 0.0

    # Corrected: Use the lowercase 'computed_field' decorator
    @computed_field
    @property
    def verdict(self) -> str:
        """Provides a health verdict based on BMI."""
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"
#second pydantic model update
class PatientUpdate(BaseModel):
    """Represents a patient record for updates."""
    name: Annotated[Optional[str], Field(None, max_length=50, description='Name of the patient')]
    city: Annotated[Optional[str], Field(None, description="City of the patient")]
    age: Annotated[Optional[int], Field(None, gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Optional[Literal['male', 'female', 'other']], Field(None, description='Gender of the patient')]
    height: Annotated[Optional[float], Field(None, gt=0, description='Height of the patient in cm')]
    weight: Annotated[Optional[float], Field(None, gt=0, description='Weight of the patient in kg')]


# --- API Endpoints ---

@app.get("/")
def hello():
    """Root endpoint with a welcome message."""
    return {"message": "Patient management system API"}

@app.get('/about')
def about():
    """Provides information about the API."""
    return {"message": "A fully functional API to manage patient records"}

@app.get('/view', response_model=Dict[str, Patient])
def view():
    """Retrieves all patient records."""
    return load_data()

@app.get('/patient/{patient_id}', response_model=Patient)
def view_patient(patient_id: str = Path(..., description="The ID of the patient in the DB", example="P001")):
    """Retrieves a single patient by their ID."""
    data = load_data()
    if patient_id in data:
        # Create a Patient instance to include computed fields
        patient_data = data[patient_id]
        # The id is not stored in the value, so we add it back for model validation
        patient_data['id'] = patient_id
        return Patient(**patient_data)
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort', response_model=List[Patient])
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight, or bmi'),
                  order: str = Query('asc', description='Sort in asc or desc order')):
    """Sorts patients by a specified field."""
    valid_fields = ['height', 'weight', 'bmi', 'age', 'name']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Select from {valid_fields}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order. Select from ['asc', 'desc']")

    data = load_data()
    
    # Convert dictionary of patients into a list of Patient objects
    patients_list = []
    for p_id, p_data in data.items():
        p_data['id'] = p_id  # Add id back to the dictionary
        patients_list.append(Patient(**p_data))

    # Corrected: The 'reverse' parameter for sorted() expects a boolean
    reverse_order = True if order == 'desc' else False
    
    # Now sorting on the attribute of the Patient object
    sorted_patients = sorted(patients_list, key=lambda p: getattr(p, sort_by), reverse=reverse_order)
    
    return sorted_patients

@app.post('/create', status_code=201)
def create_patient(patient: Patient):
    """Creates a new patient record."""
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    # Use model_dump to get a dictionary, but exclude computed fields for storage
    data[patient.id] = patient.model_dump(exclude={'bmi', 'verdict'})
    save_data(data)
    
    # Return the full patient model, including computed fields
    return JSONResponse(status_code=201, content={"message": "Patient created successfully", "patient": patient.model_dump()})



@app.put('/update/{patient_id}')
def update_patient(patient_id:str,patient_update: PatientUpdate):
    """Updates an existing patient record."""
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Update the existing patient data with the new values
    existing_patient_info= data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value 
    existing_patient_info['id'] = patient_id 
    patient_pydantic_obj=Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')
    
    data[patient_id] = existing_patient_info
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully", "patient": patient_pydantic_obj.model_dump()}) 


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})