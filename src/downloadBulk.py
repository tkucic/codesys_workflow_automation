
#Codesys iron python / python 2.7
from __future__ import print_function
import time

##Define list of ip addresses to download software
IP_LIST = [
    '172.24.1.41',
    '172.24.1.42',
    '172.24.1.43',
    '172.24.1.44',
    '172.24.1.45',
    '172.24.1.46'
            ]
GATEWAYS = []

#Save project if unsave
project = projects.primary
if project.dirty:
    project.save()

##Run the code generation and see if there is some errors
#Get the active application
application = project.active_application

#Generate its code
application.build()
application.generate_code()

#Check for errors
for msg in system.get_message_objects():
    print(type(msg))

#Change IP address
print('CTry to change IP address')

#Get the gateway
for gateway in online.gateways:
    print(gateway.name)

print('Create online application')
onlineApp = online.create_online_application()

print('Try to login')
onlineApp.login(0, False) #Login and do a full download

print('Try to start')
onlineApp.start()

print('App is: ', onlineApp.application_state)

print('PLC downloaded, going to next plc')
onlineApp.logout()