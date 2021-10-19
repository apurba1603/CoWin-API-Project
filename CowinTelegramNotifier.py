""" I've used CoWin API to fetch district wise vaccination slots
availability """

#------------------------------------------

#############  Modules  #############
# pip install requests
# pip install schedule
# pip install pytz
# pip install python-telegram-bot

import requests
from datetime import datetime
import schedule
import time
from pytz import timezone
import telegram
from telegram.ext import *

#------------------------------------------        
all_centers=[]
prev_centers=[]
centers_id=[]

#------------------------------------------
def COWIN():
    district_list=[720,721,725,730,728,732]

    try:
        
        for district in district_list:
            timeNow = datetime.now(timezone('Asia/Kolkata'))
            url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
            params = {"district_id": district,"date": timeNow.strftime("%d-%m-%Y") }
            resp = requests.get(url, params=params)
            data = resp.json()
            print(resp)
            for i  in data['centers']:
                if i['fee_type']=='Free':
                    for j in i['sessions']:
                        if j['available_capacity_dose1']!=0 and j['min_age_limit']==18:
                            global centers_id
                            CenterIdDate="{}{}".format(i['center_id'],j['date'])
                            centers_id.append(CenterIdDate)
                            message=message="\n<strong>District: {}\nDate: {}\nCenter Name: {}\nMunicipality: {}</strong>\nAddress: {}\nPin Code: {}\nAvailable Capacity: {}\nVaccine: {}\nDose 1: {}\nDose 2: {} \nMin. Age: {}\n".format(i['district_name'],j['date'],i['name'],i['block_name'],i['address'],i['pincode'],j['available_capacity'],j['vaccine'],j['available_capacity_dose1'],j['available_capacity_dose2'],j['min_age_limit'])
                            global all_centers
                            all_centers.append(message)

    except Exception as e:
        
        print('\nFailed to establish connection\n')
        print(e)

#------------------------------------------        
def auto():

    token='xxxxxxxxxxxxxx'  #unique authentication token to authorize the bot 
    chat_id='xxxxxxxxx'   #it is a unique id for every user and group chat, this chat id is the group id where i want to send the notifications.
    
        
    global prev_centers,centers_id,all_centers
    COWIN()
    
    info=""
    n=0
    #------------------------------------------ 
    # Eleminating the redundant centers of two successive request
    if len(all_centers)!=0:
        for centers in all_centers:
            if centers_id[n] not in prev_centers:
                info=info+str(centers)
            n+=1

    #------------------------------------------ 
    if info!="":       
        url= '\n<strong>Book Appointment On CoWIN</strong>\nhttps://selfregistration.cowin.gov.in/'
    
        try:
            format="%H:%M:%S"
            timestamp = datetime.now(timezone('Asia/Kolkata'))
            params=timestamp.strftime(format)
            bot = telegram.Bot(token)
            bot.sendMessage(chat_id, info+url, parse_mode='html')
           
        except Exception as e: 
            
            print('\nTelegram Failed to establish connection\n')
            print(e)

#------------------------------------------              
     
    prev_centers=[]
    prev_centers=centers_id
    all_centers=[]
    centers_id=[]

#------------------------------------------

#scheduling the program to run in a specific interval
schedule.every(.1).minutes.do(auto)
while True:
    schedule.run_pending()
    time.sleep(1)
#------------------------------------------