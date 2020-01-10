from dateutil.parser import parse as parse_date
import pytz


def str2datetime(datetime_str, tz=pytz.UTC):
    parsed_date = parse_date(datetime_str)
    if parsed_date.tzinfo:
        # Cast to UTC and possibly to something else to restore pytz tz data
        return parsed_date.astimezone(pytz.UTC).astimezone(tz)
    else:
        # If no TZ was parsed, assume was a naive datetime str and associate it with the specified tz
        return tz.localize(parsed_date)