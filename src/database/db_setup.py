from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 데이터베이스 설정
DATABASE_URL = "sqlite:///./real_time_data.db"  # SQLite 데이터베이스 URL

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 기본 클래스 생성
Base = declarative_base()

# 데이터베이스 테이블 정의
class RealTimeData(Base):
    __tablename__ = "real_time_data"

    id = Column(Integer, primary_key=True, index=True)
    feature_a = Column(Float, nullable=False)
    feature_b = Column(Float, nullable=False)
    label = Column(String, nullable=False)

# 데이터베이스 초기화 및 테이블 생성
def init_db():
    Base.metadata.create_all(bind=engine)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 초기화 호출
if __name__ == "__main__":
    init_db()
    