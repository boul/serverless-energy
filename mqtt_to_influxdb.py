import time
import requests
import os

current_time = int(time.time())
# username = 'lambda'
# password = 'L@MBD@!!!'
# database = 'test'
username = os.environ['INFLUXDB_USER']
password = os.environ['INFLUXDB_PASS']


def add_influx_datapoint(db, key, value, tag, user, password):

    if type(value) is int or type(value) is float:
        data = str(key) + ",type="+tag + " value=" + str(value)
        url = 'https://influx-api.boul.nl/write?db='+db

        print(data)
        r = requests.post(url, data=data, auth=(user, password))
        response = r.text
        print(response)


def add_influx_multipoint(db, data, tag, user, password):

    multipoint = ''
    url = 'https://influx-api.boul.nl/write?db=' + db

    for k, v in data.items():
        if type(v) is int or type(v) is float:

            multipoint = multipoint + "\n" + str(k) + ",type="+tag + " value=" + str(v)

    print(multipoint)
    r = requests.post(url, data=multipoint, auth=(user, password))
    response = r.text
    status = r.status_code
    print(response)
    print(status)


def p1(event, context):
    print(event)

    add_influx_multipoint('energy-p1', event, 'p1', username, password)
    #
    # for k, v in event.items():
    #
    #     if v is not None:
    #
    #         add_influx_datapoint(database, k, v, 'p1', username, password)

    return


def pv(event, context):
    print(event)

    add_influx_multipoint('energy-pv', event, 'pv', username, password)

    # for k, v in event.items():
    #
    #     if v is not None:
    #
    #         add_influx_datapoint(database, k, v, 'pv', username, password)

    return


def atag(event, context):
    print(event)

    status = event['status']
    add_influx_multipoint('energy-atag', status,'atag-status', username, password)

    report = event['report']
    add_influx_multipoint('energy-atag', report, 'atag-report', username, password)

    report_details = event['report']['details']
    add_influx_multipoint('energy-atag', report_details, 'atag-report-details', username, password)

    configuration = event['configuration']
    add_influx_multipoint('energy-atag', configuration, 'atag-configuration', username, password)

    return
