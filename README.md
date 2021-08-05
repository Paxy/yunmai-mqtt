# yunmai-mqtt
Simple scripts to read BLE data from Yunmai Smart Scale and upload it to MQTT

yunmai.py - command line to connect to BLE Yunmai scale, wait for meassurment data, and display the results in JSON form.
JSON results sample: {"weight": 86.9 , "fat": 25  , "muscle": 52 , "water": 54 , "boneMass": 4 , "skeletalMuscle": 45 , "leanBodyMass": 65 , "visceralFat": 9 }

yunmai-mqtt.py - daemon that keeps running in the loop waiting scale meassures. After each meassure, it sends data to MQTT server.

Configuration:
Variables are configured directly inside the scripts.
mac - Yunmai Scale MAC address
sex - 1 for Male, 2 for Female
height - Heigh
veryActive - (True/False) - are you sports active person
age - Age
mqttServer - MQTT Server IP address
mqttPrefix - MQTT topic prefix

Notice:
On my Yunmai Mini Smart Scale, there is a issue with firmware. Only frist time after inserting the batteries, values other then weight is meassured and sent. So, if you have the issue that only weight is meassured, you need to "reset" your scale every time and you will get other parameters.
