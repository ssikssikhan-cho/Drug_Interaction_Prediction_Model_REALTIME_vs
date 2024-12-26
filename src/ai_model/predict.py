import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models import DataModel  # DataModel을 정의한 파일을 import
from train import train_model

# 데이터베이스 연결 설정
DATABASE_URL = "sqlite:///./test.db"  # 예시로 SQLite 사용
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def load_data_from_db():
    session = SessionLocal()
    try:
        data = session.query(DataModel).all()
        return pd.DataFrame([d.__dict__ for d in data])
    finally:
        session.close()

def load_model(model_path):
    from keras.models import load_model
    return load_model(model_path)

def preprocess_input(data):
    # 데이터 전처리 로직을 여기에 추가
    return processed_data

def make_prediction(model, input_data):
    processed_data = preprocess_input(input_data)
    prediction = model.predict(processed_data)
    return prediction

def predict():
    model, le_disease = train_model()
    data = load_data_from_db()

    # 필요한 열만 추출 (성분명, 성분코드)
    X = data[['성분명A', '성분코드A', '성분명B', '성분코드B']]

    # 예측 수행
    predictions = model.predict(X)
    data['질병_정규화_예측'] = le_disease.inverse_transform(predictions)

    # 예측 결과 출력
    print(data[['성분명A', '성분코드A', '성분명B', '성분코드B', '질병_정규화_예측']])

if __name__ == "__main__":
    predict()