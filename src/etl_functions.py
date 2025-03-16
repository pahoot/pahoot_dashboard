from settings import *
import csv
from datetime import datetime, timedelta

def load_month_data(csv_path):
    '''Loads month data from a csv where first column in Person_id. Also adds a metadata field capturing the month.'''
    data = {}
    with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            key = row[0].strip()
            values = [int(value) if value.isdigit() else 0 for value in row[1:]]
            data[key] = values
        month = csv_path.split('/')[1].split('.')[0].split('_')[1]
    return data, month

def bounds_generator(month,year):
    '''Picks the proper start_date and end_date for each month in Catalan'''
    if month == 'gener':
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 1, 31)
    elif month == 'febrer':
        if year == 2024: feb_len = 29
        else: feb_len = 28
        start_date = datetime(year, 2, 1)
        end_date = datetime(year, 2, feb_len)
    elif month == 'marc':
        start_date = datetime(year, 3, 1)
        end_date = datetime(year, 3, 31)
    elif month == 'abril':
        start_date = datetime(year, 4, 1)
        end_date = datetime(year, 4, 30)
    elif month == 'maig':
        start_date = datetime(year, 5, 1)
        end_date = datetime(year, 5, 31)
    elif month == 'juny':
        start_date = datetime(year, 6, 1)
        end_date = datetime(year, 6, 30)
    elif month == 'juliol':
        start_date = datetime(year, 7, 1)
        end_date = datetime(year, 7, 31)
    elif month == 'agost':
        start_date = datetime(year, 8, 1)
        end_date = datetime(year, 8, 31)
    elif month == 'setembre':
        start_date = datetime(year, 9, 1)
        end_date = datetime(year, 9, 30)
    elif month == 'octubre':
        start_date = datetime(year, 10, 1)
        end_date = datetime(year, 10, 31)
    elif month == 'novembre':
        start_date = datetime(year, 11, 1)
        end_date = datetime(year, 11, 30)
    elif month == 'desembre':
        start_date = datetime(year, 12, 1)
        end_date = datetime(year, 12, 31)
    else:
        raise ValueError(f"Invalid month name: {month}")
    return start_date,end_date

def generate_dates(month,year):
    '''Generates dates one by one in function of the month and year provided'''
    start_date,end_date = bounds_generator(month,year)
    delta = timedelta(days=1)
    current_date = start_date
    while current_date <= end_date:
        yield current_date.strftime('%Y-%m-%d')
        current_date += delta

def get_weekday(date_str):
    '''Gets the weekday from a date in string format YYYY-MM-DD'''
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    # Get the weekday as an integer (0 for Monday, 1 for Tuesday, ..., 6 for Sunday)
    weekday_num = date_obj.weekday()
    # Convert the integer weekday to the name of the weekday
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_name = weekdays[weekday_num]
    
    return weekday_name
