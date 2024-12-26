from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RealTimeData(Base):
    __tablename__ = 'real_time_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    feature_a = Column(Float, nullable=False)
    feature_b = Column(Float, nullable=False)
    label = Column(String, nullable=False)

class ModelTraining(Base):
    __tablename__ = 'model_training'

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String, nullable=False)
    training_date = Column(String, nullable=False)
    accuracy = Column(Float, nullable=False)

    