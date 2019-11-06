from tkinter import *
import time
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
 
#for buttonPress function
prevInput = True
 
old_a = True
old_b = True
 
 
#If set to true (default), will display Red Line. If set false,
#will display brown line.
lineButton = True
 
#redLine and brownLine dictionaries
redLine = {40900: "Howard", 41190:"Jarvis", 40100: "Morse", 41300:"Loyola", 40760:"Granville",40880:"Thorndale", 41380:"Bryn Mawr", 40340:"Berwyn",
           41200:"Argyle",40770:"Lawrence",40540:"Wilson", 40080:"Sheridan", 41420:"Addison", 41320:"Belmont", 41220:"Fullerton",40650:"North/Clybourn",
           40630:"Clark/Division" ,41450:"Chicago",40300:"Grand",41660:"Lake",41090:"Monroe",40560:"Jackson",41490:"Harrison",41400:"Roosevelt",
           41000:"Cermak-Chinatown",40190:"Sox-35th",41230:"47th",41170:"Garfield",40910:"63rd",40990:"69th",42040:"79th",41430:"87th",40450:"95th/Dan Ryan"}
 
brownLine = {41290:"Kimball",41189:"Kedzie",40870:"Francisco", 41010:"Rockwell", 41480:"Western", 40090:"Damen", 41500:"Montrose", 41460:"Irving Park",
             41440:"Addison", 41310:"Paulina", 40360:"Southport", 41320:"Belmont",41210:"Wellington", 40530:"Diversey", 41220:"Fullerton", 40660:"Armitage",
             40800:"Sedgwick", 40710:"Chicago", 40730:"Washington/Wells", 40040:"Quincy", 40160:"LaSalle/Van Buren", 40850:"Harold Washington Library",
             40680:"Adams/Wabash", 40260:"State/Lake", 40380:"Clark/Lake"}
 
#redID and brownID contain all of the stop IDs
redID = [40900, 41190, 40100, 41300, 40760, 40880, 41380, 40340, 41200, 40770, 40540, 40080, 41420, 41320, 41220, 40650, 40630, 41450, 40300, 41660, 41090, 40560,
         41490, 41400, 41000, 40190, 41230, 41170, 40910, 40990, 42040, 41430, 40450]
 
brownID = [41290, 41189, 40870, 41010, 41480, 40090, 41500, 41460, 41440, 41310, 40360, 41320, 41210, 40530, 41220, 40660, 40800, 40710, 40730, 40040, 40160, 40850,
           40680, 40260, 40380]
 
#Fullerton is the default stop for both lines
redStop = 41220
brownStop = 41220
 
#temp number for iteration, ignore
i = 0
             
 
#tick function updates time using local time on computer
def tick():
    global time1
    time2 = time.strftime("%I:%M %p")
    if time2 != time1:
        time1 = time2
        currentTime.config(text=time2)
    currentTime.after(200, tick)
 
#function to toggle button press and switch from displaying red line to brown line
def buttonPress():
    global lineButton
    global prevInput
    newInput = GPIO.input(18)
    if newInput == False and prevInput == True:
        lineButton = not lineButton
    prevInput = newInput
    root.after(10, buttonPress)
 
#function to switch GUI to red line
def redLineSwitch():
    global lineButton
    global redLineLabel
    global redStopDisplay
    global redNorthLabel
    global redSouthLabel
    global i
   
 #   if lineButton:
    brownLineLabel.pack_forget()
    brownStopDisplay.pack_forget()
    brownNorthLabel.pack_forget()
    brownSouthLabel.pack_forget()
    root.update()
    redLineLabel.pack(fill=X)
    redStopDisplay.pack(fill=X)
    redNorthLabel.pack(fill = X)
    redSouthLabel.pack(fill = X)
    root.update()
    i = 0
 
