from typing import Iterable

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request, APIRouter
from config import get_customer_repo
from models import CustomerInputs, CustomerOutputs
from repository import CustomerRepo
from celery_app import my_task

app = FastAPI()
router = APIRouter(prefix="/customers", tags=['customers'])



@router.get("/all", response_model=Iterable[CustomerOutputs])
def get_customers(customer_repo: CustomerRepo = Depends(get_customer_repo)):
    return customer_repo.get_all()


@router.post("/create", response_model=CustomerOutputs)
def create_customer(new_customer: CustomerInputs, request: Request,
                 customer_repo: CustomerRepo = Depends(get_customer_repo)):
    if customer_repo.get_by_name(new_customer.customer_name):
        raise HTTPException(status_code=400, detail="Customer with this name already exists.")

    customer_created = customer_repo.create(new_customer, user_agent=request.headers.get("user-agent"),
                                            endpoint_name=create_customer.__name__)

    task_id = my_task.delay(new_customer.customer_name)
    print(f"Task ID {task_id}")
    return customer_created


app.include_router(router)

if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
