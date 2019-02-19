from datetime import timedelta, tzinfo, datetime


class GMT3(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=3)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "Europe/Russia"


def get_current_time():
    dt = datetime.now(GMT3())
    return dt.strftime("%Y-%m-%d %H:%M:%S")
