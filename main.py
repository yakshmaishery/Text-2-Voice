from tkinter import *
from tkinter import ttk,filedialog,messagebox
import pyttsx3,os
import threading

class Application:

    def __init__(self):
        """Initial Variables"""
        self.engine = pyttsx3.init()
        self.engine_rate = 150
        self.Gender_voice = 0
        pass
    
    def User_Interface(self,*args):
        """This method is Used for the User Interface GUI"""
        self.root = Tk()
        self.root.title("Text to Audio")
        self.root.state("zoomed")

        self.STYLE = ttk.Style()
        self.STYLE.configure("TButton",font=("arial",13,"bold"),background="yellow")
        self.STYLE.configure("TRadiobutton",font=("arial",13,"bold"),background="yellow")
        self.STYLE.configure("TScale",font=("arial",13,"bold"),background="yellow")
        # Label
        Label(self.root,text="Text ➡ Voice",font=("arial",15,"bold"),bg="yellow").pack(fill=X)
        # Frame
        # Buttons Frame
        self.F2 = Frame(self.root,border=0,relief=SOLID,padx=2,pady=2,bg="yellow")
        self.F2.columnconfigure(4,weight=1)

        # Run Button
        Button(self.F2,bg="orange",fg="black",font=("arial",13,"bold"),activebackground="yellow",activeforeground="black",border=1,relief=SOLID,text="RUN",cursor="hand2",command=self.RUN_Thread_FUNC).grid(row=0,column=0,padx=2,pady=2,sticky="nswe")

        # Gender
        self.Gender = IntVar()
        ttk.Radiobutton(self.F2,value=0,variable=self.Gender,text="MALE",cursor="hand2",command=self.Gender_FUNC).grid(row=0,column=1,padx=2,pady=2,sticky="nswe")
        ttk.Radiobutton(self.F2,value=1,variable=self.Gender,text="FEMALE",cursor="hand2",command=self.Gender_FUNC).grid(row=0,column=2,padx=2,pady=2,sticky="nswe")
        self.Gender.set(0)

        # Rate
        Label(self.F2,text="Rate:",font=("arial",13,"bold"),bg="yellow").grid(row=0,column=3,padx=2,pady=2,sticky="nswe")

        self.RATE_VALUE = IntVar()
        self.S1 = ttk.Scale(self.F2,from_=1,to=200,variable=self.RATE_VALUE,cursor="hand2",command=self.Voice_Rate_FUNC)
        self.S1.grid(row=0,column=4,padx=2,pady=2,sticky="nswe")

        # Save File
        Button(self.F2,bg="orange",fg="black",font=("arial",13,"bold"),activebackground="yellow",activeforeground="black",border=1,relief=SOLID,text="SAVE",cursor="hand2",command=self.Save_FUNC).grid(row=0,column=5,padx=2,pady=2,sticky="nswe")

        # it is Working
        self.Running_state = ttk.Progressbar(self.F2,value=100)
        self.Running_state.grid_forget()

        self.F2.pack(fill=BOTH,expand=True,side=BOTTOM)

        # Text box Frame
        self.F1 = Frame(self.root,border=1,relief=SOLID,padx=2,pady=2,bg="orange")
        # Text Box
        self.DATA = Text(self.F1,border=1,relief=SOLID,font=("arial",20),height=20,bg="yellow",fg="black")
        self.DATA.pack(fill=BOTH,expand=True)

        self.F1.pack(fill=BOTH,expand=True)

        self.root.mainloop()
        pass

    def RUN_Thread_FUNC(self,*args):
        """This method will start the RUN_FUNC in thread"""
        threading.Thread(target=self.RUN_FUNC,daemon=True).start()
        pass

    def RUN_FUNC(self,*args):
        """This Method is what works for Text to Voice"""
        # Rate
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', self.engine_rate)
        # Voice
        voices = self.engine.getProperty('voices')    
        self.engine.setProperty('voice', voices[self.Gender_voice].id)

        self.engine.say(self.DATA.get(0.0,END))
        self.Running_state.grid(row=1,column=0,columnspan=6,padx=2,pady=2,sticky="nswe")
        self.engine.runAndWait()
        self.Running_state.grid_forget()
        pass

    def Gender_FUNC(self,*args):
        """This Method would be Used to Change the voice of Male to Female or vice versa"""
        x = self.Gender.get()
        if x==0:
            self.Gender_voice = 0
        if x==1:
            self.Gender_voice = 1
        pass

    def Voice_Rate_FUNC(self,*args):
        """The Rate of Speed of Voice from 1 to 200"""
        self.engine_rate = self.RATE_VALUE.get()
        pass

    def Save_FUNC(self,*args):
        """To Save The  Text to Voice in MP3 File Format"""
        fileurl = filedialog.asksaveasfilename(title="Save File",filetypes=[("MP3","*.mp3")])
        if fileurl:
            fileurl = f"{fileurl}.mp3"
            print(fileurl)
            os.chdir(os.path.dirname(fileurl))
            self.engine.save_to_file(self.DATA.get(0.0,END),os.path.basename(fileurl))
            self.engine.runAndWait()
            messagebox.showinfo("Save",f"The {fileurl} has been Saved")
    pass

if __name__ == "__main__":
    Application().User_Interface()