from tkinter import *
from tkinter import filedialog,messagebox
import tkinter
import os
import logging as log


win=Tk()
#win.wm_iconbitmap("notepad.png")
win.title("Untitled - Notepad")
win.geometry("550x470+450+300")

#Text area
textarea=Text(win)
textarea.config(wrap="word",relief=FLAT)

#scrollbar

scrollbar=Scrollbar(win)
textarea.focus_set()
scrollbar.pack(side=RIGHT,fill=Y)
textarea.pack(expand=True,fill=BOTH)
scrollbar.config(command=textarea.yview)
textarea.config(yscrollcommand=scrollbar.set)

# status bar
statusbars=Label(win,text="Status bars")
statusbars.pack(side=BOTTOM)

textchange=False

def statusword(event=None):
    global textchange
    if textarea.edit_modified():
        textchange=True
        word=len(textarea.get(1.0,"end-1c").split())
        character=len(textarea.get(1.0,"end-1c").replace(" ",""))
        statusbars.config(text=f" Status                    character :{character}word :{word}        Developer Name : Ankit sharrma")
    textarea.edit_modified(False)
textarea.bind("<<Modified>>",statusword)

#MenuBar
menubar=Menu(win)
filemenu=Menu(menubar, tearoff = 0)
menubar.add_cascade(label="File",menu=filemenu)

textwrite=" "
def newfile(event=None):
    global textwrite
    textwrite=" "
    textarea.delete(1.0,END)
win.bind("<Control-n>",newfile)    
filemenu.add_command(label="New",command=newfile,compound=LEFT,accelerator="Ctrl+N")

def windowfile():
    top=Toplevel()


win.bind("<Control-Shift-n>",windowfile)
filemenu.add_command(label="New Window",command=windowfile,compound=LEFT,accelerator="Ctrl+Shift+N")

def openfile(envent=None):
    global textwrite
    textwrite=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open file",filetypes=(("Text file","*.txt"),("All files","*.*")))
    try:
        with open(textwrite,"r") as forread:
            textarea.delete(1.0,END)
            textarea.insert(1.0,forread.read())
    except FileNotFoundError:
        return
    except:
        return
    win.title(os.path.basename(textwrite))
    
win.bind("<Control-o>",openfile)
filemenu.add_command(label="Open",command=openfile,compound=LEFT,accelerator="Ctrl+O")

def savefile(event=None):
    global textwrite
    try:
        if textwrite:
            content=str(textarea.get(1.0,END))
            with open(textwrite,"w",encoding="utf-8")as forwrite:
                forwrite.write(content)
        else:
            textwrite=filedialog.asksaveasfile(mode="w",defaultextension=".txt",filetypes=(("Text file","*.txt"),("All files","*.*")))
            content2=textarea.get(1.0,END)
            textwrite.write(content2)
            textwrite.close()
    except:
        return
win.bind("<Control-s>",savefile)
filemenu.add_command(label="Save",command=savefile,compound=LEFT,accelerator="Ctrl+S")

def saveasfile(event=None):
    global textwrite
    try:
        content=str(textarea.get(1.0,END))
        textwrite=filedialog.asksaveasfile(mode="w",defaultextension=".txt",filetypes=(("Text file","*.txt"),("All files","*.*")))
        textwrite.write(content)
        textwrite.close()
    except:
        return

filemenu.add_command(label="SaveAs",command=saveasfile,compound=LEFT,accelerator="Ctrl+Shift+S")
filemenu.add_separator()
filemenu.add_command(label="Page Setup",command="pagefile")
filemenu.add_command(label="Print",command="printfile",compound=LEFT,accelerator="Ctrl+P")
filemenu.add_separator()

def exitfile(event=None):
    global textwrite,textchange
    try:
        if textchange:
            mbox=messagebox.askyesnocancel("Warning","Do you want to save this file")
            if mbox is True:
                if textwrite:
                    content=teaxtarea.get(1.0,END)
                    with open(textwrite,"w",encoding="utf-8") as forchange:
                        forchange.write(content)
                        win.destroy()
                else:
                    content2=str(textarea.get(1.0,END))
                    textwrite=filedialog.asksaveasfile(mode="w",defaultextension=".txt",filetypes=(("Text file","*.txt"),("All files","*.*")))
                    textwrite=write(content2)
                    textwrite.close()
                    win.destroy()
            elif mbox is False:
                win.destroy()
        else:
            win.destroy()
    except:
        return
        
