import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import DataModel  # DataModel을 정의한 파일을 import

# 데이터베이스 연결 설정
DATABASE_URL = "sqlite:///./test.db"  # 예시로 SQLite 사용
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def insert_data(session, data):
    session.add(data)
    session.commit()

def update_data(session, data_id, updated_data):
    data = session.query(DataModel).filter(DataModel.id == data_id).first()
    if data:
        for key, value in updated_data.items():
            setattr(data, key, value)
        session.commit()

def delete_data(session, data_id):
    data = session.query(DataModel).filter(DataModel.id == data_id).first()
    if data:
        session.delete(data)
        session.commit()

def get_data(session, data_id):
    return session.query(DataModel).filter(DataModel.id == data_id).first()

def get_all_data(session):
    return session.query(DataModel).all()

# 기존 데이터 삽입 예시
def add_existing_data_from_excel(file_paths):
    session = SessionLocal()
    try:
        for file_path in file_paths:
            # 엑셀 파일 읽기
            df = pd.read_csv(file_path)
            
            # 데이터베이스에 삽입
            for _, row in df.iterrows():
                data = DataModel(
                    제품명A=row['제품명A'],
                    성분코드A=row['성분코드A'],
                    제품코드A=row['제품코드A'],
                    제품명A=row['제품명A'],
                    성분명B=row['성분명B'],
                    성분코드B=row['성분코드B'],
                    제품코드B=row['제품코드B'],
                    제품명B=row['제품명B'],
                    상세_비고_병합=row['상세_비고_병합']
                )
                insert_data(session, data)
    finally:
        session.close()

if __name__ == "__main__":
    excel_file_paths = [
        "C:/Users/Eunsoo/Desktop/개인프로젝트 백업/중복제거_데이터1.csv",
        "C:/Users/Eunsoo/Desktop/개인프로젝트 백업/중복제거_데이터2.csv",
        "C:/Users/Eunsoo/Desktop/개인프로젝트 백업/중복제거_데이터3.csv"
    ]
    add_existing_data_from_excel(excel_file_paths)