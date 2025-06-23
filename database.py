from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Setup
engine = create_engine("sqlite:///mcp.db", echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Model
class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    key = Column(String)
    value = Column(String)

# Create table if not exists
Base.metadata.create_all(engine)

# Exported function
def get_session():
    return Session()

