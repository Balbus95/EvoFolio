import pickle
import os
from deap import creator, base, tools

# stats=pickle.load(open("stats_NGEN=10_CXPB=0.9_SELPARAM=0.8_TOURNPARAM=0.9_MU=48.dump","rb"))
# print(type(stats[0]))

# guadagni=pickle.load(open("guadagni.dump","rb"))
# print(guadagni[0])
# listmax=[]
# listmin=[]
# for i in stats:
#     gen, max, min = i.select("gen", "max", "min")
#     #print(max)
#     #print(max[0][0])
#     listmin.append(min)
#     listmax.append(max)
#     print(str(gen),' ',str(max))
#     #print(i)

# # grafico(min,max)
    
# Import Tkinter library
from tkinter import *

root = Tk()
root.geometry("700x250")
FileTypesList = ['.insv', '.insp', '.dng', '.docx', '.jpg']
checkboxes = {}

def ShowCheckBoxes(FileTypesList):
    Cbcolumn = 0
    Cbrow = 8
    Chkcount = 0

    for Checkbox in range(len(FileTypesList)):
        name = FileTypesList[Checkbox]
        current_var = IntVar()
        current_box = Checkbutton(root, text=name, variable=current_var)
        current_box.var = current_var
        current_box.grid(row=Cbrow, column=Cbcolumn)
        checkboxes[current_box] = name  # so checkbutton object is the key and value is string
        if Cbcolumn == 2:
            Cbcolumn = 0
            Cbrow += 1
        else:
            Cbcolumn += 1
        Chkcount += 1

def get_checked_boxes():
    output = []
    for box in checkboxes:
        if box.var.get() == 1:
            output.append(checkboxes[box])
    print(output)  # debug
    return output

print_cbox_button = Button(root, text='Print checked checkedboxes', command=get_checked_boxes)
print_cbox_button.grid(row=10, column=0, columnspan=3)

ShowCheckBoxes(FileTypesList)

root.mainloop()