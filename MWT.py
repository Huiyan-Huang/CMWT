import os
import datetime
import glob
import sys


#scan a folder, found it 1st level subfolder, found the one containing useable data and extract date created, name of the line and the path to the folder.
def get_PDN(path):
        result=list()
        for item in os.listdir(path):
                subpath=os.path.join(path,item)
                if os.path.isdir(subpath):
                        os.chdir(subpath)
                        setfile=glob.glob("*.set")
                        if len(setfile)>0:
                                ctime=datetime.date.fromtimestamp(os.stat(setfile[0]).st_ctime)
                                Datalable=str(ctime.year)+str(ctime.month).zfill(2)+str(ctime.day).zfill(2)
                                result.append([subpath, Datalable, os.path.splitext(setfile[0])[0]])
                        else:
                                print "Data file incomplet, can't proceed"
        return result
#-----------------------------------------------------------------------------------
        
#main calulation body
def Dpause(input_file_path_name, sleep_time_thershold=10):

        data=list()
        lines=open(input_file_path_name).readlines()
        for item in lines:
                a=item.replace("\n","")
                if "NaN" not in a:
                        a=a.split(" ")
                        b=[float(jtem) for jtem in a]
                        data.append(b)
        
        length=len(data)-1
                        
        T_wake=list()
        T_stop=list()
        T_travel=0
        T_time=0
        A_speed=0
        T_total=0
        D_pause=list()
        D_pauseT=list() 
                
        if length>0:
                for i in range (1, length):
                        if data[i-1][5]==0 and abs(data[i][5])==1:
                                T_wake.append(data[i][3])
                        if data[i][5]==0 and abs(data[i-1][5])==1:
                                T_stop.append(data[i][3])
                        if abs(data[i][5])==1:
                                T_travel=T_travel+(data[i][3]-data[i-1][3])*data[i][1]
                                T_time=T_time+(data[i][3]-data[i-1][3])
                
                         
                if len(T_wake)*len(T_stop)==0:
                        D_pause=list()
                elif len(T_stop)>len(T_wake):
                        for j in range(len(T_wake)):
                                D_pause.append(T_wake[j]-T_stop[j])
                elif len(T_stop)<len(T_wake):
                        for j in range(len(T_stop)):
                                D_pause.append(T_wake[j+1]-T_stop[j])
                elif T_wake[0]-T_stop[0]>0:
                        for j in range(len(T_wake)):
                                D_pause.append(T_wake[j]-T_stop[j])
                else:
                        for j in range(len(T_wake)):
                                D_pause.append(T_stop[j]-T_wake[j])
                                
                
                for item in D_pause:
                        if item>=sleep_time_thershold:
                                D_pauseT.append(item)
                                
                T_total=data[-1][3]-data[0][3]
                A_speed=T_travel/T_time
                        
        return T_total, A_speed, sum(D_pauseT), len(D_pauseT), D_pauseT
#-----------------------------------------------------------------------------------

#Path_Data_Name has to provide the path, the time and the experiment name
def OutInput(Path_Date_Name, t=10, config=r"C:\CMWT\MWTconfig.txt"):
        f=open(config)
        command1=f.readline()
        command2=f.readline()
        command1=command1[:-1]
        command2=command2[:-1]
        f.close()
        
        t=float(t)
        
        for k in range(0, len(Path_Date_Name)):
                result=list()
                result.append(["Total_time","AVG_Speed","Total_pausing_time","No._pause","Dur_each_P"])
                path=Path_Date_Name[k][0]
                fnames=glob.glob(path+'/*.dat')
                outfn=Path_Date_Name[k][1]+Path_Date_Name[k][2]+'_'+str(t)+'result.txt'
                outfile=open(os.path.join(path,outfn), 'w')
                
                if len(fnames)==0:
                        command3=os.system(command1+' '+path+' '+command2)
                        fnames=glob.glob(path+'/*.dat')
                
                for item in fnames:
                        [x1,x2,x3,x4,x5]=Dpause(item,t)
                        x5.insert(0,x4)
                        x5.insert(0,x3)
                        x5.insert(0,x2)
                        x5.insert(0,x1)
                        result.append(x5)

                print>>outfile, '\t'.join(result[0])
                for i in range(1,len(result)):
                        for j in range(0, len(result[i])):
                                result[i][j]="%.4f" %result[i][j]
                        print>>outfile, '\t'.join(result[i])
                outfile.close()
#-----------------------------------------------------------------------------------

