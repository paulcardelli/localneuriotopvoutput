#!/usr/bin/python
#
# Python script to upload neurio data locally to pvoutput and to csv
# Also pulls weather from Weather Underground from selected PWS
#
# Script can be modified to pull more frequently, and to send ot more locations
# Such and ThingSpeak.com or to Google Sheets
#
# Crontab to run ever 5 minutes  - Example
#0 * * * * /usr/local/bin/neurio/neurio.py
#5 * * * * /usr/local/bin/neurio/neurio.py
#10 * * * * /usr/local/bin/neurio/neurio.py
#15 * * * * /usr/local/bin/neurio/neurio.py
#20 * * * * /usr/local/bin/neurio/neurio.py
#25 * * * * /usr/local/bin/neurio/neurio.py
#30 * * * * /usr/local/bin/neurio/neurio.py
#35 * * * * /usr/local/bin/neurio/neurio.py
#40 * * * * /usr/local/bin/neurio/neurio.py
#45 * * * * /usr/local/bin/neurio/neurio.py
#50 * * * * /usr/local/bin/neurio/neurio.py
#55 * * * * /usr/local/bin/neurio/neurio.py
#

import requests, csv, os, subprocess
from time import strftime

#IP address of Neurio
neurioip = "192.168.1.17"  #Change to IP address of your Neurio Sensor 

#PVoutput System ID
SYSTEMID='12345'  #signup and get from pvoutput.org hint you will see it on the URL

#PVoutput API Key
APIKEY='1234abc' #signup and get API Key from pvoutput.org undet settings

wu_apikey="1234abc" # sign up here http://www.wunderground.com/weather/api/ for a key
wu_pws="KWASEATT329" # Personal weatherstation ID just pick one near you and change this ID

#CSV file Path
pvpath = "/home/pi/"   #Pick a path that is conveniant. This will be your backup data location for when the internet was down. You may want to delete of compress older files

#status DATE  yyyymmdd
pvdate = strftime('%Y%m%d')  

#status TIME  24 HH:MM
pvtime = strftime('%H:%M')

#set retries to 5
requests.adapters.HTTPAdapter(max_retries=5)

#pull json from local neurio sensor json
pvdata = requests.get('http://'+neurioip+'/current-sample').json()

gen_W = pvdata['channels'][3]['p_W']
gen_V = pvdata['channels'][3]['v_V']
cons_W = pvdata['channels'][4]['p_W']
temp_c = 0

#checks if gen_W is a negative and if so changes to 0
if gen_W < 0:
	gen_W = 0

# weatherunderground
wu_data = requests.get('http://api.wunderground.com/api/'+wu_apikey+'/conditions/q/pws:'+wu_pws+'.json').json()
temp_c = wu_data['current_observation']['temp_c']

#logdata locally on CSV
if os.path.isfile(pvpath+pvdate+'.csv'):
	fd = open(pvpath+pvdate+'.csv','a')
	writer = csv.writer(fd)
	writer.writerow( (pvtime, gen_W, gen_V, cons_W,temp_c) )
	fd.close()
else:
	fd = open(pvpath+pvdate+'.csv','w')
	writer = csv.writer(fd)
	writer.writerow( ('Time', 'Solar Watts', 'Volts', 'Consumption Watts','Temperature') )
	writer.writerow( (pvtime, gen_W, gen_V, cons_W,temp_c) )
	fd.close()

#upload the data to the pvoutput website  d=date t=time v2=Power_gen_watts v3=Power_consumed_watts v5=temp_celcius v6=genation volts
cmd=('curl --retry 10 -d "d=' + pvdate + '" -d "t=' + pvtime + '" -d "v2=' + str(gen_W) + '" -d "v4=' + str(cons_W) + '" -d "v5=' + str(temp_c) + '" -d "v6=' + str(gen_V) + '" -H "X-Pvoutput-Apikey:'+ APIKEY +'" -H "X-Pvoutput-SystemId:'+ SYSTEMID +'" http://pvoutput.org/service/r2/addstatus.jsp') 

#send the request
ret = subprocess.call(cmd, shell=True)

# Was working on replacing the subprocess call with a request.post but kept getting 400 bad request errors
#headers = {
#	'X-Pvoutput-Apikey': APIKEY, 
#	'X-Pvoutput-SystemId': SYSTEMID
#}
#data = 'd='+pvdate+'&t='+pvtime+'&v2='+str(gen_W)+'&v4='+str(cons_W)+'&v5='+str(temp_c)#+'&v6='+str(gen_V)
#print data
#r = requests.post('http://pvoutput.org/service/r2/addstatus.jsp', headers=headers, data=data)
#print r.status_code

