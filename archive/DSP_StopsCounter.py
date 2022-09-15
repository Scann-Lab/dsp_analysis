

Time_Dist_Success = True

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


def StopCount(line1, line2):

    prev_time = float(line2[0])
    curr_time = float(line1[0])
    prev_X = float(line1[1])
    prev_Z = float(line1[2])
    curr_X = float(line2[1])
    curr_Z = float(line2[2])

    if (prev_X == curr_X and prev_Z == curr_Z):

        return True
    else:
        return False

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
    line.append(Stressor)
    line.append(ExpType)
    line.append(DSPType)
    line.append(TrialNo)
    line.append(TrialID)
    line.append(Time_Elapsed)
    line.append(Dist)
    line.append(Status)
    line.append(Time_First)
    line.append(TotalStopTime)
    line.append(CountStop)
    line.append(CountStop3)
    return line
    
    
if (Time_Dist_Success == True):

    indir = "/pathtodata/"
    outdir = "/pathout/"
    
    outPutHeader = ['Participant No', 'Stressor','ExpType','DSPType', 'TrialNo', 'TrialID', 'Time Elapsed', 'Distance',
                     'Status', 'Time to First Movement','Total Stop Time','Total Stop Count','≥.5s Stops']
    
    wb = xlsxwriter.Workbook("/pathout/DSP_stops.xlsx")

    
    sheet = wb.add_worksheet('Sheet')
    
    for i in range (13):
        sheet.write(0, i, outPutHeader[i])

    input_line = []
    
    ParticipantNo = ""
    Stressor =""
    ExoType = ""
    DSPType = ""
    TrialNo = 0
    TrialID = ""
    Time_Elapsed = 0.0
    Dist = 0.0
    Status = ""
    Time_First = 0.0
    StopTime = 0.0
    TotalStopTime = 0.0
    StopFound = 0.0
    StopCounts = 0.0
    row = 0
    Time = 0.0
    Moving = 0.0
    Stopped = 0.0
    CountStop = 0
    CountStop2 = 0
    CountStop3 = 0
    TimeStopped = 0.0
    TotalStopTime = 0.0
    
    for f in os.listdir(indir):
        if (f != '.DS_Store'): 
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


            with open(indir + f) as infile:
                for current_line in infile: #skips first 7 lines
                    if (numOfLines <= 7):
                        if current_line.startswith('ParticipantNo'):
                            ParticipantNo = current_line[15:18]
                        if current_line.startswith('Stressor'):
                            Stressor = current_line[10:12]
                        if current_line.startswith('Exp Type'):
                            ExpType = current_line[11:18]
                        if current_line.startswith('DSPType'):
                            DSPType = current_line[9:10]
                        numOfLines += 1
                        
                    elif (current_line.startswith('!!')): #At every new trial, gets info and prints

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
                            
                            #print(input_line)
                        
                        TrialID = getTrialID(current_line)
                        TrialID = TrialID[0:7]
                        
                        col = 0
                        
                        for i in input_line: #Writes to excel file
                            sheet.write(row, col, i)
                            col += 1
                         
                        Dist = 0.0
                        row += 1
                        TrialNo += 1
                        print("!!",TrialID)
                        
                        Moving = 0.0
                        Stopped = 0.0
                        TimeStopped = 0.0
                        TotalStopTime = 0.0
                        CountStop = 0
                        CountStop2 = 0
                        CountStop3 = 0
                        
                    
                    else: #Finds time of first movement and sums x and y values for distance
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

                            if foundFirstTime == True:

                                line1 = getInfo(current_line)
                                line2 = getInfo(prev_line)
                                prev_time = float(line2[0])
                                curr_time = float(line1[0])
                                if (StopCount(line1,line2) == False):

                                    Stopped = 0.0
                                    TimeStopped = 0.0
                                    Moving += 1
                                    CountStop2 = 0
                                    #print("Move Counter =", Moving)

                                if (StopCount(line1, line2) == True):

                                    Moving = 0

                                    StopTime = curr_time - prev_time
                                    TotalStopTime += StopTime

                                    Stopped += 1
                                    #print("stop = ",Stopped)
                                    
                                    if Stopped == 1:
                                        CountStop += 1
                                    
                                    if Stopped > 0:
                                        TimeStopped += StopTime
                                        #print("Time w/i this stop =", TimeStopped)
                                    if TimeStopped >= .5:
                                        CountStop2 += 1
                                        #print("CS2 = ",CountStop2)
                                        if CountStop2 == 1:
                                            CountStop3 += 1 
                                        #print("CS3 = ",CountStop3)


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