import pytz
import datetime

UTC = pytz.UTC
KOR = pytz.timezone('Etc/GMT-9')


def utc_to_kor(dt):
    # UTC 시간을 KOR 기준으로 바꿔준다.
    return UTC.localize(dt).astimezone(KOR).replace(tzinfo=None)


def kst_dt_now():
    utc_dt = datetime.datetime.utcnow()
    kst_dt = utc_to_kor(utc_dt)
    return kst_dt


def kst_today():
    dt = kst_dt_now()
    return dt.date()
