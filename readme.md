# The Camp Letter
**이 코드는 2019년 10월 29일에 정상 작동을 확인하엿습니다.**  
이후의 작동은 보장하지 못합니다.

http://www.thecamp.or.kr/  
육군 훈련소에 있는 훈련병에게 자동으로 편지를 보냅니다.  


## 편지 예시
![sample](https://user-images.githubusercontent.com/48249622/54866992-b5290480-4dbe-11e9-96e1-2e6a65a2ce1b.PNG)

친구가 수료했기 때문에, 이전에 보냈던 인터넷편지를 캡쳐할 수 없네요. 

## 설정
1. 더 캠프
    1. 자체 이메일 계정으로 가입 (소셜 계정 X)
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
    (텔레그램은 필수 아님)
        - `훈련병이름`은 실제 이름으로 바꿔주고, `unit_code`, `group_id`는 위에서 확인한 값을 넣는다. 
    1. 뉴스데이터를 가져오기 위해서 
    https://newsapi.org/ 여기에 가입하고 API key 를 생성하여
    `settings.py` 의 `NEWS_API_TOKEN` 값에 넣는다.

## 사용 방법
- 로컬에서 직접 실행하거나
- 서버에 올려 cron 으로 실행하거나  
    1. pip install -r requirements.txt
    1.  0 12 * * * /usr/bin/python3 /path/to/script/handler.py
- 만들어 놓은 AWS Lambda + `serverless` framework 을 사용한다.
    1. npm install serverless -g
    1. sls plugin install -n serverless-python-requirements
    1. `https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html`를 참고하여
    운영체제에 맞게 credentials 설정, IAM user role 설정(아래 참고)
    1. sls deploy
    > AWS Lambda 는 한 달에 백 만 번 호출이 무료입니다.
    ##### IAM user role 설정 참고
    - CloudWatchFullAccess
    - AmazonS3FullAccess
    - AWSLambdaFullAccess
    - AmazonVPCFullAccess
    - 추가 (inline policy)
        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "cloudformation:CreateStack",
                        "cloudformation:CreateChangeSet",
                        "cloudformation:ListStacks",
                        "cloudformation:UpdateStack",
                        "cloudformation:DescribeChangeSet",
                        "cloudformation:ExecuteChangeSet",
                        "cloudformation:DescribeStackEvents",
                        "cloudformation:DescribeStackResource",
                        "cloudformation:ValidateTemplate"
                    ],
                    "Resource": [
                        "*"
                    ]
                }
            ]
        }
        ```

## 주의?
- 수료 후에는 서버를 종료합시다.
- 2019년 10월 29일에 정상 작동을 확인했습니다. 이후에는 그렇지 않을 수도 있습니다.
- 네이버는 네이버날씨 크롤링을 금하고 있습니다. `https://weather.naver.com/robots.txt`
- 네이버날씨 페이지 구조, 업빗 API 명세, newsapi API 명세의 변경이 있으면 작동하지 않을 수 있습니다.  
- 직접 쓴 편지도 보내주세요. 바깥 소식도 좋지만 사랑하는 사람들과 주변 사람들의 소식을 들으면 기분이 아주 좋습니다.
