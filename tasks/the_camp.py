import requests

from utils.time_util import kst_today
from tasks import crawler
import settings


class TheCamp:
    def __init__(self, camp_id, camp_pw):
        self.session = requests.Session()
        self.camp_id = camp_id
        self.camp_pw = camp_pw

        self.session.headers['User-Agent'] \
            = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

    def login(self):
        url = 'https://www.thecamp.or.kr/pcws/common/login.do'

        data = {
            'subsType': 1,
            'user-id': self.camp_id,
            'user-pwd': self.camp_pw,
        }

        resp = self.session.post(url, json=data)
        print(resp.status_code)

    @staticmethod
    def preprocess_content(content):
        return content

    def send_letter(self, title, message, name):
        if not title or not message:
            raise ValueError('제목, 내용이 필요합니다.')

        message = self.preprocess_content(message)
        friend_data = settings.friends.get(name)
        payload = {
            'boardId': "",
            'title': title,
            'content': f'{kst_today()}\n' + message,
            'birth': friend_data['birth'],
            'group_id': friend_data['group_id'],
            'relationship': friend_data['relationship'],
            'trainee_name': name,
            'unit_code': friend_data['unit_code'],
            'fileInfo': [],
        }
        print(title)
        print(message)

        url = 'https://www.thecamp.or.kr/pcws/message/letter/insert.do'
        resp = self.session.post(url, json=payload)
        print(resp.text)
        print(resp.status_code)


def send_letter():
    send_telegram = True if settings.TELEGRAM_TOKEN else False
    contents = {}

    weather = crawler.weather_crawler()  # 논산 날씨
    news = crawler.news_crawler()  #
    coin = crawler.coin_crawler()
    news_coin = news + '\n\n' + coin

    if weather is not None:
        contents['날씨'] = weather
    # if news is not None:
    #     contents['뉴스'] = news
    # if coin is not None:
    #     contents['코인'] = coin
    contents['소식'] = news_coin

    camp = TheCamp(settings.camp_id, settings.camp_pw)
    camp.login()

    from utils import telegram

    for key, content in contents.items():
        for name in settings.friends.keys():
            try:
                camp.send_letter(f'{kst_today()} 오늘의 {key}', content, name)
            except Exception as e:
                if send_telegram:
                    telegram.send_message(f'The Camp Error! : {key} ({str(e)})')
        if send_telegram:
            telegram.send_message(f'{kst_today()} 오늘의 {key}' + '\n' + content)


if __name__ == '__main__':
    send_letter()
