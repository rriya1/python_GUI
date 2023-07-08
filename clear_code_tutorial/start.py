import tkinter as tk
#from tkinter import ttk #all the widgets
import ttkbootstrap as ttk
from tkinter import font

#method to add functionality
def convert():
    miles=inputvar.get() #getiing the input from the input box varibale
    km=miles*1.61 #converting and stroing in a varibale
    outputvar.set(km)#updating the output varibale to display the answer

#window
window=ttk.Window( themename='darkly')#with ttkbootstrap we can use this command nstead of the below one
#window=tk.Tk()#creating a window
window.title('first project') #giving a title to the window
window.geometry('300x100') #string to define the widthxheight of the window

#widget
title_label=ttk.Label(master=window,
                      text='Miles to Km converter',
                      font='Verdana 15 bold'); #declared a text widget
title_label.pack() #to actually display the widget on master

#input widgets
inputvar=tk.IntVar() #variable to store value from widget
frame=ttk.Frame(master=window)
button=ttk.Button(master=frame, text='Convert', command=convert) #widget button
input=ttk.Entry(master=frame, textvariable=inputvar) #widget entry box


#packing the widgets
input.pack(side='left')
button.pack(side='left', padx=10)
frame.pack(pady=10)

##--------------------------------------##
#this was to view all the available font#
# font_list=list(font.families())
# print(font_list)
##--------------------------------------##

#output
outputvar=tk.StringVar() #variable to store string outputs
output_label=tk.Label(master=window, text='output', font='Verdana 12', textvariable=outputvar) #definifn output label and also connecting it to a string varibale
output_label.pack()

#run/display
window.mainloop() #mainloop to display the window