import itertools
import os
PATHCSVFOLDER="C:\\Users\\mario\\OneDrive\\Documenti\\GitHub\\evoport\\stock\\WEEK\\AAPL.csv"

path=os.path.dirname(PATHCSVFOLDER)
#path=path[:5]
print(path)

num1=1
num2=2

try:
    if(num1!=num2):
        raise Exception("need num1=num2")
except Exception as e:
    print(e)




import os
if os.name == 'nt':
    import win32api, win32con
def file_is_hidden(p):
    if os.name== 'nt':
        attribute = win32api.GetFileAttributes(p)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return p.startswith('.') #linux-osx


sss=0.00487252686151365+0.011508394195790098
print(sss)