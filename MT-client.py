#!/usr/bin/env python3

import socket
import datetime
import csv
import re
import os.path
from mysql.connector import connect, Error


# Setting the host and port number from CLI arguments
# Second parameter for port is optional

# HOST = sys.argv[1]
# if len(sys.argv) > 2:
#     PORT = int(sys.argv[2])
# else:
#     PORT = 1025        # Default port for MT IND360 controller

#
# Setting HOST and PORT from ENV variables provided through Docker Compose
#

HOST = os.environ['SCALE_HOST']
PORT = int(os.environ['SCALE_PORT'])
SCALE = int(os.environ['SCALE_NUM'])

print(HOST)
print(PORT)

# Converison factor to convert kg to pounds
KGTOPOUNDS = 2.2046


def logtodb(value):
    sql = """
    INSERT INTO scales (scale_id, timestamp, gross_kg, net_kg, tare_kg, gross_lb, net_lb, tare_lb) 
    VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)
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
    res = SCALE, value['Timestamp'], value['Gross (kg)'], value['Net (kg)'], value['Tare (kg)'], value['Gross (lb)'], value['Net (lb)'], value['Tare (lb)']
    return res


def logweight(value):
    needs_header = True
    csv_columns = ['Scale', 'Timestamp',
                   'Gross (kg)', 'Net (kg)', 'Tare (kg)', 'Gross (lb)', 'Net (lb)', 'Tare (lb)']
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
    lines.pop(-1)
    values = []

    for line in lines:
        # Remove the beginning of the string by using RegEx replacement
        out = re.sub("^(\w+\s*\w*:\s+)", "", line)
        values.append(out)
    
    values_dict = {
        'Scale': SCALE,
        'Timestamp': values[0],
        'Gross (kg)': remove_kg(values[1]),
        'Net (kg)': remove_kg(values[2]),
        'Tare (kg)': remove_kg(values[3]),
        'Net (lb)': round((remove_kg(values[2])*KGTOPOUNDS), 2),
        'Gross (lb)': round((remove_kg(values[1])*KGTOPOUNDS), 2),
        'Tare (lb)': round((remove_kg(values[3])*KGTOPOUNDS), 2)
    }
    # print(values_dict)
    return values_dict


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(1024)
        msg = data.decode('utf-8')
        value = cleanString(msg)
        print(value)
        logweight(value)
        sqlquery = createquery(value)
        logtodb(sqlquery)
