# real-time-ai-project/real-time-ai-project/README.md
# Real-Time AI Project
## 설치 및 실행

1. **환경 설정**: `.env` 파일을 수정하여 데이터베이스 연결 문자열 및 API 키를 설정
2. **의존성 설치**: 다음 명령어를 사용하여 필요한 패키지를 설치
   ```
   pip install -r requirements.txt
   ```
3. **Docker 실행**: Docker를 사용하여 프로젝트를 실행하려면 다음 명령어를 사용
   ```
   docker-compose up --build
   ```

## 사용법

- 서버가 실행되면 API 엔드포인트를 통해 실시간 데이터를 수신할 수 있습니다.
- `/train` 엔드포인트를 호출하여 AI 모델을 훈련시킬 수 있습니다.
- `/predict` 엔드포인트를 사용하여 훈련된 모델로 예측을 수행할 수 있습니다.