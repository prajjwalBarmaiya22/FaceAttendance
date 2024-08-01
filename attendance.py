import pandas as pd
import os
import csv
from datetime import datetime

def attendence():
    df = pd.read_excel('NEW TIME TABLE.xlsx')
    columns_to_fill = ['FOURTH PERIOD', 'SIXTH PERIOD']
    df[columns_to_fill] = df[columns_to_fill].fillna(value='')
    dic = {
        'FIRST PERIOD': '10:00:00 AM - 11:00:00 AM',
        'SECOND PERIOD': '11:00:00 AM - 12:00:00 PM',
        'THIRD PERIOD': '12:00:00 PM - 01:00:00 PM',
        'FOURTH PERIOD': '02:00:00 PM - 03:00:00 PM',
        'FIFTH PERIOD': '03:00:00 PM - 04:00:00 PM',
        'SIXTH PERIOD': '04:15:00 PM - 05:15:00 PM'
    }
    day = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4
    }
    current_time_str = datetime.now().strftime("%I:%M:%S %p")
    current_time = datetime.strptime(current_time_str, "%I:%M:%S %p").time()
    current_datetime = datetime.now()
    current_day = current_datetime.strftime("%A")
    if current_day in day:
        x = day[current_day]
    colunm = {'FIRST PERIOD': 1, 'SECOND PERIOD': 2, 'THIRD PERIOD': 3, 'FOURTH PERIOD': 4, 'FIFTH PERIOD': 5, 'SIXTH PERIOD': 6}
    for key, value in dic.items():
        start_time_str, end_time_str = value.split(' - ')
        start_time = datetime.strptime(start_time_str, "%I:%M:%S %p").time()
        end_time = datetime.strptime(end_time_str, "%I:%M:%S %p").time()
        if start_time <= current_time <= end_time:
            if key in colunm:
                y = colunm[key]
            return df.iloc[x, y]

def update_attendance_csv(scholar_number, subject):
    filename = f'C:/Users/barma/PycharmProjects/FaceAttendancestudent_csv/{scholar_number}.csv'
    if not os.path.exists(filename):
        create_student_csv(scholar_number, [subject])
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    marked = False
    for row in rows:
        if row['Subject Name'] == subject and row['Attendence'] == '1':
            marked = True
            break
    if not marked:
        for row in rows:
            if row['Subject Name'] == subject:
                row['Attendence'] = '1'
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Subject Name', 'Attendence']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

def create_student_csv(scholar_number):
    filename = f'C:/Users/barma/PycharmProjects/FaceAttendancestudent_csv/{scholar_number}.csv'
    subjects = ['Data Science', 'AI', 'CN', 'Statistical Modeling', 'Compiler Design', 'OS','CN LAB','OS LAB','COMPILER LAB']
    try:
        if not os.path.exists(filename):
            with open(filename, mode='w', newline='') as csvfile:
                fieldnames = ['Subject Name', 'Attendence']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for subject in subjects:
                    writer.writerow({'Subject Name': subject, 'Attendence': 0})
    except Exception as e:
        print(f"Error creating CSV file for scholar {scholar_number}: {str(e)}")