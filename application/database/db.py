from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column,Integer,String

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True, autoincrement=True)
    name = Column(String(25),nullable=False)
    email = Column(String(50),unique=True,nullable=False)
    password = Column(String(100),nullable=False)
    department = Column(String(50),nullable=False)


###db connection
engine = create_engine("sqlite:///C:/Users/sanoj/rbac_chatbot/database/rbac2.db")
Session = sessionmaker(bind=engine)


Base.metadata.create_all(engine)