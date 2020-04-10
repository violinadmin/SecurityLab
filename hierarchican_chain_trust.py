#import Tkinter as tk
import tkinter as tk

### -------------------------- Window ----------------------- ###

mainWindow=tk.Tk()
mainWindow.title("Trust chain")
heading_label=tk.Label(mainWindow,text="Trust chain",padx=(10),pady=(20))
heading_label.pack()
heading_label=tk.Label(mainWindow,text="Enter user name (Anna, Bob, Polina, Alina):")
heading_label.pack()
first_field=tk.Entry(mainWindow)
first_field.pack()
operation=tk.Label(mainWindow,text="Action:")
operation.pack()


### ------------------------- Trust chain ------------------------ ###

#handle = open("key") # Get key for vernam from file
#key = handle.read()
trust_ch = {
    "Anna" : "NSTU",
    "Bob" : "MTI",
    "Alina" : "NSU",
    "Polina" : "VHO",
    "NSTU" : "Russian Federation",
    "MTI" : "USA",
    "VHO" : "USA",
    "NSU" : "Russian Federation"}

def get_chainn():
    username=first_field.get()
    result=get_chain(username)
    result_label.config(text="Chain is:" +str(result))

encryption_button=tk.Button(mainWindow,text="Get chain",command=lambda:get_chainn())
encryption_button.pack()


def get_rooot():
    username=first_field.get()
    result=get_root(username)
    result_label.config(text="Root certificate is:" +str(result))

decryption_button=tk.Button(mainWindow,text="Get root sertificate name", command=lambda:get_rooot())
decryption_button.pack()

def get_root(user):
    output=trust_ch[trust_ch[user]]
    return output

def get_chain(user):
    output=user+"-->"+trust_ch[user]+"-->"+trust_ch[trust_ch[user]]
    return output

### ---------------- End Vernam ---------- ###

### --------------- DES3 ----------------- ###

### ---------------------------------------###

result_label=tk.Label(mainWindow, text="operations result is:")
result_label.pack()
mainWindow.mainloop()
