import requests
import time
from datetime import datetime

pincode = input("Please input your pin: ")
date = time.strftime("%d-%m-%Y", time.localtime())
url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'
qs = {"pincode": pincode, "date": date}
headers = {"Accept-Language": "hi_In"}
response = requests.request("GET", url, headers=headers, params=qs)
data = response.json()
for i in data['centers']:
    if i['fee_type'] == 'Paid':
        fee = i['vaccine_fees'][0]['fee']
    else:
        fee = '0'
    print(f"\nCenter:{i['name']}\nAddress:{i['address']} {i['block_name']}\nVaccine Type:{i['fee_type']}\nPrice:{fee}\n---------------")

    for j in i['sessions']:
        print(f"Date:{j['date']}\nVaccine Name:{j['vaccine']}\nAvailable Capacity:{j['available_capacity']}\nAge:{j['min_age_limit']}\nDose 1:{j['available_capacity_dose1']}\nDose 2:{j['available_capacity_dose2']}")
    print('---------------\n')
