import re
def ReadFile(path):
    f = open("test.txt", "r")
    txt=f.read()
    txt=txt.upper()
    return txt

def HandleComments(txt):
    Lines = txt.splitlines()
    for line in Lines:
        x=line.find(';')
        if(x!=-1):
            line=line[:x]
            line=line.strip()
        if(line!=''):    
            LinesNoComments.append(line)

def GetVariablesName(Lines):
    for line in Lines:
        x=line.find('DEFINE')
        if(x!=-1):
            l=re.split(' ',line)
            Variables[l[1]]=l[2]

def DetectLabels(line):
    global Address      
    x=line.find(':')
    if(x!=-1):                      #Label
        LabelVariables[line[:x]]={"Address":Address,"Value":'$'}
        line=line[x+1:]
        line=line.strip()
    return line        

def SplitInstruction(line):
    x=line.replace(',',' ')
    l=re.split('\s+',x)
    return l


def DetectVariables(line):
    global Address    
    x=False  
    Pc=""
    for var in Variables:
        if(len(line)>2):
            if(re.fullmatch(var,line[1]) and not re.fullmatch('DEFINE',line[0]) ):
                Pc=var
                line[1] ='X(R7)'
                x=True
            elif(line[1].find('#')!=-1 and not re.fullmatch('DEFINE',line[0]) ):
                Pc=line[1][1:]
                line[1] ='(R7)+'
                x=True
            if(re.fullmatch(var,line[2]) and not re.fullmatch('DEFINE',line[0])):
                Pc=var
                line[2] ='X(R7)'
                x=True
            elif(line[2].find('#')!=-1 and not re.fullmatch('DEFINE',line[0])):
                Pc=line[2][1:]
                line[2] ='(R7)+'
                x=True
    return line,x,Pc            

def GetAddresses(Lines):
    global Address    
    for line in Lines:
        #Detect Label 
        line=DetectLabels(line)
        if(line==''):
            continue

        #SplitLine
        SplittedLine=SplitInstruction(line)

        #Detect Variables 
        FormattedLine,Check,Pc=DetectVariables(SplittedLine)
        if(FormattedLine[0].find('DEFINE')!=-1):
            LabelVariables[FormattedLine[1]]={"Address":Address,"Value":FormattedLine[2]}

        if(Check):
            if(FormattedLine[0].find('DEFINE')==-1 and re.findall("\d", Pc)):
                ImportantLines.append(FormattedLine)
                ImportantLines.append(int(Pc))
            elif(FormattedLine[0].find('DEFINE')==-1):
                ImportantLines.append(FormattedLine)
                ImportantLines.append(Pc)    
            Address+=2
        else:
            if(FormattedLine[0].find('DEFINE')==-1 ):
                ImportantLines.append(FormattedLine)
            Address+=1  

def ReplaceVariables(lines):
    for line in range(0,len(lines)):
        if (not isinstance(lines[line], list) and isinstance(lines[line], str)): 
            lines[line]=LabelVariables[lines[line]]['Address']-line
    return lines        

Address=0    
txt=ReadFile("BlaBla")
LinesNoComments=[]
HandleComments(txt)
Variables={}
GetVariablesName(LinesNoComments)
LabelVariables={}
ImportantLines=[]
NoComma=[]
GetAddresses(LinesNoComments)
SemiFinalRam=ReplaceVariables(ImportantLines)
print(SemiFinalRam)