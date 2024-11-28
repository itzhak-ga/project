from pydantic import BaseModel
from datetime import datetime

class CustomerModel(BaseModel):
    customer_id: str
    customer_name: str

    class Config:
        from_attributes = True


class CustomerInputs(CustomerModel):
    pass


class CustomerOutputs(CustomerModel):
    id: int
    last_created: datetime
    last_modified: datetime
    user_agent: str
    endpoint_name: str
