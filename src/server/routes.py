from flask import Flask, request, jsonify, Blueprint
import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models import DataModel
from src.database.db_operations import insert_data, get_data
from src.ai_model.train import train_model
from src.ai_model.predict import predict

app = Flask(__name__)
bp = Blueprint('routes', __name__)

# 데이터베이스 연결 설정
DATABASE_URL = "sqlite:///./test.db"  # 예시로 SQLite 사용
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Insert data into the database
    insert_data(data)
    
    return jsonify({"message": "Data received successfully"}), 201

@bp.route('/train', methods=['POST'])
def train():
    model, le_disease = train_model()
    return jsonify({"message": "모델 훈련이 완료되었습니다."})

@bp.route('/predict', methods=['POST'])
def make_prediction():
    predictions = predict()
    return jsonify(predictions)

@bp.route('/data', methods=['POST'])
def get_real_time_data():
    session = SessionLocal()
    try:
        # 실시간 데이터 가져오기 (예시로 외부 API 호출)
        response = requests.get('https://www.data.go.kr/data/15056780/openapi.do#/API%20%EB%AA%A9%EB%A1%9D/getUsjntTabooInfoList02')
        data = response.json()

        # 데이터베이스에 저장
        for item in data:
            data_model = DataModel(
                제품명A=item['제품명A'],
                성분코드A=item['성분코드A'],
                성분명B=item['성분명B'],
                성분코드B=item['성분코드B'],
                질병_정규화=item['질병_정규화']
            )
            insert_data(session, data_model)
        
        return jsonify({"message": "실시간 데이터가 성공적으로 저장되었습니다."})
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        session.close()

@app.route('/data', methods=['GET'])
def fetch_data():
    data = get_data()
    return jsonify(data), 200

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)