import calendar
from datetime import datetime,timedelta
m = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}
def sixty(s):
    day,month,year,hour,minute,sec = int(s[:2]),s[3:6],int(s[7:11]),int(s[12:14]),int(s[15:17]),int(s[18:20])
    d = datetime(day=day,
        month=m[month], 
        year=year
        )
    def get_key(val):
        for key, value in m.items():
            if val == value:
                return key
 
    

    due = d + timedelta(days = 60)
    return f"{due.day}/{get_key(due.month)}/{due.year}"

help_message = 'Please use these three commands before inputting the first and last name of a person for a report: "New" to store a new report. "Get" to get report information of a person. "Finish" to finish a report.'


    
    