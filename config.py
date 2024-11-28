from repository import CustomerRepo


def get_customer_repo() -> CustomerRepo:
    customer_repo = CustomerRepo.build_repo()
    try:
        yield customer_repo
    finally:
        customer_repo.close()