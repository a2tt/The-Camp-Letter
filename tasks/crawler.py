import requests
import re

from bs4 import BeautifulSoup

from utils.time_util import *

import settings


today = kst_today()
tomorrow = today + datetime.timedelta(days=1)
days = [f'오늘({today.month}/{today.day})', f'내일({tomorrow.month}/{tomorrow.day})']


def coin_crawler():
    try:
        target_symbols = {'BTC': '비트코인',
                          'BCH': '비트코인캐시',
                          'ETH': '이더리움',
                          'ETC': '이더리움클래식',
                          'XRP': '리플',
                          'TRX': '트론',
                          'BSV': '비트코인에스브이',
                          'EOS': '이오스',
                          'ADA': '에이다',
                          'XLM': '스텔라루멘',
                          'ADT': '애드토큰',
                          'SNT': '스테이터스네트워크토큰',
                          'ZIL': '질리카',
                          'STORM': '스톰',
                          'QTUM': '퀀텀',
                          'ELF': '엘프',
                          'ARK': '아크',
                          'LTC': '라이트코인',
                          'XMR': '모네로',
                          }
        symbols = ','.join(list(map(lambda v: 'KRW-' + v, target_symbols.keys())))
        datas = {}
        params = {'markets': symbols}
        url = 'https://api.upbit.com/v1/ticker'
        resp = requests.get(url, params=params)
        print(resp)
        if resp.status_code != 200:
            return

        resp = resp.json()
        for data in resp:
            symbol = data['market'][4:]
            price = data['trade_price']
            price = int(price) if int(price) == price else price
            change = round(data['change_rate'] * 100, 2)
            datas[symbol] = f'{price} ({change}%) _ {target_symbols[symbol]}'

        content = '\n'.join(list(map(lambda d: f'{d[0].upper()} : {d[1]}', datas.items())))
        return content
    except Exception as e:
        print('coin : ', e)
        return ''


def news_crawler():
    try:
        params = {'country': 'kr',
                  'apiKey': settings.NEWS_API_TOKEN}
        url = 'https://newsapi.org/v2/top-headlines'
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            return None
        articles = resp.json()['articles']
        titles = map(lambda d: d.get('title', ''), articles)  # 제목만 가져온다.
        titles = list(map(lambda t: t[:t.rfind('-')], titles))  # 신문사 이름 제거

        contents = []
        for idx, title in enumerate(titles):
            contents.append(f"{idx+1}) {title}")  # 번호 넣기

        return '\n'.join(contents)
    except Exception as e:
        print('news : ', e)
        return ''


def _weather_crawler():
    url = 'https://weather.naver.com/rgn/cityWetrCity.nhn?cityRgnCd=CT006003'  # 논산 날씨
    resp = requests.get(url)
    bs = BeautifulSoup(resp.text, 'lxml')

    contents = ''

    weather_table = bs.find_all('table', {'class': 'tbl_weather'})
    # 오늘, 내일
    first = weather_table[0]
    tds = first.find('tbody').find_all('td')
    for idx, td in enumerate(tds):
        text = td.get_text().strip()
        text = re.sub('\n{2,}', '\n', text)
        contents += f'** {days[idx]}\n{text}\n----------\n'

    # 모래부터 5일
    second = weather_table[1]
    trs = second.find('tbody').find_all('tr')
    for tr in trs:
        day = '** ' + tr.find('th').get_text().strip()
        cells = tr.find_all('div', {'class': 'cell'})
        cell_1 = cells[0]
        cell_2 = cells[1]
        cell_1 = re.sub('\n+', ' / ', cell_1.get_text().strip())
        cell_2 = re.sub('\n+', ' / ', cell_2.get_text().strip())
        contents += f'{day}\n{cell_1}\n{cell_2}\n----------\n'
    return contents


def weather_crawler():
    try:
        return _weather_crawler()
    except Exception as e:
        print('weather : ', e)
        return ''
