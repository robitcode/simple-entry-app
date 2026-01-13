from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./project.db"

engine = create_engine(
    DATABASE_URL,connect_args={"check_same_thread":False}
)

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base = declarative_base()

from sqlalchemy import Column, String, Integer

class Entry(Base):
    # Table name
    __tablename__ = "entry"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String,index = True)
    surname = Column(String)
    address = Column(String)

    def __refr__(self):
        return f"[Entry Details] id: ${self.id} / name: ${self.name} / surname: ${self.address}"
    
Entry.metadata.create_all(bind = engine)