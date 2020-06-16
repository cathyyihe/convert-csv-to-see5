import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilenames
import tkinter.messagebox
import os
import pandas
import time
# import shutil

from convertcsvtosee5 import See5
from convertcsvtoarff import Arff


statusshow=""
alldf=[]
exetime=str(time.time())
tempcsv=exetime+"new.csv"

def cleandata(path_1):
    global tempcsv
    global templocation
    alldf=[]
    for path in path_1:
        df=pandas.read_csv(path).fillna("?")
        alldf.append(df)
    mergedf=pandas.concat(alldf,ignore_index=True)
    cleandf=mergedf.drop_duplicates().T.drop_duplicates().T
    cleandfm=cleandf.fillna("?")
    cleandfm.to_csv(tempcsv,index=False)
    templocation=os.path.abspath(tempcsv)

def selectpath():
    widget8.delete(0,"end")
    global tempcsv
    global csvname
    global csvfile
    path_1=askopenfilenames(filetypes =[("CSV Files","*.csv")])
    # path_1=askopenfilenames(filetypes =(("CSV Files","*.csv"),))
    path1.set(path_1)
    csvname=path_1
    cleandata(path_1)
    global attribute_from_csv
    global attr
    listbox_read=open(tempcsv,"r")
    attribute_from_csv=listbox_read.readline().split(",")
    for item in tuple(attribute_from_csv):
        attr=item
        widget8.insert("end",attr)
    listbox_read.close()

def savepath():
    global savedict
    path_2=askdirectory()
    savedict=path_2
    path2.set(path_2)

def selectall():
    global statusshow
    statusshow="all attributes are selected"
    status["text"]=statusshow
    widget8.select_set(0,"end")

def unselectall():
    global statusshow
    statusshow="unselect all the attributes"
    status["text"]=statusshow
    widget8.selection_clear(0, "end")

def submit1():
    global tempcsv
    global templocation
    global exetime
    global savedict
    try:
        return savedict
    except:
        tk.messagebox.showerror("error","Please choose where you want to save the files.")
    finally:
        fileToWrite = str(savedict+"/"+tempcsv[len(exetime):-4]+".arff")
        basename=str(os.path.basename(fileToWrite))
        Arff(tempcsv,fileToWrite).generate_arff()
        global attribute_from_csv
        if len(widget8.curselection())==0:
            k=open(fileToWrite,"w")
            k.write("@relation " + basename[:-5] + "\n\n")
            k.write("@attribute" + " " + "?" + " " + "numeric" + "\n")
            k.write("\n@data\n")
            k.write("?"+"\n")
            k.close()
            try:
                os.rename(fileToWrite,savedict+"/"+basename[:-5]+"_empty.arff")
            except:
                os.remove(savedict+"/"+basename[:-5]+"_empty.arff")
                os.rename(fileToWrite,savedict+"/"+basename[:-5]+"_empty.arff")
        if 0<len(widget8.curselection())<len(attribute_from_csv):
            try:
                os.rename(fileToWrite,"temp.arff")
            except:
                os.remove("temp.arff")
                os.rename(fileToWrite,"temp.arff")
            o= open("temp.arff","r+")
            oldlines=o.readlines()
            p=open(fileToWrite,"w")
            p.write(oldlines[0])
            p.write("\n")
            for q in widget8.curselection():
                p.write(oldlines[q+2])
            p.write("\n"+"@data"+"\n")
            olddata=oldlines[oldlines.index("@data\n")+1:]
            for u in olddata:
                u=u[:-1].split(",")
                for v in range(0,len(u))[::-1]:
                    if v not in widget8.curselection():
                        del(u[v])
                p.write(",".join(u)+"\n")
            o.close()
            p.close()
            try:
                os.rename(fileToWrite,savedict+"/"+basename[:-5]+"_part.arff")
            except:
                tk.messagebox.showerror("error","File is existed, new file will override it.")
                os.remove(savedict+"/"+basename[:-5]+"_part.arff")
                os.rename(fileToWrite,savedict+"/"+basename[:-5]+"_part.arff")
            os.remove("temp.arff")
        if len(widget8.curselection())==len(attribute_from_csv):
            try:
                os.rename(fileToWrite,savedict+"/"+basename[:-5]+"_all.arff")
            except:
                tk.messagebox.showerror("error","File is existed, new file will override it.")
                os.remove(savedict+"/"+basename[:-5]+"_all.arff")
                os.rename(fileToWrite,savedict+"/"+basename[:-5]+"_all.arff")
        os.remove(templocation)
        global statusshow
        statusshow="csv has been converted to arff."
        status["text"]=statusshow
        tk.messagebox.showinfo("result",statusshow)
        global win1
        win1.destroy()

