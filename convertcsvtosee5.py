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
        # print(self.target+"\t"*3+"| the target attribute"+"\n")
        n.write(self.target+"\t"*3+"| the target attribute"+"\n"*2)

        attributes = alldata[0]

        data=[]
        for item in alldata[1:]:
            for x in range(len(attributes)):
                if len(item[x])==0:
                    item_x="?"
                else:
                    item_x=str(item[x])
                data+=[item_x,]
        # print(data)
        # print(type(data))
        datatype=[]
        for w in range(len(attributes)):
            for y in range(w,len(data),len(attributes)):
                datatype+=[data[y],]
            datatype=list(sorted(set(datatype)))
            try:
                t="+"
                datacheck=eval(str(t.join(datatype)).strip("~!@#$%^&*(),./;'[]\<>-=_+{}|:<>? "))
                # print(attributes[w]+"\t\t"+"continuous.")
                n.write(attributes[w]+"\t"*2+"continuous."+"\n")
            except:
                if "?" in datatype:
                    datatype.remove("?")

                if len(datatype)>=10:
                    # print(attributes[w]+"\t\t"+"label.")
                    n.write(attributes[w]+"\t"*2+"label."+"\n")
                else:
                    # print(attributes[w],end="\t\t")
                    n.write(attributes[w]+"\t"*2)
                    # for q in range(len(datatype)-1):
                    #     print(datatype[q]+",",end="")
                    #     n.write(datatype[q]+",")
                    # print(datatype[-1]+".")
                    # n.write(datatype[-1]+".\n")
                    # print(",".join(datatype)+".")
                    n.write(",".join(datatype)+".\n")
            w+=1
            datatype=[]
        n.close()

        # create .data file
        m=open(self.datafile,"w")
        for d in alldata[1:]:
            # for e in range(len(d)-1):
            #     print(d[e]+",",end="")
            #     m.write(d[e]+",")
            # print(d[-1])
            # m.write(d[-1]+"\n")
            # print(type(d))
            for dd in range(len(d)):
                # print(type(d[dd]))
                if len(d[dd])==0:
                    d[dd]="?"
                elif "%" in d[dd]:
                    d[dd]=str(eval(d[dd].strip("%"))/100)

            # print(",".join(d))
            m.write(",".join(d)+"\n")

        m.close()


# See5("csv1.csv","see51.names","see51.data","city").generate_see5()
# See5("csv4.csv","csv4.names","csv4.data","city").generate_see5()
# See5("mergedcsv13.csv","mergedcsv13.names","mergedcsv13.data","city").generate_see5()
# See5("anatesting.csv","anatesting.names","anatesting.data","Group").generate_see5()
# See5("test_merge.csv","test2.names","test2.data","pred").generate_see5()

