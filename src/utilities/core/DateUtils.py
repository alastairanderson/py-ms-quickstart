import time
# from calendar import timegm
from datetime import date, datetime, timedelta
import dateutil.parser as dup
from dateutil.relativedelta import relativedelta

class DateUtils:
    
    """
    date_format's => "%Y-%m-%d %H:%M", "%d/%m/%Y"
    """
    @staticmethod
    def convert_date_str_to_date(date_str_to_convert, date_format):
        return datetime.strptime(date_str_to_convert, date_format)


    @staticmethod
    def convert_date_to_date_str(date_to_convert, date_format):
        return date_to_convert.strftime(date_format)


    @staticmethod
    def add_timedelta_str_to_date(initial_date, timedelta_str):
        # the format is "Weeks, Days, Hours, Minutes, Seconds"
        td = timedelta_str.split(",")
        return initial_date + timedelta(weeks=int(td[0]), days=int(td[1]), hours=int(td[2]), minutes=int(td[3]), seconds=int(td[4]))


    @staticmethod
    def get_current_date_time():
        return datetime.now()


    @staticmethod
    def add_timedelta_to_date(date_to_delta, weeks=0, days=0, hours=0, minutes=0, seconds=0):
        return date_to_delta + timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)


    @staticmethod
    def convert_from_isoformat_str_to_datetime(isoformat_dt_str):
        return dup.parse(isoformat_dt_str)


    @staticmethod
    def convert_date_to_isoformat_str(dt):
        if isinstance(dt, str):
            print("Warning: {0} is a string".format(dt))
            return dt
        return dt.isoformat()


    @staticmethod
    def get_last_day_of_previous_month(date_to_use):
        return date(date_to_use.year, date_to_use.month, 1) - relativedelta(days=1)


    @staticmethod
    def get_first_date_of_next_month(date_to_use):
        return date(date_to_use.year, date_to_use.month, 1) + relativedelta(months=1)


    @staticmethod
    def extract_MMMM_from_date(datetime1):
        return datetime1.strftime("%B")


    @staticmethod
    def difference_in_seconds(first_date, second_date):
        return (second_date-first_date).total_seconds()


    @staticmethod
    def set_specific_time(initial_date, hour_of_date=0, minute_of_date=0, second_of_date=0, microsecond_of_date=0):
        return initial_date.replace(hour=hour_of_date, minute=minute_of_date, second=second_of_date, microsecond=microsecond_of_date)