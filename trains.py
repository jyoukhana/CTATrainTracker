import urllib.request
import json
import datetime
import dateutil.parser
## pip install python-dateutil
import time
import gui



api_key = "46b2d88168b94c2893e7a38aeb14ce07"
def timeFix(isoTime):
    ttime = dateutil.parser.parse(isoTime)
    hoursminutes = ttime.strftime('%H:%M')
    return hoursminutes

    
  #  niceTime = time.strftime("%b %d %Y %H:%M:%S",unformattedtime)

def getTrains(bool, trainId):
    #this can only reach 4
    numberTrains = 0
    south = []
    north = []
    trainQueue = 0

    if bool == True:
        #howard/95th can only reach max.length of 2

        while numberTrains < 4:
            redline_url = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=" + str(api_key) + "&mapid=" +str(trainId)+ "&rt=" + "red&max=10&outputType=JSON"  
            red = urllib.request.urlopen(redline_url)

            data = json.load(red)

            # train = data['ctatt']['eta'][1]

            etaList = data['ctatt']['eta']
            
            if etaList[trainQueue]['stpDe'] == 'Service toward 95th/Dan Ryan': 
                if len(south)>=2:
                    if trainQueue>=4:
                        trainQueue = 0
                        print("nice")
                    else:
                        trainQueue+=1
                        print('v cool')
                else:
                    arrival_time = timeFix(etaList[trainQueue]['arrT'])
                    south.append(arrival_time)
                    trainQueue+=1
                    numberTrains+=1
            else:
                if len(north)>=2:
                    if trainQueue>=4:
                        trainQueue = 0
                    else:
                        trainQueue+=1
                else:
                    arrival_time = timeFix(etaList[trainQueue]['arrT'])
                    north.append(arrival_time)
                    trainQueue+=1
                    numberTrains+=1

            #print(north)
            #print("howard ^ 95 v")
            #print(south)

            
    else:
        while numberTrains < 4:
            brownline_url = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=" + str(api_key) + "&mapid=" +str(trainId)+ "&rt=" + "brn&max=10&outputType=JSON"  
            brown = urllib.request.urlopen(brownline_url)

            data = json.load(brown)

            # train = data['ctatt']['eta'][1]

            etaList = data['ctatt']['eta']
        
            if etaList[trainQueue]['stpDe'] == 'Service toward Loop': 
                if len(south)>=2:
                    if trainQueue>=4:
                        trainQueue = 0
                    else:
                        trainQueue+=1
                else:
                    arrival_time = etaList[trainQueue]['arrT']
                    south.append(arrival_time)
                    trainQueue+=1
                    numberTrains+=1

            else:
                if len(north)>=2:
                    if trainQueue>=4:
                        trainQueue = 0
                    else:
                        trainQueue+=1
                else:
                    arrival_time = etaList[trainQueue]['arrT']
                    north.append(arrival_time)
                    trainQueue+=1
                    numberTrains+=1

            #print(north)
            #print("kimball ^ loop v")
            #print(south)

    if numberTrains == 4:        
        schedule = []
        for first in north:
            schedule.append(first)
        for second in south:
            schedule.append(second)
        print(schedule)
        
            
#def delayed():
#    delayed = true



# test link
#red
#redline_url = http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=46b2d88168b94c2893e7a38aeb14ce07&mapid=41220&rt=red&max=5&outputType=JSON
#brown
# http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=46b2d88168b94c2893e7a38aeb14ce07&mapid=41220&rt=brn&max=5&outputType=JSON
getTrains(True, 41220)

##to do:
    ## test cases for howard/95th, not super important
    ## fix the appearance of time