def submit2():
    global tempcsv
    global templocation
    global exetime
    global savedict
    try:
        return savedict
    except:
        tk.messagebox.showerror("error","Please choose where you want to save the files.")
    finally:
        namesfile = str(savedict+"/"+tempcsv[len(str(exetime)):-4]+".names")
        datafile = str(savedict+"/"+tempcsv[len(str(exetime)):-4]+".data")
        target=widget14.get()
        if target=="":
            w1=tk.messagebox.showwarning("warning","No target attribute")
        See5(tempcsv,namesfile,datafile,target).generate_see5()
        global attribute_from_csv
        if len(widget8.curselection())==0:
            with open(savedict+"/"+str(tempcsv[len(str(exetime)):-4]+"_empty.names"),"w"):pass
            with open(savedict+"/"+str(tempcsv[len(str(exetime)):-4]+"_empty.data"),"w"):pass
        if 0<len(widget8.curselection())<len(attribute_from_csv):
            o= open(namesfile,"r+")
            oldlines=o.readlines()
            p=open("temp.names","w")
            for head in range(1):
                p.write(oldlines[head]+"\n")
            for q in widget8.curselection():
                if q>-1:
                    p.write(oldlines[q+2])
                else:
                    p.write(oldlines[len(attribute_from_csv)+q+2])
            o.close()
            p.close()
            os.remove(namesfile)

            s= open(datafile,"r+")
            olddata=s.readlines()
            t=open("temp.data","w")
            for u in olddata:
                u=u[:-1].split(",")
                for v in range(0,len(u))[::-1]:
                    if v not in widget8.curselection():
                        del(u[v])
                t.write(",".join(u)+"\n")
            s.close()
            t.close()
            os.remove(datafile)
            try:
                os.rename("temp.data",savedict+"/"+tempcsv[len(exetime):-4]+"_part.data")
                os.rename("temp.names",savedict+"/"+tempcsv[len(exetime):-4]+"_part.names")
            except:
                tk.messagebox.showerror("error","File is existed, new file will override it.")
                os.remove(savedict+"/"+tempcsv[len(exetime):-4]+"_part.names")
                os.remove(savedict+"/"+tempcsv[len(exetime):-4]+"_part.data")
                os.rename("temp.names",savedict+"/"+tempcsv[len(exetime):-4]+"_part.names")
                os.rename("temp.data",savedict+"/"+tempcsv[len(exetime):-4]+"_part.data")
        if len(widget8.curselection())==len(attribute_from_csv):
            try:
                os.rename(namesfile,savedict+"/"+str(tempcsv[len(str(exetime)):-4]+"_all.names"))
                os.rename(datafile,savedict+"/"+str(tempcsv[len(str(exetime)):-4]+"_all.data"))
            except:
                tk.messagebox.showerror("error","File is existed, new file will override it.")
                os.remove(savedict+"/"+str(tempcsv[len(str(exetime)):-4]+"_all.names"))
                os.remove(savedict+"/"+str(tempcsv[len(str(exetime)):-4]+"_all.data"))
                os.rename(namesfile,savedict+"/"+str(tempcsv[len(str(exetime)):-4]+"_all.names"))
                os.rename(datafile,savedict+"/"+str(tempcsv[len(str(exetime)):-4]+"_all.data"))
                # shutil.move(str(tempcsv[len(str(exetime)):-4]+"_all.data"),savedict+"/"+str(tempcsv[len(str(exetime)):-4]+"_all.data"))
        os.remove(templocation)

        global statusshow
        statusshow="csv has been converted to see5 files (.names and .data)."
        status["text"]=statusshow
        tk.messagebox.showinfo("result",statusshow)
        global win1
        win1.destroy()

