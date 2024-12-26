import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models import DataModel  # DataModel을 정의한 파일을 import

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

def train_model():
    data = load_data_from_db()

    # 필요한 열만 추출 (성분명, 성분코드, 질병_정규화)
    data = data[['성분명A', '성분코드A', '성분명B', '성분코드B', '질병_정규화']]

    # 레이블 인코딩 (성분명과 성분코드 범주형 데이터 수치화)
    le_name_a = LabelEncoder()
    le_name_b = LabelEncoder()
    le_code_a = LabelEncoder()
    le_code_b = LabelEncoder()
    le_disease = LabelEncoder()

    # 각 성분명과 성분코드에 대해 별도의 인코딩
    data['성분명A'] = le_name_a.fit_transform(data['성분명A'])
    data['성분코드A'] = le_code_a.fit_transform(data['성분코드A'])
    data['성분명B'] = le_name_b.fit_transform(data['성분명B'])
    data['성분코드B'] = le_code_b.fit_transform(data['성분코드B'])
    data['질병_정규화'] = le_disease.fit_transform(data['질병_정규화'])

    # 입력(X)와 출력(y) 데이터 설정
    X = data[['성분명A', '성분코드A', '성분명B', '성분코드B']]
    y = data['질병_정규화']

    # 데이터셋 분리 (훈련, 테스트 세트)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # SMOTE 적용 (소수 클래스 증강, k_neighbors 값 설정)
    smote = SMOTE(random_state=42, k_neighbors=1)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

    # GridSearchCV를 사용하여 Random Forest의 최적의 하이퍼파라미터 탐색
    param_grid = {
        'n_estimators': [100, 200, 300],  # 하이퍼파라미터 범위 설정
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5, 10]
    }

    grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(X_train_resampled, y_train_resampled)

    # 최적의 모델 저장
    best_model = grid_search.best_estimator_
    return best_model, le_disease

if __name__ == "__main__":
    model, le_disease = train_model()
    print("모델 훈련이 완료되었습니다.")
    