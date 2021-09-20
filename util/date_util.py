from tzlocal import get_localzone
from datetime import  datetime
import pytz

FORMAT_DATE = '%d/%m/%Y %H:%M:%S'

def get_datetime():
    now = datetime.now()
    return datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0, microsecond=0)


def get_date_timezone(date):
    return datetime(year=date.year, month=date.month,
                    day=date.day,
                    hour=date.hour, minute=date.minute,
                    second=date.second, tzinfo=pytz.utc).astimezone(get_localzone())