filemenu.add_command(label="Exit",command=exitfile)

editmenu=Menu(menubar, tearoff = 0)
menubar.add_cascade(label="Edit",menu=editmenu)
editmenu.add_command(label="Undo",command=lambda:textarea.event_generate("<<Undo>>"),compound=LEFT,accelerator="Ctrl+Z")
editmenu.add_separator()
editmenu.add_command(label="Cut",command=lambda:textarea.event_generate("<Control x>"),compound=LEFT,accelerator="Ctrl+X")
editmenu.add_command(label="Copy",command=lambda:textarea.event_generate("<Control c>"),compound=LEFT,accelerator="Ctrl+C")
editmenu.add_command(label="Paste",command=lambda:textarea.event_generate("<Control v>"),compound=LEFT,accelerator="Ctrl+V")
editmenu.add_command(label="Delete",command=lambda:textarea.event_generate("<Delete>"),compound=LEFT,accelerator="Del")
editmenu.add_separator()
editmenu.add_command(label="Search With Bing...",command="searchedit",compound=LEFT,accelerator="Ctrl+E")

def get_index(index):
    return tuple(map(int,str.split(index,".")))

def findedit():

    def findbutton():
        word=findentry.get()
        if nocasematch.get():
            matchcase=False
            wraparound=False
        else:
            matchcase=True
            wraparound=True
        if direction.get():
            row,col=get_index(textarea.index(INSERT))
            begcol=str(col-len(word))
            beglocation=str(str(row)+"."+ begcol)
            location=textarea.search(word,textarea.index(beglocation),backwards=True,nocase=matchcase)
            log.info("searching backwords")
        else:
            log.info("searching forwards")
            location=textarea.search(word,textarea.index(INSERT),backwards=True,nocase=matchcase)
        if location !=" ":
            log.info("found" + word + "at position" + location)
            priorsearch=word
            row,col=get_index(location)
            endcol=str(col+len(word))
            endlocation=str(str(row)+ "."+ endcol)
            textarea.mark_set("insert",endlocation)
            textarea.see("insert")
            textarea.tag_remove("sel","1.0",END)
            textarea.tag_raise("sel")
            textarea.tag_add("sel",location,endlocation)
            textarea.focus()
        else:
            log.warning(word + "String not found")
            
    
    findwin=Toplevel()
    findwin.geometry("390x150")
    findwin.title("Find Word")
    findwin.resizable(0,0)
    findtext=Label(findwin,text="Find What:")
    findentry=Entry(findwin,width=35)
    findbutton=Button(findwin,text="Find Next",command=findbutton,width=7,)
    findtext.grid(row=0,column=0,padx=4,pady=4)
    findentry.grid(row=0,column=3,padx=4,pady=4)
    findbutton.grid(row=0,column=7,padx=4,pady=4)
    # frame area
    direction=BooleanVar()
    direction.set(False)
    nocasematch=BooleanVar()
    nocasematch.set(False)

    createframe=LabelFrame(findwin,text="Direction")
    upradio=Radiobutton(createframe,text="UP", variable=direction ,value=True)
    downradio=Radiobutton(createframe,text="Down",variable=direction,value=False)
    upradio.grid(row=2,column=2,padx=4,pady=4)
    # radio button

    downradio.grid(row=2,column=4,padx=4,pady=4)
    createframe.grid(row=2,column=3,padx=4,pady=4)
    findbuttoncancel=Button(findwin,text="Cancel",width=7)
    findbuttoncancel.grid(row=2,column=7,padx=4,pady=4)
    # check button

    matchcase=Checkbutton(findwin,text="Match  Case",variable=nocasematch)
    matchcase.grid(row=3,column=0)
    wraparound=Checkbutton(findwin,text="Wrap around",variable=nocasematch)
    wraparound.grid(row=4,column=0)
    

editmenu.add_command(label="Find",command=findedit,compound=LEFT,accelerator="Ctrl+F")

