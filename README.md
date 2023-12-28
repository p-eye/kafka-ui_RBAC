
## 개발 배경
- 현재 kafka-ui를 쿠버네티스 환경에서 Helm으로 설치해서 사용 중입니다.
- kafka-ui RABC 설정은 Helm Chart를 수정하는 방식이기에 권한 관리가 간단하지 않았습니다.
- 용이한 권한 관리를 위해 웹 UI로 권한을 제어하는 어플리케이션을 개발했습니다. (with Streamlit)
- EKS, Google OAuth 기준으로 동작 확인했습니다.


## 동작 방식
- kafka-ui의 RBAC가 설정된 ConfigMap를 수정하고, 앱 Redeploy로 변경된 설정을 반영합니다.


## 주요 기능
- Role 생성, 수정, 삭제
- Role에 유저 추가, 제외
- 유저 삭제
- 구글 로그인 및 접근 제어 적용


## 설치 방법
- ```git clone https://github.com/eunpk/kafka-ui_RBAC.git```
- config 디렉토리에 설정 파일 추가
    - credentials: EKS 접근 key, secret
    - secret.toml: kafka-ui 배포 정보, 구글 로그인 및 접근 제어를 위한 oauth, db 정보
    - kubeconfig: ~/.kube/config 파일
 
- ```docker-compose up -d```
- localhost:8501 접속
