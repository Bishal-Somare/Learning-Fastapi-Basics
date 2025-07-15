import pydantic
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name:Annotated[str,Field(max_length=50,title='Name of the patient',
                             description='Give the name of the patient',example=['nitesh','Amish'])]
    email:EmailStr
    linkedin_url:AnyUrl

    age: int=Field(gt=0,le=120)# greater then zero less then 120 years

    weight:Annotated[float,Field(gt=0,strict=True)] #as weight can't be negative here
    married:Annotated[bool,Field(default=None,description='adding the marriage')] # default value
    # allergies: Optional[List[str]] = Field(default=None, max_items=5)  # default value is required
    allergies:Annotated[Optional[List[str]],Field(default=None,max_items=5,description='List of allergies of the patient',
                                        example=['pollen','nuts','dust'])]
    contact_details:Dict[str,str]

    @field_validator('age', mode='before')
    def validate_age(cls, v):
        # You can add custom validation logic here if needed
        return v
 

 
def insert_patient_data(patient: Patient):
    print(patient.name) 
    print(patient.age)
    print(patient.weight)
    print(patient.allergies)
    print("inserted into database")

patient_info = {'name': 'bishal', 'email':'bishal12@gmail.com','linkedin_url':'https://linkedin.com/in/bishal','age': '30',
                'weight':100.5,'married': True,
            'contact_details':{'email':'bishal@example.com','phone':'1234567890'}}
patient1 = Patient(**patient_info)  # parses & validates data
insert_patient_data(patient1)

