## Written by Alex Boone
## Modified by Steven Weisberg
## Last edit: 2/10/2020

### Purpose of this script is to process location data from the Dual Solution
### Paradigm, built in Unity 3D. It will output a set of images that can be 
### hand-coded to determine A) Success, and B) which path was taken (familiar
### route or novel shortcut). 


from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
#from imageio import imread
import os

Plotter = False
Time_Dist_Success = True

#******************************************************************************************************
#                                         PLOTTER
#******************************************************************************************************


scriptDir = os.getcwd()

# Expects that the data is one file up from the analysis script
os.chdir(os.path.dirname(os.getcwd()))
masterDir = os.getcwd()


indir = os.path.join(masterDir,'DSP_RawData')
outdir = os.path.join(masterDir,'DSP_ProcessedData')


def Graph(trialID):
    pyplot.figure(dpi = 350)
    figureFiletype = ".png"
    pyplot.plot(PosX_array, PosY_array, "k", label = "__nolegend__")

    v = [0, 222, 0, 222]
    pyplot.axis(v)
    pyplot.ylabel("Y")
    pyplot.xlabel("X")
    pyplot.title(title)
    pyplot.legend(["Path"], loc = 'center left', bbox_to_anchor = (1.0, 0.5))
   
    
    # Which version of the experiment are we in?
    if (Alt_Exp == "DSPType: 2"):
        expPrefix = "DSP2_"
    else:
        expPrefix = "DSP1_"

    # Open the image with that trial structure
    imageFilename = expPrefix + trialID + figureFiletype
    bestImage = os.path.join(scriptDir,'Nav_stratAbility_Maps',imageFilename)
    img = imread(bestImage)


    #AFTER I HAVE CREATED THE INDIVIDUAL BASEMAPS

    pyplot.imshow(img,zorder=0,extent=[0.0, 222.0, 0.0, 222.0]) #left right bottom top


    pp.savefig()
    pyplot.clf()

#######
if (Plotter == True):
    

    currTrial = ""
    Alt_Exp = ""
    TrialID = ""
    title = ""

    for f in os.listdir(indir):
        #the first file in each directory was this for some reason
        if ("txt" in f):
            print (f)
            numOfLines = 0
            Trial_Count = 0

            with open(os.path.join(indir,f)) as infile:
                filename = f + ".pdf"
                pp = PdfPages(os.path.join(outdir,filename))
                PosX_array = []
                PosY_array = []

                for current_line in infile:

                    if (current_line.startswith("!!")):
                        if (Trial_Count > 0):
                            Graph(currTrial)
                            PosX_array = []
                            PosY_array = []

                        Trial_Count += 1

                        title = current_line[2:]
                        title_split = current_line.split("_")
                        trialID = title_split[2]
                        trialID = trialID[0:2]
                        currTrial = trialID

                        print (title)
                    elif "DSPType" in current_line:
                        Alt_Exp = current_line.strip()
                    elif current_line == '\n':
                        print('uh oh')
                    #Gets x,z coordinates from each line and puts into array
                    elif Trial_Count > 0:
                        no_time_line = current_line.split("  ")
                        movement = no_time_line[1].split(",")
                        x = float(movement[0])
                        y = float(movement[1])

                        PosX_array.append(x)
                        PosY_array.append(y)

                #Plots the last trial
                else:
                    Graph(currTrial)
                    PosX_array = []
                    PosY_array = []


            pyplot.close()
            pp.close()
#########

#******************************************************************************************************
#                                TIME/DIST/SUCESS PARSER
#******************************************************************************************************


import os
import xlsxwriter
import math

def distance(x1,y1,x2,y2): #simple distance formula
    x = x1-x2
    y = y1-y2
    x = x**2
    y = y**2
    z = x+y
    return round(math.sqrt(z), 2)

def checkFail(time):
    if time >= 39.98:
        return "Failure"
    else:
        return "Success"

def getInfo(line): #returns list of all info
    split_time = line.split(':')
    Time_Elapsed = float(split_time[0])
    split_other = split_time[1].split(',')
    X_Coord = float(split_other[0])
    Y_Coord = float(split_other[1])
    info = [Time_Elapsed, X_Coord, Y_Coord]
    return info

def getTrialID(line):
    line = current_line.split("_")
    TrialID = line[1] + "_" + line[2]
    return TrialID

