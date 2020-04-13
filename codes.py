
import csv
import os

csvfile = "csv1.csv"
namesfile = "see51.names"
datafile = "see51.data"
target="pred"
maxnum=10

# read csv file
f = open(csvfile, 'r')
alldata = list(csv.reader(f))
f.close()

# create .names file
n=open(namesfile,"w")
print(target+"\t"*3+"| the target attribute"+"\n")
n.write(target+"\t"*3+"| the target attribute"+"\n"*2)

attributes = alldata[0]

data=[]
for item in alldata[1:]:
    for x in range(len(attributes)):
        item_x=str(item[x])
        data+=[item_x,]

datatype=[]
for w in range(len(attributes)):
    for y in range(w,len(data),len(attributes)):
        datatype+=[data[y],]
    datatype=list(sorted(set(datatype)))
    try:
        t="+"
        datacheck=eval(str(t.join(datatype)).strip("~!@#$%^&*(),./;'[]\<>-=_+{}|:<>? "))
        print(attributes[w]+"\t\t"+"continuous.")
        n.write(attributes[w]+"\t"*2+"continuous."+"\n")
    except NameError or SyntaxError:
        if len(datatype)>=maxnum:
            print(attributes[w]+"\t\t"+"label.")
            n.write(attributes[w]+"\t"*2+"label."+"\n")
        else:
            print(attributes[w],end="\t\t")
            n.write(attributes[w]+"\t"*2)
            print(",".join(datatype)+".")
            n.write(",".join(datatype)+".\n")          

    w+=1
    datatype=[]
n.close()

# create .data file
m=open(datafile,"w")
for d in alldata[1:]:
    print(",".join(d))
    m.write(",".join(d)+"\n")
m.close()