##################################################################################################################

win1 = tk.Tk()
win1.title("Support Tool")
win1.geometry()
win1.resizable(width="false",height="false")


widget1= tk.Label(win1, text="Support Tool",height=3,font=20)
widget1.grid(row=3,column=0,columnspan=9,sticky="nsew")


widget2= tk.Label(win1, text="Import from:",width=11,height=1,justify="right")
widget2.grid(row=5,column=0,sticky="w")

path1=tk.StringVar()
widget3= tk.Entry(win1,textvariable=path1)
widget3.grid(row=5,column=1,columnspan=7,sticky="we")

widget4= tk.Button(win1,font=("courier",10),text="open",width=11,command=selectpath)
widget4.grid(row=5,column=8,columnspan=1,sticky="e")

widget5= tk.Label(win1, text="Export to:",width=11,height=1,justify="right")
widget5.grid(row=7,column=0,columnspan=1,sticky="w")

path2=tk.StringVar()
widget6= tk.Entry(win1,textvariable=path2)
widget6.grid(row=7,column=1,columnspan=7,sticky="we")

widget7= tk.Button(win1,font=("courier",10),text="select",width=11,command=savepath)
widget7.grid(row=7,column=8,columnspan=1,sticky="e")

frame4= tk.Frame(win1)
frame4.grid(row=9,column=0,columnspan=9,rowspan=1)

v=tk.IntVar()
option1= tk.Radiobutton(frame4,text="select all",variable=v,value=1,command=selectall)
option1.grid(row=9,column=0)
option2= tk.Radiobutton(frame4,text="unselect all",variable=v,value=2,command=unselectall)
option2.grid(row=9,column=1)

frame5= tk.Frame(win1)
frame5.grid(row=10,rowspan=2,columnspan=9)

widget8= tk.Listbox(frame5,selectmode="extended",justify="center")
widget8.grid(row=11,column=0,columnspan=9,sticky="we",ipady=9,ipadx=9)

yscrollbar= tk.Scrollbar(frame5)
yscrollbar.configure(command=widget8.yview)
widget8.configure(yscrollcommand=yscrollbar.set)
yscrollbar.grid(row=11,column=9,sticky="ns",pady=9)

widget15= tk.Label(win1, text="Please input target attribute for see5:",height=2)
widget15.grid(row=15,column=0,columnspan=2,sticky="nsew")
widget14= tk.Entry(win1)
widget14.grid(row=15,column=5,columnspan=5,sticky="we")

widget9= tk.Button(win1,font=("courier",10),text="cancel",width=11,height=2,command=win1.quit)
widget9.grid(row=20,column=0,sticky="w")
widget10= tk.Label(win1,font=("courier",10),text="",width=11,height=2)
widget10.grid(row=20,column=1,sticky="w")

widget12= tk.Button(win1,font=("courier",10),text="convert to:\nARFF",width=11,height=2,command=submit1)
widget12.grid(row=20,column=7,sticky="e")
widget13= tk.Button(win1,font=("courier",10),text="convert to:\nsee5",width=11,height=2,command=submit2)
widget13.grid(row=20,column=8,sticky="e")

status=tk.Label(win1,text=statusshow) #,bg="red",fg="white")
status.grid(row=100,columnspan=9,sticky="w")

win1.mainloop()

if os.path.exists(tempcsv):
    os.remove(tempcsv)