#function to switch GUI to brown line
def brownLineSwitch():
    global lineButton
    global brownLineLabel
    global brownStopDisplay
    global brownNorthLabel
    global brownSouthLabel
    global i
   
   # if not lineButton:
    redLineLabel.pack_forget()
    redStopDisplay.pack_forget()
    redNorthLabel.pack_forget()
    redSouthLabel.pack_forget()
    root.update()
    brownLineLabel.pack(fill=X)
    brownStopDisplay.pack(fill=X)
    brownNorthLabel.pack(fill = X)
    brownSouthLabel.pack(fill = X)
    root.update()
    i = 0
   
def get_encoder_turn():
    # return -1, 0, or +1
    global old_a, old_b
    result = 0
    new_a = GPIO.input(23)
    new_b = GPIO.input(24)
    if new_a != old_a or new_b != old_b :
        if old_a == 0 and new_a == 1 :
            result = (old_b * 2 - 1)
        elif old_b == 0 and new_b == 1 :
            result = -(old_a * 2 - 1)
    old_a, old_b = new_a, new_b
    time.sleep(0.001)
    return result
 
def iterateStops():
    global i
    global redStop
    global brownStop
    global redID
    global brownID
    global redLine
    global brownLine
   
    change = get_encoder_turn()
    print(change)
   
    #keypress/knob code...
    if lineButton:
        if change != 0 and i > 0 and i < len(redID):
            i = i + change
            redStop = redID[i]
            print(redStop)
    else:
        if change != 0 and i > 0 and i < len(brownID):
            i = i + change
            brownStop = brownID[i]
            print(brownStop)
    root.after(10, iterateStops)
 
def currentStop():
    global redStop
    global brownStop
    global redLine
    global brownLine
    global redLineLabel
    global redStopDisplay
    global brownLineLabel
    global brownStopDisplay
   
    if lineButton:
        redStopDisplay.pack_forget()
        redStopDisplay = Label(headerFrame, text = "{}".format(redLine[redStop]), bg = "red", fg = "white", font=("Arial", 14))
        redStopDisplay.pack(fill=X)
        root.update()
    else:
        brownLineLabel.pack_forget()
        brownStopDisplay = Label(headerFrame, text = "{}".format(brownLine[brownStop]), bg = "saddle brown", fg = "white", font=("Arial", 12))
        brownStopDisplay.pack(fill=X)
        root.update()
    root.after(10, currentStop)
 
#Creates GUI Window
root = Tk()
root.geometry("320x240")
headerFrame = Frame(root)
headerFrame.pack(side= TOP)
directionFrame = Frame(root)
directionFrame.pack(side=LEFT)
 
#sets current time
time1 = ""
currentTime = Label(headerFrame, font=("Arial", 10))
currentTime.pack()
tick()
 
#Red Line labels
redLineLabel = Label(headerFrame, text = "CTA Red Line Tracker | Station:", bg = "red", fg = "white",font=("Arial", 14))
redStopDisplay = Label(headerFrame, text = "{}".format(redLine[redStop]), bg = "red", fg = "white", font=("Arial", 14))
redNorthLabel = Label(directionFrame, text = "Howard: {}, {}".format(schedule[0], schedule[1]), bg = "red", fg = "white",font=("Arial", 18))
redSouthLabel = Label(directionFrame, text = "95th/Dan Ryan: {}, {}".format(schedule[2], schedule[3]), bg = "red", fg = "white",font=("Arial", 18))
 
#Brown Line labels
brownLineLabel = Label(headerFrame, text = "CTA Brown Line Tracker | Station:", bg = "saddle brown", fg = "white",font=("Arial", 12))
brownStopDisplay = Label(headerFrame, text = "{}".format(brownLine[brownStop]), bg = "saddle brown", fg = "white", font=("Arial", 12))
brownNorthLabel = Label(directionFrame, text = "Kimball: ", bg = "saddle brown", fg = "white",font=("Arial", 18))
brownSouthLabel = Label(directionFrame, text = "Loop: ", bg = "saddle brown", fg = "white",font=("Arial", 18))

if lineButton:
        redLineSwitch()
if lineButton == False:
        brownLineSwitch()
 
 
#Refreshes the GUI and checks for each function
root.after(10, buttonPress)
root.after(10, iterateStops)
root.after(10, currentStop)
 
root.mainloop()
