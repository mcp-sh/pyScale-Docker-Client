from mysql.connector import connect, Error
import datetime
import random
import time

SCALE = 1


def logtodb(value):
    sql = """
    INSERT INTO scales (scale, timestamp, gross, net, tare) VALUES ( %s, %s, %s, %s, %s)
    """
    # vals = value['Scale'], value['Timestamp']
    # vals = 1, "2021/10/12"
    print(value)

    try:
        with connect(
            host="localhost",
            user="zsh",
            password="zshmt",
            database="mt_scale"
        ) as connection:
            # print(connection)
            with connection.cursor() as cursor:
                cursor.execute(sql, value)
                connection.commit()
    except Error as e:
        print(e)


def createEntry():
    ct = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    tare = round(random.uniform(1.0, 5.0), 2)
    net = round(random.uniform(500.0, 505.0), 2)
    gross = round((net + tare), 2)
    value = SCALE, ct, gross, net, tare

    return value


for i in range(10):
    value = createEntry()
    logtodb(value)
    randomInt = random.randint(1, 20)
    print(f"Sleeping for {randomInt} seconds")
    time.sleep(randomInt)
