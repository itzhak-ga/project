from fastapi import Depends, HTTPException, Request

from models import CustomerInputs
from repository import CustomerRepo
from functools import wraps


def get_customer_repo() -> CustomerRepo:
    customer_repo = CustomerRepo.build_repo()
    try:
        yield customer_repo
    finally:
        customer_repo.close()


def exception_handler(func):
    @wraps(func)
    def wrapper(new_customer: CustomerInputs, request: Request,
                customer_repo: CustomerRepo = Depends(get_customer_repo), *args, **kwargs):
        if customer_repo.get_by_name(new_customer.customer_name):
            raise HTTPException(status_code=400, detail="Customer with this name already exists.")
        return func(new_customer, request, customer_repo, *args, **kwargs)

    return wrapper