def findnextedit():
    word=" "
    location=textarea.search(word,textarea.index(INSERT),nocase=True)
    log.info("searching next -- forwards")
    if location !="":
        log.info("found"+word+"at position"+location)
        row,col=get_index(location)
        endcol=str(col+len(word))
        endlocation=str(str(row)+"."+endcol)
        textarea.mark_set("insert",endlocation)
        textarea.see("insert")
        textarea.tag_remove("sel","1.0",END)
        textarea.tag_raise("sel")
        textarea.tag_add("sel",location,endlocation)
        textarea.focus()
    else:
        log.warning(word+"string not found")
        
editmenu.add_command(label="Find Next",command=findnextedit,compound=LEFT,accelerator="F3")
editmenu.add_command(label="Find Previous",command="findpreviousedit",compound=LEFT,accelerator="Shift+F3")

def replaceedit():
    replacewin=Toplevel()
    replacewin.geometry("400x160")
    replacewin.title("Replace ")
    replacewin.resizable(0,0)
    findtext=Label(replacewin,text="Find :")
    findentry=Entry(replacewin,width=35)
    findbutton=Button(replacewin,text="Find Next",command="findbutton",width=8,)
    findtext.grid(row=0,column=0,padx=4,pady=4)
    findentry.grid(row=0,column=3,padx=4,pady=4)
    findbutton.grid(row=0,column=7,padx=4,pady=4)
    replacetext=Label(replacewin,text="Replace :")
    
    replaceentry=Entry(replacewin,width=35)
    replacebutton=Button(replacewin,text="Replace",command="replacebutton",width=8,)
    replacetext.grid(row=2,column=0,padx=4,pady=4)
    replaceentry.grid(row=2,column=3,padx=4,pady=4)
    replacebutton.grid(row=2,column=7,padx=4,pady=4)
    replaceallbutton=Button(replacewin,text="Replace All",command="replaceallbutton",width=8,)
    replaceallbutton.grid(row=3,column=7,padx=4,pady=4)
    cancelbutton=Button(replacewin,text="Cancel",command="cancelbutton",width=8,)
    cancelbutton.grid(row=4,column=7,padx=4,pady=4)
    matchcase=Checkbutton(replacewin,text="Match  Case")
    matchcase.grid(row=4,column=0)
    wraparound=Checkbutton(replacewin,text="Wrap around")
    wraparound.grid(row=5,column=0)

    
editmenu.add_command(label="Replace",command=replaceedit,compound=LEFT,accelerator="Ctrl+H")
editmenu.add_command(label="Go To...",command="gotoedit",compound=LEFT,accelerator="Ctrl+G")
editmenu.add_separator()
editmenu.add_command(label="Select All",command=lambda:textarea.tag_add("sel","1.0","end"),compound=LEFT,accelerator="Ctrl+A")
#editmenu.add_command(label="Time/Date",command=timedateedit,compound=LEFT,accelerator="F5")

formatmenu=Menu(menubar, tearoff = 0)
menubar.add_cascade(label="Format",menu=formatmenu)
formatmenu.add_checkbutton(label="Word Wrap",command="check1")
formatmenu.add_command(label="Font...",command="fontformat")

viewmenu=Menu(menubar, tearoff = 0)
menubar.add_cascade(label="View",menu=viewmenu)
zoommenu=Menu(viewmenu,tearoff=0)
viewmenu.add_cascade(label="Zoom       ",menu=zoommenu,compound=LEFT)
zoommenu.add_command(label="Zoom In",command="zoominmenu",compound=LEFT,accelerator="Ctrl+Plus")
zoommenu.add_command(label="Zoom Out",command="zoomoutmenu",compound=LEFT,accelerator="Ctrl+Minus")
zoommenu.add_command(label="Restore Default Zoom",command="restoredefaultzoommenu",compound=LEFT,accelerator="Ctrl+0")
viewmenu.add_checkbutton(label="Status Bar",command="Statusbar")

helpmenu=Menu(menubar, tearoff = 0)
menubar.add_cascade(label="Help",menu=helpmenu)
helpmenu.add_command(label="View Help",command="viewhelpmenu")
helpmenu.add_command(label="Send Feedback",command="sendfeedbackmenu")
helpmenu.add_separator()
helpmenu.add_command(label="About Notepad",command="aboutnotepadmenu")

win.config(menu=menubar)
    
win.mainloop()