#Get all the result.txt files and put their paths to a list
def Get_Result(Rootpath):
        filelist=list()
        walktree(Rootpath, filelist.append)
        
        for i in range(0, len(filelist)):
                if 'result.txt' not in filelist[i]:
                        filelist[i]=''
                        
        filelist=list(set(filelist))
        filelist=filter(None, filelist)
        return filelist
#-----------------------------------------------------------------------------------

#Make a new class to deposit data
class Wormpause:
    def __init__(self,TotalT,AvgS,TotalP,NoP):
            self.TotalT=TotalT
            self.AvgS=AvgS
            self.TotalP=TotalP
            self.NoP=NoP
    def __repr__(self):
            return repr((self.TotalT, self.AvgS, self.TotalP, self.NoP))
#-----------------------------------------------------------------------------------

#Walk though a directory and run callback function on each files.
def walktree(top, callback):
        for f in os.listdir(top):
                pathname=os.path.join(top,f)
                if os.path.isdir(pathname):
                        walktree(pathname, callback)
                elif os.path.isfile(pathname):
                        callback(pathname)
                else:
                        print 'Skipping %s' % pathname
#-----------------------------------------------------------------------------------

#Get the summary output
def Out_summary(Rootpath):
        outfile=open(os.path.join(Rootpath,"summary.txt"), 'a')
        print>>outfile, '\t'.join(["Filename", "SumTotalT", "SumAvgS", "SumTotalP", "SumNoP", "SumNo", "SumNoZero", "AvgTotalT", "AvgSumAvgS", "AvgSumTotalP", "AvgSumNoP"])
        filelist=Get_Result(Rootpath)
        for j in range(0, len(filelist)):
                f=open(filelist[j])
                resultl=list()
                f.readline()
                for line in f:
                        a=line.split("\t")
                        resultl.append(Wormpause(a[0],a[1],a[2],a[3]))
                f.close()
                
                [SumTotalT, SumAvgS, SumTotalP, SumNoP, SumNo, SumNoZero]=[0,0,0,0,0,0]
                for i in range(0, len(resultl)):                            
                        if resultl[i].TotalT=="0.0000":                     
                                SumNoZero+=1                                
                        else:                                               
                                SumTotalT=SumTotalT+float(resultl[i].TotalT)
                                SumAvgS=SumAvgS+float(resultl[i].AvgS)      
                                SumTotalP=SumTotalP+float(resultl[i].TotalP)
                                SumNoP=SumNoP+float(resultl[i].NoP)         
                                SumNo=SumNo+1                        
                
                AvgTotalT=SumTotalT/SumNo
                AvgSumAvgS=SumAvgS/SumNo  
                AvgSumTotalP=SumTotalP/SumNo
                AvgSumNoP=SumNoP/SumNo
                
                result=[SumTotalT, SumAvgS, SumTotalP, SumNoP, SumNo, SumNoZero, AvgTotalT, AvgSumAvgS, AvgSumTotalP, AvgSumNoP]
                
                for i in range(0, len(result)):
                        if i<6:
                                result[i]=str(result[i])
                        else:
                                result[i]="%.4f" %result[i]
                                
                result.insert(0,filelist[j].split("\\")[-1][:-10])
                print>>outfile, '\t'.join(result)
        outfile.close()
#-----------------------------------------------------------------------------------            
if len(sys.argv)<2:
        print ""
        print "   This is a program to calculate multiworm tracker experiment data"
        print "   This is the full version, will generate the .DAT file from image files."
        print "   If .DAT files already generated, it will use the generated .dat files"
        print "without replacing them. In case new .dat should be generate, you should "
        print "DELETE all the previously generated .dat files."
        print "   Do remember to close the jump up Choregraphy window otherwise the analysis"
        print "result files may not be generated."
        print "====================================="
        print "Usage: MWT <path> <time thershold>"
        print "OR:"
        print "Usage: MWT <path>"
        print "====================================="
        print "   <path>: full path to where .dat files are WITHOUT FINAL", "\\","!!"
        print "e.g: K:\\Folder\\20120223_151715"
        print "   <time thershold>: if a worm stops for a duration less than it"
        print "it will not be consider as paused. Unit: seconds"
        print "   If <time thershold> is omitted, default value is 10 seconds."
        print ""
        print "C-T Zhu, 2012/2/27"
else:
	Start_Path=sys.argv[1]	
	#Start_Path=r"F:\MWT"
	if len(sys.argv)>2:
                t=float(sys.argv[2])
       	else:
                t=10.0
	PDN=get_PDN(Start_Path)
	OutInput(PDN, t)
	Out_summary(Start_Path)
