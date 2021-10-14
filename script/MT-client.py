#!/usr/bin/env python3

import sys
import socket
import datetime
import csv
import re
import os.path
from mysql.connector import connect, Error

HOST = os.environ['SCALE_HOST']
PORT = int(os.environ['SCALE_PORT'])
SCALE = int(os.environ['SCALE_NUM'])

# Hard coded values for testing
# HOST = '127.0.0.1'
# PORT = 1033
# SCALE = 1

print(HOST)
print(PORT)

# Conversion factor to convert kg to pounds
KGTOPOUNDS = 2.2046

def get_ts():
    ct = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return ct

def logtodb(value):
    sql = """
    INSERT INTO scales (scale_id, date, time, gross_kg, net_kg, tare_kg, gross_lb, net_lb, tare_lb) 
    VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        with connect(
            host="db",
            user="zsh",
            password="zshmt",
            database="mt_scale"
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, value)
                connection.commit()
    except Error as e:
        print(e)


def createquery(value):
    res = SCALE, value['Date'], value['Time'], value['Gross (kg)'], value['Net (kg)'], value['Tare (kg)'], value['Gross (lb)'], value['Net (lb)'], value['Tare (lb)']
    return res


def log_to_csv(value):
    needs_header = True
    csv_columns = ['Scale', 'Date', 'Time',
                   'Gross (kg)', 'Net (kg)', 'Tare (kg)',
                   'Gross (lb)', 'Net (lb)', 'Tare (lb)' 
                   ]
    datestring = datetime.datetime.today().strftime("%Y%m%d")
    logfile = '/scaledata/log-'+datestring+'.csv'

    if os.path.isfile(logfile):
        needs_header = False
    else:
        needs_header = True

    with open(logfile, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        if needs_header:
            writer.writeheader()
        writer.writerow(value)


def remove_kg(val):
    out = val[:-3]
    return float(out)


def cleanString(input):
    lines = input.splitlines()
    try:
        lines.pop(-1)
    except IndexError:
        print('Received a malformatted message')
        sys.exit(1)
    values = []

    for line in lines:
        # Remove the beginning of the string by using RegEx replacement
        out = re.sub("^(\w+\s*\w*:\s+)", "", line)
        values.append(out)
    
    ts_item = re.split(r'\s+', values[0])
    insert_date = datetime.datetime.strptime(ts_item[1], "%d/%m/%Y").strftime("%Y-%m-%d")
    
    values_dict = {
        'Scale': SCALE,
        'Date': insert_date,
        'Time': ts_item[0],
        'Gross (kg)': remove_kg(values[1]),
        'Net (kg)': remove_kg(values[2]),
        'Tare (kg)': remove_kg(values[3]),
        'Net (lb)': round((remove_kg(values[2])*KGTOPOUNDS), 2),
        'Gross (lb)': round((remove_kg(values[1])*KGTOPOUNDS), 2),
        'Tare (lb)': round((remove_kg(values[3])*KGTOPOUNDS), 2)
    }
    return values_dict

def handle_data(msg):
    value = cleanString(msg)
    log_to_csv(value)
    sqlquery = createquery(value)
    logtodb(sqlquery)

def connect_to_scale(s):
    try:
        s.connect((HOST, PORT))
    except socket.error as e:
        print(str(e))
        sys.exit(1)
    print(f'Connected to {HOST}:{PORT}')
    res = s.recv(512)
    rstr = res.decode('utf-8')
    print(f'Received message at {get_ts()}')
    handle_data(rstr)
    match = re.search('\*{5,30}', rstr )
    if match:
        print('Message complete')
        print('Closing connection')
        s.close()

rounds = 1

while True:
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f'{get_ts()} Connecting to scale {SCALE}...')
    connect_to_scale(ClientSocket)
    rounds += 1

