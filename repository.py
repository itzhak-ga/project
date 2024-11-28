from typing import Iterable
from sqlalchemy.orm.session import Session, sessionmaker
from models import CustomerInputs, CustomerOutputs
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://itzhak:12345@localhost:5432/itzhakdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CustomerSchema(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(244), nullable=False, index=True)
    customer_name = Column(String(244), nullable=False)
    last_created = Column(DateTime, default=datetime.now)
    last_modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user_agent = Column(String, nullable=False)
    endpoint_name = Column(String, nullable=False)


class CustomerRepo:
    def __init__(self, session: Session):
        self.session = session
        self.schema = CustomerSchema

    @classmethod
    def build_repo(cls) -> 'CustomerRepo':
        session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return cls(session_maker())

    def close(self) -> None:
        self.session.close()

    def get_all(self) -> Iterable[CustomerOutputs]:
        return self.session.query(CustomerSchema).all()

    def create(self, customer: CustomerInputs, user_agent: str, endpoint_name: str) -> CustomerOutputs:
        row = self.schema(**customer.model_dump(), user_agent=user_agent, endpoint_name=endpoint_name)
        self.session.add(row)
        self.session.commit()
        return CustomerOutputs.from_orm(row)

    def get_by_name(self, customer_name: str) -> CustomerOutputs:
        return self.session.query(CustomerSchema).filter(CustomerSchema.customer_name == customer_name).first()
