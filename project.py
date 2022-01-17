#Casey project code
import re,calendar,keyboard
from datetime import datetime,timedelta


#globals
active = True
t = datetime.today()
year = t.year
month = t.month 
day = t.day
today = datetime(year,month,day)
info = {
    'firstName': '',
    'lastName':'',
    'ReportDate':[],
    60:[],
    45:[],
    30:[],
    15:[],
    'meeting':[]
}

"""functions""" 
# for all calculated days from date received 
#60 days
def receivedSix(d):
    new = d + timedelta(60)
    info[60] = new
    return new
#45 days
def receivedFour(d):
    new = d + timedelta(45)
    info[45] = new
    return new
#30 days
def receivedThree(d):
    new = d + timedelta(30)
    info[30] = new
    return new
#15 days
def receivedFive(d):
    new = d + timedelta(15)
    info[15] = new
    return new
#used for intervals for corresponding days 
def pause(d):
    while True:
        r = input(f'You have {d} day(s) left would you like to submit your finalized report date? Type Y for yes and N for no: ')
        if r.capitalize() == 'N':
            break
        if r.capitalize() == 'Y':
            info['meeting'] = today+timedelta(30)
            print(f'{today + timedelta(30)} is 30 days from today to set a meeting')
            
        else:
            print('Sorry that is not an accepted answer, please try again.')    
        break

while active:
    right = True
    while right:
        #saves student name in variable
        studentName = input("Please input the student's first and last name: ")

        #varies full names
        if ' ' in studentName:
            right = False
        else: 
            print("Please input the student's first and last name seperated with a space")
    
    #splits students first and last name 
    info['firstName'], info['lastName'] = studentName.split(' ')
    
    #Ask for date
    inputDate = input("Enter the date you received the report seperated with '-' ie. 'year-month-day': ")
    
    
    #escape all other symbols but the numbered dates and put them in the corresponding variables
    year, month, day = re.split("[\D']+",inputDate)
    
    #checkes that date is possible and the format is correct
    if int(day) <= 31 and int(month)<=12 and int(year) > 1999 and int(year) <2100 and '-' in inputDate:
        #format
        info['ReportDate'] = datetime(int(year),int(month),int(day))
        #exits out of both loops
        active = False
        right = False
        
    else:
        #if not correct continues to ask for the right format and possible dates
        print('Sorry that is either not a correct date, or not in the correct format please make sure you have the "-" and formated as follows; "day-month-year')


#this is 45 days out, 15 days into the count
while True:                 
    if info['reportDate']+timedelta(15) == receivedFive(info['reportDate']): 
        pause(45) 
        break
    if info['reportDate']+timedelta(30) == receivedFive(info['reportDate']): 
        pause(30) 
        break
    if info['reportDate']+timedelta(45) == receivedFive(info['reportDate']): 
        pause(15) 
        break
    

    
print(info)

    
    
    




