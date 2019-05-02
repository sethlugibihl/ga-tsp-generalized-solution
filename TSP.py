#Start of code for processing TSP data for tours of countries
#http://www.math.uwaterloo.ca/tsp/world/countries.html
import math
import sys
import time

def processTour(fileName,numPreLines):
    infile=open(fileName,"r")
    dataD={}
    listData=[]
    for i in range(numPreLines):
        infile.readline()
    for line in infile:
        lstVals=line.split()
        if len(lstVals)>1:
            #dataD[int(lstVals[0])]=[int(float(lstVals[1])*10000),int(float(lstVals[2])*10000)]
            #listData.append([int(float(lstVals[1])*10000),int(float(lstVals[2])*10000)])
            dataD[int(lstVals[0])]=[float(lstVals[1]),float(lstVals[2])]
            listData.append([float(lstVals[1]),float(lstVals[2])])
            if int(lstVals[0]) % 1000 == 0:
                print(lstVals[0])
    #dataD=[]
    #listData=[[10,10],[8,8],[5,5],[6,6],[12,12],[2,2]]
    print(listData[:1])
    start=time.time()
    TSPMatrix=[]
    for row in range(len(listData)):
        r=[]
        #for col in range(row,len(listData)):
        for col in range(len(listData)):
            #print((listData[row][0]-listData[col][0])**2)
            d=round((math.sqrt((listData[row][0]-listData[col][0])**2+(listData[row][0]-listData[col][0])**2)),2)
            print(d)
            r.append(d)
        TSPMatrix.append(r)
        if row%1000==0:
            print(row, time.time()-start)
    return  sys.getsizeof(dataD),sys.getsizeof(listData),TSPMatrix

szD,szL,tsp=processTour("wi29.tsp",7)
print("Dictionary size in bytes = ", szD)
print("List size in bytes = ", szL)
outFile=open("matrix.txt","w")
for row in range(len(tsp)):
    #outFile.write(str(tsp[row]).rjust(300)+"\n")
    outFile.write(str(tsp[row])+"\n")
outFile.close()

    
