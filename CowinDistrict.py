import json
import requests
from datetime import datetime
date = datetime.now()
count=0
try:
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    # pr = {"pincode": int(input("Enter Pin: ")), "date": date.strftime("%d-%m-%Y") }
    pr = {"district_id": 730,"date": date.strftime("%d-%m-%Y") }
    resp = requests.get(url, params=pr)
    data = resp.json()
    
except :
    print('Failed to establish connection')
    exit()
    
# print(data)
for i  in data['centers']:
    if i['fee_type']=='Free':
        for j in i['sessions']:
            # if j['available_capacity_dose1']!=0 and j['min_age_limit']==18 and j['vaccine']=='COVISHIELD':
            if j['available_capacity_dose2']!=0 and j['vaccine']=='COVISHIELD':
            
                print(f"Date: {j['date']} \nCenter Name: {i['name']}\nDistrict: {i['district_name']}\nAddress: {i['address']}\nPin Code: {i['pincode']}\nAvailable Capacity: {j['available_capacity']} \nVaccine: {j['vaccine']}\nDose1: {j['available_capacity_dose1']} \nDose2: {j['available_capacity_dose2']} \nMin. Age: {j['min_age_limit']}\n")
                count+=1
if count==0: print("Sorry No Vaccination slot available")