import requests
from lxml import etree
from urllib.parse import urlencode
from datetime import datetime

def get_instant_booking_url():
    return 'https://app.wayleadr.com/companies/uber/offices/1455-3rd-street-san-francisco-ca/request/new?instant_booking=true'

def get_booking_request():
    return 'https://app.wayleadr.com/companies/uber/offices/1455-3rd-street-san-francisco-ca/request'

def get_cookie():
    with open('cookie.txt', 'r') as f:
        cookie = f.readline()
    cookies_dict = {str.strip(i.split('=')[0].strip()): str.strip(i.split('=')[1].strip()) for i in cookie.split('; ')}
    return cookies_dict

def get_header():
    return {'Content-Type': 'application/x-www-form-urlencoded'}

def construct_date():
    with open('date.txt', 'r') as f:
        date = f.readline()
    date = date.strip()
    dateArray = date.split('/')
    return date, dateArray[2] + '-' + dateArray[0] + '-' + dateArray[1]

def get_request_data(resp):
    html1 = etree.HTML(resp)
    token = html1.xpath('//meta[@name="csrf-token"]/@content')[0]

    date = construct_date()
    return {'authenticity_token': token,
            'booking_request[date_range]':date[0],
            'booking_request[start_time]':date[1] + ' 01:00:00 -0700',
            'booking_request[end_time]':date[1] + ' 23:30:00 -0700',
            'booking_request[preferred_zone_id]':'1499',
            'booking_request[vehicle_plate]': '9EFH512',
            'booking_request[instant_booking]':'true',
            'booking_request[booking_request_method]':'instant',
            'commit': 'Book Now!',
            'for_user': ''}


first_response = requests.get(get_instant_booking_url(),cookies=get_cookie(), headers=get_header())
second_response = requests.post(get_booking_request(), cookies=get_cookie(), headers = get_header())
third_response = requests.post(get_booking_request(), cookies=get_cookie(), headers=get_header(), data=urlencode(get_request_data(second_response.text)))
