from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated
class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the patient',
                               description='Give the name of the patient', example=['nitesh', 'Amish'])]
    email: EmailStr
    linkedin_url: AnyUrl

    age: int = Field(gt=0, le=120)  # greater than zero less than 120 years

    weight: Annotated[float, Field(gt=0, strict=True)]  # as weight can't be negative here
    married: Annotated[Optional[bool], Field(default=None, description='adding the marriage')]  # default value
    allergies: Annotated[Optional[List[str]], Field(default=None, max_items=5,
                                                    description='List of allergies of the patient',
                                                    example=['pollen', 'nuts', 'dust'])]
    contact_details: Dict[str, str]

    @field_validator('age', mode='before')
    def validate_age(cls, v):
        # You can add custom validation logic here if needed
        return v        
    