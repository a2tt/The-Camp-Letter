# The Camp Letter
http://www.thecamp.or.kr/  
육군 훈련소에 있는 훈련병에게 자동으로 편지를 보냅니다.

## 설정
1. 더 캠프
    1. 자체 계정으로 가입 (소셜 계정 X)
    2. 사이트 내의 훈련소 카페 가입, 훈련병 등록
    3. 직접 편지를 쓸 수 있는 상황까지 만든다.

1. `unit_code`, `group_id` 확인
    1. 더 캠프 로그인 상태에서 https://www.thecamp.or.kr/pcws/home/viewList.do? 에 접속
    2. Ctrl + Shift + i 를 눌러서 개발자 콘솔 실행
    3. 개발자 콘솔의 Elements 탭을 클릭하고 Ctrl + F 로 찾기 실행
    4. 원하는 사람의 연대를 입력 ex. 30연대 
    5. `<a group_id="000" unit_code="0000000" school_type="1">30연대 x교육대 x중대 </a>` 이와 같은 태그를 확인하고
    이 안의 `group_id` 값과 `unit_code` 값을 저장한다.
     
1. `settings.py`
    1. `settings.sample.py`를 참고하여 `settings.py` 생성
    (텔레그램은 선택)
    1. 뉴스데이터를 가져오기 위해서 
    https://newsapi.org/ 여기에 가입하고 API key 를 생성하여
    `settings.py` 의 `NEWS_API_TOKEN` 값에 넣는다.

## 사용 방법
- 로컬에서 직접 실행하거나
- 서버에 올려 cron 으로 실행하거나  
    - 0 12 * * * /usr/bin/python3 /path/to/script/handler.py
- 만들어놓은 serverless framework 을 사용한다. 
    1. npm install serverless -g
    2. sls plugin install -n serverless-python-requirements
    3. AWS Lambda 사용시 https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html 참고
    4. sls deploy