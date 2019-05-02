#Start of code for processing TSP data for tours of countries
#http://www.math.uwaterloo.ca/tsp/world/countries.html
import math
import sys
import time
import pickle
import pprint

def processTour(fileName,roundTo=2):
    infile=open(fileName,"r")
    dataD={}
    listData=[]
    line=infile.readline()
    while "NODE_COORD_SECTION" not in line:
        line=infile.readline()
    lineCount=0
    for line in infile:
        lstVals=line.split()
        if len(lstVals)>1:
            dataD[int(lstVals[0])-1]=[float(lstVals[1]),float(lstVals[2])]
            listData.append([float(lstVals[1]),float(lstVals[2])])
        lineCount+=1
    print("Dictionary created")
    if lineCount < 20:
        pp = pprint.PrettyPrinter(indent=3)
        pp.pprint(dataD)
        print("List created")
        pp.pprint(listData)
    start=time.time()
    TSPMatrix=[]
    for row in range(len(listData)):
        r=[]
        #for col in range(row,len(listData)):  #For "diagonal" matrix, but will need to adjust your access = index -row
        for col in range(len(listData)):
            d=round((math.sqrt((listData[row][0]-listData[col][0])**2+(listData[row][1]-listData[col][1])**2)),roundTo)
            r.append(d)
        TSPMatrix.append(r)
        if row !=0 and row%1000==0:
            print(row, time.time()-start)
    if lineCount<20:
        print("Distance Matrix created")
        for row in TSPMatrix:
            print(row)
    return  sys.getsizeof(dataD),sys.getsizeof(listData),sys.getsizeof(TSPMatrix),TSPMatrix

szD,szL,szTSP,tsp=processTour("wi29.tsp",roundTo=4)
outFile=open("matrix.txt","w")
for row in range(len(tsp)):
    outFile.write(str(tsp[row])+"\n")
outFile.close()

pklOut=open("pickledMatrix.pkl","wb")
x=pickle.dump(tsp,pklOut)
pklOut.close()


    
