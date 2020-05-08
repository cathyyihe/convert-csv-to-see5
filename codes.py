import csv
import os

class See5():
    def __init__(self,csvfile,namesfile,datafile,target):
        self.csvfile = csvfile
        self.namesfile = namesfile
        self.datafile = datafile
        self.target=target

    def generate_see5(self):
        maxnum=10

        # read csv file
        f = open(self.csvfile, 'r')
        alldata = list(csv.reader(f))
        f.close()

        # create .names file
        n=open(self.namesfile,"w")
        n.write(self.target+"\t"*3+"| the target attribute"+"\n"*2)

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
                n.write(attributes[w]+"\t"*2+"continuous."+"\n")
            except NameError or SyntaxError:
                if len(datatype)>=10:
                    n.write(attributes[w]+"\t"*2+"label."+"\n")
                else:
                    n.write(attributes[w]+"\t"*2)
                    n.write(",".join(datatype)+".\n")
            w+=1
            datatype=[]
        n.close()

        # create .data file
        m=open(self.datafile,"w")
        for d in alldata[1:]:
            m.write(",".join(d)+"\n")
        m.close()


# See5("csv1.csv","see51.names","see51.data","city").generate_see5()