def checkFirstMove(line1, line2):
    prev_X = float(line1[1])
    prev_Z = float(line1[2])
    curr_X = float(line2[1])
    curr_Z = float(line2[2])
    if (prev_X != curr_X or prev_Z != curr_Z):
        return True
    else:
        return False

def appendInput():
    line = []
    line.append(ParticipantNo)
    line.append(DSPType)
    line.append(EncodingTours)
    line.append(TrialNo)
    line.append(TrialID)
    line.append(Time_Elapsed)
    line.append(Dist)
    line.append(Status)
    line.append(Time_First)
    return line



if (Time_Dist_Success == True):

    
    outputHeader = ['ParticipantNo','DSPType', 'EncodingTours', 'TrialNo', 'TrialID', 'Time Elapsed', 'Distance',
                     'Status', 'Time_to_First_Movement']

    wb = xlsxwriter.Workbook(os.path.join(outdir,"Master_DSP_all.xlsx"))

    sheet = wb.add_worksheet('Sheet')

    for i in range (len(outputHeader)):
        sheet.write(0, i, outputHeader[i])



    input_line = []

    ParticipantNo = ""
    Stressor = ""
    ExpType = ""
    DSPType = ""
    EncodingTours = ""
    ParticipantGen = ""
    TrialNo = 0
    TrialID = ""
    Time_Elapsed = 0.0
    Dist = 0.0
    Status = ""
    Time_First = 0.0
    
    headerCounter = 0
    trialStart = False
    
    row = 0

    for f in os.listdir(indir):
        if ("txt" in f):
            print (f)
            numOfLines = 0
            TrialNo = 0
            prev_line = ""
            curr_line= ""
            line_no = 0
            foundFirstTime = False
            Dist = 0.0
            x1 = 0.0
            y1 = 0.0
            x2 = 0.0
            y2 = 0.0
            
            headerLines = 0

            with open(os.path.join(indir,f)) as infile:
                for current_line in infile: 
                    
                    if headerLines < 5:
                        if current_line.startswith('Participant'):
                            ParticipantNo = current_line.split(': ')[1]
                        elif current_line.startswith('DSPType'):
                            DSPType = current_line.split(': ')[1]
                        elif current_line.startswith('Encoding'):
                            EncodingTours = current_line.split(': ')[1]

                        headerLines += 1

                    elif (current_line.startswith('!!')): #At every new trial, gets info and prints
                        trialStart = True
                        if TrialNo > 0:
                            info = getInfo(prev_line)
                            Time_Elapsed = float(info[0])
                            Status = checkFail(Time_Elapsed)
                            foundFirstTime = False
                            prev_line = ""
                            x1 = 0.0
                            y1 = 0.0
                            x2 = 0.0
                            y2 = 0.0
    
                            input_line = appendInput()
    
    
                        TrialID = getTrialID(current_line)
                        TrialID = TrialID[0:7]
    
                        col = 0
    
                        for i in input_line: #Writes to excel file
                            sheet.write(row, col, i)
                            col += 1
    
                        Dist = 0.0
                        row += 1
                        TrialNo += 1
    
                    elif trialStart: #Finds time of first movement and sums x and y values for distance
                        if (prev_line.startswith("!")) == False and (prev_line != ""):
                            line1 = getInfo(current_line)
                            line2 = getInfo(prev_line)
                            x1 = float(line1[1])
                            y1 = float(line1[2])
                            x2 = float(line2[1])
                            y2 = float(line2[2])
    
                    
                            Dist += float(distance(x1, y1, x2, y2))
    
                    
                            if foundFirstTime == False:
                                line1 = getInfo(current_line)
                                line2 = getInfo(prev_line)
    
                                if (checkFirstMove(line1, line2)):
                                    Time_First = line1[0]
                                    foundFirstTime = True
    
                        #To prepare for trial #24
                        if TrialNo == 24:
                            curr_line = current_line
    
                        prev_line = current_line

                #Does trial #24
                info = getInfo(prev_line)
                Time_Elapsed = float(info[0])
                Status = checkFail(Time_Elapsed)
                foundFirstTime = False
                prev_line = ""
                input_line = appendInput()
    
                col = 0 

                for i in input_line:
                    sheet.write(row, col, i)
                    col += 1

                            #print(input_line)

    wb.close()
