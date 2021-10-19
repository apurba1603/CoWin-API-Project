import requests
from datetime import datetime
import schedule
import time
import smtplib
from email.message import EmailMessage
import pywhatkit

date = datetime.now()

all_centers=[]
prev_centers=[]
centers_id=[]

def COWIN():
    district_list=[730]
    try:
        for district in district_list:
            url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
            pr = {"district_id": district,"date": date.strftime("%d-%m-%Y") }
            resp = requests.get(url, params=pr)
            data = resp.json()
            for i  in data['centers']:
                if i['fee_type']=='Free':
                    for j in i['sessions']:
                        if j['available_capacity_dose1']!=0 and j['min_age_limit']==18:
                            global centers_id
                            CenterIdDate="{}{}".format(i['center_id'],j['date'])
                            centers_id.append(CenterIdDate)
                            message="\n*Date: {}*\n*Center Name: {}*\n*District: {}*\nAddress: {}\nPin Code: {}\nAvailable Capacity: {}\nVaccine: {}\nDose 1: {}\nDose 2: {} \nMin. Age: {}\n".format(j['date'],i['name'],i['district_name'],i['address'],i['pincode'],j['available_capacity'],j['vaccine'],j['available_capacity_dose1'],j['available_capacity_dose2'],j['min_age_limit'])
                            global all_centers
                            all_centers.append(message)
    
    except :
        print('\nFailed to establish connection\n')
        exit()
        
def auto():
    global prev_centers,centers_id,all_centers
    COWIN()
    
    info=""
    p="*"
    n=0
    if len(all_centers)!=0:
        for centers in all_centers:
            if centers_id[n] not in prev_centers:
                info=info+str(centers)
            n+=1
    if info!="":
        date = datetime.now()
        now=date.strftime("%H:%M:%S")        
        # print(at,info,"\n",p*70)
        hh=date.strftime("%H")
        mm=date.strftime("%M")
        url= '*Book Appointment On CoWIN*\nhttps://selfregistration.cowin.gov.in/'
        
        try:
            pywhatkit.sendwhatmsg('+91xxxxxxxxxx',str(now+info+url),int(hh),(int(mm)+1))
        
        except:
            print('\nFailed to establish connection\n')
        
        
    prev_centers=[]
    prev_centers=centers_id
    all_centers=[]
    centers_id=[]


schedule.every(.01).minutes.do(auto)
while True:
    schedule.run_pending()
    time.sleep(1)