import re
str="@SP"
str=str.upper()
str=str.replace("SP","R6")
str=str.replace("PC","R7")
autoIncrement=re.fullmatch("i\((R[0-9])\)\+",str)
autoDecrement=re.fullmatch("\-\(R[0-9]\)",str)
direct=re.fullmatch("R[0-9]$",str)
indexed=re.fullmatch("[^@-]\(R[0-9]\)",str)
autoIncrementIndirect=re.fullmatch("@\(R[0-9]\)\+",str)
autoDecrementIndirect=re.fullmatch("@\-\(R[0-9]\)",str)
directIndirect=re.fullmatch("@R[0-9]",str)
indexedIndirect=re.fullmatch("@[^-]+\(R[0-9]\)",str)
print(autoIncrement)
print(autoDecrement)
print(direct)
print(indexed)
print(autoIncrementIndirect)
print(autoDecrementIndirect)
print(directIndirect)
print(indexedIndirect)