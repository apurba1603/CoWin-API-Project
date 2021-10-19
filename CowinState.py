import requests
from datetime import datetime

date = datetime.now()
district=[710,711,712,713,714,715,783,716,717,718,719,720,721,722,723,724,725,726,727,728,729,730,731,732,733,734,735,736,737]
global all_centers
all_centers=[]
info=""

def COWIN(dis):
    try:
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
        pr = {"district_id": dis,"date": date.strftime("%d-%m-%Y") }
        resp = requests.get(url, params=pr)
        data = resp.json()
        for i  in data['centers']:
            if i['fee_type']=='Free':
                for j in i['sessions']:
                    if j['available_capacity_dose1']!=0 and j['min_age_limit']==18:
                        
                        message="\nDate: {}\nCenter Name: {}\nDistrict: {}\nAddress: {}\nPin Code: {}\nAvailable Capacity: {}\nVaccine: {}\nDose 1: {}\nDose 2: {} \nMin. Age: {}\n".format(j['date'],i['name'],i['district_name'],i['address'],i['pincode'],j['available_capacity'],j['vaccine'],j['available_capacity_dose1'],j['available_capacity_dose2'],j['min_age_limit'])
                        
                        all_centers.append(message)
    
    except :
        print('\nFailed to establish connection\n')
        exit()
        
def CheckDistrict():
    for i in district:
        COWIN(i)
        
CheckDistrict()

if len(all_centers)==0: 
    print("\nSorry No Vaccination slot available")

else:
    for i in all_centers:
        info=info+i
        
print(info)