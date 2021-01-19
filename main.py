import re
def ReadFile(path):
    f = open(path, "r")
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
    if(re.fullmatch('JSR',line[0])):
        Pc=line[1]
        x=True
        return line,x,Pc
    if(len(line)>2):
        if(line[1].find('#')!=-1 and not re.fullmatch('DEFINE',line[0]) ):
                Pc=line[1][1:]
                line[1] ='(R7)+'
                x=True
        if(line[2].find('#')!=-1 and not re.fullmatch('DEFINE',line[0])):
                Pc=line[2][1:]
                line[2] ='(R7)+'
                x=True        


    for var in Variables:
        if(len(line)>2):
            if(re.fullmatch(var,line[1]) and not re.fullmatch('DEFINE',line[0]) ):
                Pc=var
                line[1] ='X(R7)'
                x=True
            
            if(re.fullmatch(var,line[2]) and not re.fullmatch('DEFINE',line[0])):
                Pc=var
                line[2] ='X(R7)'
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
        if(len(FormattedLine) >2):
            if(re.fullmatch("^\d*\(R[0-9]\)",FormattedLine[1])):
                t= FormattedLine[1].find("(")
                Pc=FormattedLine[1][0:t]
                ImportantLines.append(FormattedLine)
                ImportantLines.append(int(Pc))
                Address+=2
                Check=True
                continue
            if(re.fullmatch("^\d*\(R[0-9]\)",FormattedLine[2])):
                t= FormattedLine[2].find("(")
                Pc=FormattedLine[2][0:t]
                ImportantLines.append(FormattedLine)
                ImportantLines.append(int(Pc))
                Address+=2
                Check=True  
                continue
            if(re.fullmatch("@\d*\(R[0-9]\)",FormattedLine[1])):
                t= FormattedLine[1].find("(")
                Pc=FormattedLine[1][1:t]
                ImportantLines.append(FormattedLine)
                ImportantLines.append(int(Pc))
                Address+=2
                Check=True  
                continue
            if(re.fullmatch("@\d*\(R[0-9]\)",FormattedLine[2])):
                t= FormattedLine[2].find("(")
                Pc=FormattedLine[2][1:t]
                ImportantLines.append(FormattedLine)
                ImportantLines.append(int(Pc))
                Address+=2
                Check=True  
                continue
            


            


        if(FormattedLine[0].find('DEFINE')!=-1):
            LabelVariables[FormattedLine[1]]={"Address":Address,"Value":FormattedLine[2]}

        if(Check):
            if(FormattedLine[0].find('DEFINE')==-1 and FormattedLine[0].find('JSR')==-1 and re.findall("\d", Pc)):
                ImportantLines.append(FormattedLine)
                ImportantLines.append(int(Pc))

            elif(FormattedLine[0].find('DEFINE')==-1):
                ImportantLines.append(FormattedLine)
                if(FormattedLine[0].find('JSR')==-1):
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

def DetectModes(str):
    if(re.fullmatch("\(R[0-9]\)\+",str)):
        return "autoIncrement"
    if(re.fullmatch("\-\(R[0-9]\)",str)):
        return "autoDecrement"
    if(re.fullmatch("R[0-9]",str)):
        return "direct"
    if(re.fullmatch("[^@-]\(R[0-9]\)",str)):
        return "indexed"
    if(re.fullmatch("@\(R[0-9]\)\+",str)):
        return "autoIncrementIndirect"
    if(re.fullmatch("@\-\(R[0-9]\)",str)):
        return "autoDecrementIndirect"
    if(re.fullmatch("@R[0-9]",str)):
        return "directIndirect"
    if(re.fullmatch("@[^-]+\(R[0-9]\)",str)):
        return "indexedIndirect" 

def DetectRegister(str):
    x=re.search('R',str)
    first=x.span()[0]
    x=str[first:first+2]
    return x


get_bin = lambda x, n: format(x, 'b').zfill(n)
def GenerateOutPut(lines):
    for line in range(0,len(lines)):
        if (isinstance(lines[line], list)):
            if(lines[line][0] in Instructions.keys()):
                f.write(Instructions[lines[line][0]])
            else:
                print("Errooor!!")
            if(len(lines[line])==1):
                f.write('\n')         
                continue
            elif(len(lines[line])==2):
                if(re.fullmatch(("^B.*$"),lines[line][0])):
                    Offset=LabelVariables[lines[line][1]]['Address']-line
                    Offset=Offset & 0x3ff
                    f.write(get_bin(Offset, 10))
                elif(re.fullmatch(("JSR"),lines[line][0])):
                    Offset=LabelVariables[lines[line][1]]['Address']
                    Offset=Offset & 0xffff
                    f.write('0001110000\n')
                    f.write(get_bin(Offset, 16))    
                else:
                    f.write('0000')
                    f.write(Modes[DetectModes(lines[line][1])])
                    f.write(Registers[DetectRegister(lines[line][1])])    

            elif(len(lines[line])==3):
                f.write(Modes[DetectModes(lines[line][1])])
                f.write(Registers[DetectRegister(lines[line][1])]) 
                f.write(Modes[DetectModes(lines[line][2])])
                f.write(Registers[DetectRegister(lines[line][2])])    
        else:
            f.write(get_bin(lines[line]& 0xffff, 16))                       
            
        f.write('\n')         

def WriteVars():

    for var in LabelVariables:
        if (LabelVariables[var]['Value']) != '$':
            f.write(get_bin(int(LabelVariables[var]['Value']), 16))
            f.write('\n')           

            
Registers={
    "R0":"000",
    "R1":"001",
    "R2":"010",
    "R3":"011",
    "R4":"100",
    "R5":"101",
    "R6":"110",
    "R7":"111",
}
Modes={
    "direct":"000",
    "autoIncrement":"001",
    "autoDecrement":"010",
    "indexed":"011",
    "directIndirect":"100",
    "autoIncrementIndirect":"101",
    "autoDecrementIndirect":"110",
    "indexedIndirect":"111",
}
Instructions={
    "MOV":"0000",
    "ADD":"0001",
    "ADC":"0010",
    "SUB":"0011",
    "SBC":"0100",
    "AND":"0101",
    "OR":"0110",
    "XOR":"0111",
    "CMP":"1000",
    "INC":"100100",
    "DEC":"100101",
    "CLR":"100110",
    "INV":"100111",
    "LSR":"101000",
    "ROR":"101001",
    "ASR":"101010",
    "LSL":"101011",
    "ROL":"101100",
    "BR":"110000",
    "BEQ":"110001",
    "BNE":"110010",
    "BLO":"110011",
    "BLS":"110100",
    "BHI":"110101",
    "BHS":"110110",
    "HLT":"1110000000000000",
    "NOP":"1110010000000000",
    "RESET":"1110100000000000",
    "JSR":"111100",
    "RTS":"111101",
    "INT":"1111100000000000",
    "IRET":"1111110000000000",
    

}
Address=0    
#Enter Your file path. 
txt=ReadFile('c6.txt')
LinesNoComments=[]
HandleComments(txt)
Variables={}
GetVariablesName(LinesNoComments)
LabelVariables={}
ImportantLines=[]
NoComma=[]
GetAddresses(LinesNoComments)
SemiFinalRam=ReplaceVariables(ImportantLines)
f = open("c6Binary.txt", "w")
GenerateOutPut(SemiFinalRam)
WriteVars()