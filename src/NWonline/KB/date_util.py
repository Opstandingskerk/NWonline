###############################################################################
# File: NWonline/KB/date_util.py
# Author: Lukas Batteau
# Description: Contains utility methods for working with dates. The standard
# Python library datetime doesn't offer much help in doing date math. 
###############################################################################
import calendar
import datetime

ONE_YEAR = datetime.timedelta(365.25)
TWELVE_YEARS = 12 * ONE_YEAR
 
def add_months(date, months):
    month = date.month - 1 + months
    year = date.year + month / 12
    month = month % 12 + 1
    day = min(date.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)
