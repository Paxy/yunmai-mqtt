#!/usr/bin/env python3
from bluepy.btle import Scanner, DefaultDelegate, Peripheral
from YunmailLib import YunmaiLib
from time import sleep
import paho.mqtt.client as mqtt

mac="0C:B2:B7:17:D1:F0"
sex=1 #1=Male, 2=Female
height=183
veryActive= True
age=35
mqttServer="172.16.2.1"
mqttPrefix="paxyhome"

client = mqtt.Client()

class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        if(len(data) < 20): 
            return
        #print("    Data {} size {}".format(data.hex(),len(data)))
        self.processData(data)
        
    def processData(self,data):
        data=data.hex()
        weight=int((data[26:28] + data[28:30]), 16) * 0.01
        resistance=int((data[30:32] + data[32:34]), 16)
        fat=int((data[34:36] + data[36:38]), 16) * 0.01
        #print (fat)

        if(resistance==0):
              client.publish('{}/yunmai/weight'.format(mqttPrefix), round(weight,1))
              print('{"weight":',round(weight,1),', "fat":',round(fat),' , "muscle":',round(muscle),', "water":',round(water),', "boneMass":',round(boneMass),', "skeletalMuscle":',round(skeletalMuscle),', "leanBodyMass":',round(leanBodyMass),', "visceralFat":',round(visceralFat),' }')
              return
    
        scale=YunmaiLib(sex==1,height,veryActive)
        fat=scale.getFat(age,weight,resistance)
        muscle=scale.getMuscle(fat)
        water=scale.getWater(fat)
        boneMass=scale.getBoneMass(muscle,weight)
        skeletalMuscle=scale.getSkeletalMuscle(fat)
        leanBodyMass=scale.getLeanBodyMass(weight,fat)
        visceralFat=scale.getVisceralFat(fat,age)    

        client.publish('{}/yunmai/weight'.format(mqttPrefix), round(weight,1))
        client.publish('{}/yunmai/fat'.format(mqttPrefix), round(fat))
        client.publish('{}/yunmai/muscle'.format(mqttPrefix), round(muscle))
        client.publish('{}/yunmai/water'.format(mqttPrefix), round(water))
        client.publish('{}/yunmai/boneMass'.format(mqttPrefix), round(boneMass))
        client.publish('{}/yunmai/skeletalMuscle'.format(mqttPrefix), round(skeletalMuscle))
        client.publish('{}/yunmai/leanBodyMass'.format(mqttPrefix), round(leanBodyMass))
        client.publish('{}/yunmai/visceralFat'.format(mqttPrefix), round(visceralFat))
        
        print('{"weight":',round(weight,1),', "fat":',round(fat),' , "muscle":',round(muscle),', "water":',round(water),', "boneMass":',round(boneMass),', "skeletalMuscle":',round(skeletalMuscle),', "leanBodyMass":',round(leanBodyMass),', "visceralFat":',round(visceralFat),' }')
        return

while True:
    try:
        client.connect(mqttServer)
        client.loop_start();

        p = Peripheral(mac)
        p.setDelegate( MyDelegate() )
        
        packet=bytearray.fromhex("12100100003a85")
        packet.extend(height.to_bytes(1, 'little'))
        packet.extend(sex.to_bytes(1, 'little'))
        packet.extend(age.to_bytes(1, 'little'))
        packet.extend(bytearray.fromhex("555a00000103")) # set scale data

        checksum = 0
        for el in packet:
            checksum ^= el

        packet.extend(bytes(checksum.to_bytes(1, 'little')))
        value = bytearray(b'\x0d')
        value.extend(packet)
        
        handle=44
        p.writeCharacteristic(handle, value, True)
            
        #print(" Connected to {}".format(mac))
        handle=40
        value=bytes([1, 0])

        p.writeCharacteristic(handle, value, True)
        #print("    Write {} to {:02x}".format(value, handle))
        
        while True:
            if p.waitForNotifications(1.0):
            #print("    Collecting data")
                continue

            #print ("Waiting...")

    except Exception as e:
         print('{"error": "',e,'"}')

    sleep(1)

    
    





