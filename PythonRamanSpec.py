import matplotlib.pyplot as plt #import matplotlib for plot the equation
import os
import csv
import cPickle as pickle
folders={}

def RSI(filename): #raman Xantus-1 spectrum instance generator
    instance = SR()
    instance.raman_X1converter(filename)
    return instance

def processfolder(folderpath,name=None):
    folder=os.listdir(folderpath)
    foldername=os.path.basename(folderpath)
    acceptedformat=['.csv','.txt'] #list of accepted file format
    spectra={}
    for i in folder:
        if os.path.splitext(i)[1] in acceptedformat:
            spectra[os.path.splitext(i)[0]]=RSI(folderpath+'/'+i)
    return spectra
    
def saveobject(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output,-1)

def loadobject(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

class SR:
    def __init__(self):
        #INFO ABOUT SPECTROMETER USED
        self.SpectrometerName='n.d'
        self.SN='n.d.'#serial number of the instrument
        self.manufacturer='n,d'
        self.laserwavelenght='n.d.' #this in nm
        
        #INFO ABOUT SPECTRUM
        self.SpettroXY=[] #list where are sotred the [[X,Y]] values of the spectra
        self.Pixel_Count='n.d.'
        self.Peak_Count='n.d.'
        self.Integration_Time='n.d.' #this should be in ms
        self.Average='n.d.' #number of spectra used to gt the spectra
        self.Noise_Threshold='n.d.'
        self.Sensor_Mode='n.d.'
        self.Case_Temperature='n.d.' #this should be ielsius
        self.Sensor_Temperature='n.d.'
        self.Peaks_List=[]
        self.file_Path='n.d.'
     
                                    
    def raman_X1converter(self,nomefileinput):
        self.file_Path=nomefileinput
        self.SpectrometerName="Xantus-1"
        self.manufacturer="BaySpec"
        self.laserwavelenght=785.59
        with open(nomefileinput,"r") as s:
                        spettro= [i.strip().split(',') for i in s.readlines()]
                        if spettro[0][0]=='SN:':
                            self.Integration_Time=spettro[1][1].strip()
                            self.Average=spettro[4][1].strip()
                            self.Sensor_Mode=spettro[6][1].strip()
                            self.Case_Temperature=spettro[7][1].strip()
                            self.Sensor_Temperature=spettro[8][1].strip()


                            for i in spettro[10:]:
                                if i !=['Peak_Raman_Shift(cm^-1)', ' Peak_Intensity(Count)']:
                                    self.SpettroXY.append(i)                                
                                else:
                                    break
        
                        else:
                            self.SpettroXY=spettro#questo e' solo nel caso lo spettro fosse gia' stato elaborato    


    
    def plot(self):
		if self.SpettroXY=='n.d.':
			print "No spectra data loaded!"
	        else:
		        Y=[float(i[1]) for i in self.SpettroXY]
		        X=[float(i[0]) for i in self.SpettroXY]
		        fig = plt.figure()
		        ax = fig.add_subplot(111)
		        ax.plot(X,Y,label="prova") #plot the function
		        plt.title(os.path.splitext(os.path.basename(self.file_Path))[0])
		        plt.xlim(min(X) * 0.9, max(X) * 1.1)
		        plt.ylim(min(Y) * 0.9, max(Y) * 1.2)
		        #plt.legend(loc=1, ncol=1, shadow=True)
		        plt.ylabel(r'Counts')
		        plt.xlabel(r'Raman shift $(cm^{-1})$')
										
    def PA(self):#Peak Analyzer of raman spectra 
        if self.SpettroXY=='n.d.':
			print "No spectra data loaded!"
        else:
		        Y=[float(i[1]) for i in self.SpettroXY]
		        X=[float(i[0]) for i in self.SpettroXY]
		        fig = plt.figure()
		        ax = fig.add_subplot(111)
		        ax.plot(X,Y,label="prova") #plot the function
		        plt.title(os.path.splitext(os.path.basename(self.file_Path))[0])
		        plt.xlim(min(X) * 0.9, max(X) * 1.1)
		        plt.ylim(min(Y) * 0.9, max(Y) * 1.2)
		        #plt.legend(loc=1, ncol=1, shadow=True)
		        plt.ylabel(r'Counts')
		        plt.xlabel(r'Raman shift $(cm^{-1})$')
  
        Y=[float(i[1]) for i in self.SpettroXY]
        X=[float(i[0]) for i in self.SpettroXY]
        Diz=dict(zip(X,Y)) #create a dictionary that associeate X with Y
        PeaksList=[]
        Interval=[]
                   
        def onclick(event):
                                print 'Limite intervallo=%f'%(event.xdata)
                                Interval.append(event.xdata)
                                if len(Interval)%2==0:
                                    a=Interval[-2]
                                    print a
                                    b=Interval[-1]
                                    print b
                                    if b<a: #if the user selct first the highest value these statements 
                                        A=b
                                        B=a
                                    else:
                                        A=a
                                        B=b
                                    maxv=0
                                    picco=0
                                    for i in [ j for j in X if A<j<B] :
                                        if Diz[i]>maxv:
                                            maxv=Diz[i]
                                            picco=i      
                                    print "Interval: %f - %f  Peak at: %f " %(a,b,picco)
                                    PeaksList.append([picco,maxv])
                                    self.Peaks_List.append([picco,maxv])
                                    ax.annotate("%0.1f" %(picco), xy=(picco,maxv),  xycoords='data',
                                            xytext=(-10, 10), textcoords='offset points',
                                            arrowprops=dict(arrowstyle="->")
                                            )
                                    plt.draw()
        plt.show()       
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        
        
    def ramspan(self,nomefileinput):
        global extnomefile
        extnomefile=nomefileinput
        spettro=open(nomefileinput,"r")
        X=[float(i.split(",")[0]) for i in spettro]
        spettro.close()
        spettro=open(nomefileinput,"r") 
        Y=[float(i.split(",")[1][:-2]) for i in spettro]
        spettro.close()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(X,Y,label="prova") #plot the function
        plt.xlim(min(X) * 0.9, max(X) * 1.1)
        plt.ylim(min(Y) * 0.9, max(Y) * 1.2)
        #plt.legend(loc=1, ncol=1, shadow=True)
        plt.ylabel(r'Counts')
        plt.xlabel(r'Raman shift $(cm^{-1})$')
        Diz=dict(zip(X,Y)) #create a dictionary that associeate X with Y
        PeaksList=[]
        def onclick(xmin, xmax):
            print 'Interval: {0} - {1}'.format(xmin,xmax)
            peakY=0 #max Y value
            piccoX=0 #value of the X associate to the peak
            for i in [ j for j in X if xmin<j<xmax] :
                if Diz[i]>peakY:
                    peakY=Diz[i]
                    piccoX=i
            print "Peak at: %f " % piccoX
            PeaksList.append([piccoX,peakY])
            ax.annotate("picco", xy=(piccoX,peakY),  xycoords='data',
                    xytext=(-10, 10), textcoords='offset points',
                    arrowprops=dict(arrowstyle="->"))
            plt.draw()
                                    
        span = SpanSelector(ax, onclick, 'horizontal', useblit=True,rectprops=dict(alpha=0.5, facecolor='blue'))
        
        
    def printlatex(self):
        print r"%begining LaTeX code remember you need \usepackage{pgfplots} \usepackage{tikz}"
        p=os.path.splitext(self.file_Path)[0]
        p2='%sC.csv' %(os.path.basename(p))
#        with open(p2, 'w') as csvfile:
#                                    csvwriter = csv.writer(csvfile, delimiter=',')
#                                    csvwriter.writerows(self.SpettroXY)
#    
        print  r"\begin{figure}"
        print  r"\tikzset{pin distance=6pt, every pin edge/.style={<-,shorten >=-2pt,shorten <=-3pt}, every pin/.append style={font=\footnotesize}}"
        print  r"\begin{tikzpicture}"
        print  r"\begin{axis}[" 
        print  r"y tick label style={/pgf/number format/.cd,scaled y ticks = false,set thousands separator={},fixed},"
        print  r"x tick label style={/pgf/number format/.cd,scaled x ticks = false,set thousands separator={},fixed}, "
        print  r"ylabel={Conteggi}, xlabel={Raman Shift ($cm^{-1}$)},]"
        print  r" \addplot[line width = 0.5pt] table [mark=none,col sep=comma,] {%s};" %(p2)
        for i in self.Peaks_List:
            #print  r"\draw [<-] (axis cs:%f,%f)-- +(10pt,10pt) node[right] {%0.1f};"%(i[0],i[1],i[0])
            print  r"\node[font=\tiny,pin= above right:{ %i}] at (axis cs:%i,%i) {};"%(i[0],i[0],i[1])
        print  r"\end{axis}"
        print  r"\end{tikzpicture}"
        print  r"\caption{Spettro Raman campione ``%s'', tempo di integrazione %s ms lunghezza d'onda del laser %s nm. }" %(os.path.basename(p),self.Integration_Time,self.laserwavelenght)
        print  r"\label{fig:%s}" %(os.path.basename(p))
        print  r"\end{figure}"
        
    def savelatex(self):
        p=os.path.splitext(self.file_Path)[0]
        p2=p+'C.csv'
        n='\n'
        with open(p2, 'w') as csvfile:
                                    csvwriter = csv.writer(csvfile, delimiter=',')
                                    csvwriter.writerows(self.SpettroXY)    
        with open(p+'.tex','w') as f:
	                f.write(r"\begin{figure}"+n)
	                f.write(r"\tikzset{pin distance=6pt, every pin edge/.style={<-,shorten >=-2pt,shorten <=-3pt}, every pin/.append style={font=\footnotesize}}"+n)
	                f.write(r"\begin{tikzpicture}"+n)
	                f.write(r"\begin{axis}[" +n)
	                f.write(r"y tick label style={/pgf/number format/.cd,scaled y ticks = false,set thousands separator={},fixed},"+n)
	                f.write(r"x tick label style={/pgf/number format/.cd,scaled x ticks = false,set thousands separator={},fixed}, "+n)
	                f.write(r"ylabel={Conteggi}, xlabel={Raman Shift ($cm^{-1}$)},]"+n)
	                f.write(r" \addplot[line width = 0.5pt] table [mark=none,col sep=comma,] {%s};" %(p2)+n)
	                for i in self.Peaks_List:
	                    #f.write(r"\draw [<-] (axis cs:%f,%f)-- +(10pt,10pt) node[right] {%0.1f};"%(i[0],i[1],i[0])+n)
	                    f.write(r"\node[font=\tiny,pin= above right:{ %i}] at (axis cs:%i,%i) {};"%(i[0],i[0],i[1])+n)
	                f.write(r"\end{axis}"+n)
	                f.write(r"\end{tikzpicture}"+n)
	                f.write(r"\caption{Spettro Raman campione ``%s'', tempo di integrazione %s ms lunghezza d'onda del laser %s nm. }" %(os.path.basename(p),self.Integration_Time,self.laserwavelenght)+n)
	                f.write(r"\label{fig:%s}" %(os.path.basename(p))+n)
	                f.write(r"\end{figure}"+n)
                
    
    
    
        
    
       
