# startSignageSlideshow.py | Version 1.0

import json
import os
import time
import calendar
from datetime import datetime, timedelta

#Read in the config JSON.
with open('DigitalSignageConfig.json') as f:
    configData = json.load(f)

def main():
    checkType()
    exit()
    doLog("Started DigitalSignage")
    currentState = "firstrun"
    #Loop forever.
    while(True):
        doLog("Starting check loop...")
        #Check if we are on the first run or going into a state change (blank, static, or slides).
        #The state variable is an array with of [nextState, timeUntilNextState].
        if currentState == 'firstrun':
            state = ('slides', timedelta(hours=0, minutes=0, seconds=0))
        else:
            state = checkType()
        if state != None:
            #If we are going into a different state then the previous one or there is a restart in the next 10 minutes, sleep until the right time and then call doSlides().
            if currentState != state[0] or state[0] == 'restart':
                #If we are restarting, set state[0] to the previous state.
                if state[0] == "restart":
                    state[0] = currentState
                doLog("Changing from {} state to {} state in {} seconds, sleeping until then.".format(currentState, state[0], state[1].seconds))
                #Sleep until the time to change.
                time.sleep(state[1].seconds)
                #Set the current state to the one we are going to.
                currentState = state[0]
                #Call the function to load the slides.
                doSlides(state[0])
        doLog("Check loop done, sleeping for 5 minutes...")
        #Sleep for 5 minutes until the next check
        time.sleep(300)

def checkType():
    retVal = None
    #Read in the schedule file.
    with open("{}DigitalSignageSchedule.json".format(configData["SignagePath"])) as f:
        data = json.load(f)
    #Get the day of the week.
    dayOfWeek = calendar.day_name[datetime.now().weekday()]
    #Create an array of times for the current day. It is created from the "Daily" times along with the times for the current day of the week.
    #Times for the day of the week have higher precedent.
    timesToConsider = []
    for k, v in data[dayOfWeek].items():
        if v != "":
            times = v.split(",")
            for x in times:
                timesToConsider.append([k, x.replace(" ", "")])
    for k, v in data["Daily"].items():
        if v != "":
            times = v.split(",")
            for x in times:
                timesToConsider.append([k, x.replace(" ", "")])
    #Convert the dates to timedeltas from the current time.
    for x in timesToConsider:
        splitTime = x[1].split(":")
        periodStartDT = datetime.now().replace(hour=int(splitTime[0]), minute=int(splitTime[1]), second=0)
        x[1] = periodStartDT - datetime.now()
    #If there is a period that starts in the next 10 minutes, return it.
    for x in timesToConsider:
        if x[1].seconds <= 600 and x[1].days == 0:
            retVal = x
    return retVal

def doSlides(typePath):
    #Get the files from the slide path.
    files = os.listdir("{}{}\\".format(configData["SignagePath"], typePath))
    # Filter for only pptx files that have a file name of the correct format (length of a date, starts with the year, have two dashes).
    files = [x for x in files if x[-4:] == "pptx" and (len(x) == 15 and x[:2] == "20" and x.count("-") == 2)]
    #Set the filename temporarily to the first pptx file.
    fname = files[0]
    #Loop through all the qualifying files and determine which has the closest date without being in the future.
    for file in files:
        date = datetime.strptime(file[:-5], '%Y-%m-%d')
        if date > datetime.strptime(fname[:-5], '%Y-%m-%d') and date <= datetime.now():
            fname = file
    #Log that we are starting.
    doLog("Starting slides {}.".format(fname))
    #Kill PowerPoint if it is already running.
    os.system("taskkill /F /IM POWERPNT.exe")
    #Change to the signage directory.
    os.chdir("{}{}".format(configData["SignagePath"], typePath))
    #Create the command to start PowerPoint with the correct slideshow.
    cmd = 'start "" "{}" /S {}'.format(configData["PowerPointPath"], fname)
    #Run the command. 
    os.system(cmd)
    #Go back to the signage directory.
    os.chdir("{}".format(configData["SignagePath"], typePath))

def doLog(stringToLog):
    output = "{} | {}\n".format(datetime.now(), stringToLog)
    print(output)
    with open("{}/log.txt".format(configData["CodePath"]), 'a+') as f:
        f.write(output)

if __name__ == '__main__':
    main()
