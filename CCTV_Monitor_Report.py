from tkinter import *
from tkinter.ttk import Progressbar
import sys
from tkinter import ttk
from PIL import ImageTk, Image
import cv2,pandas,datetime,time
from tkinter import messagebox
from time import sleep
# -*- coding: utf-8 -*-

root=Tk()
root.resizable(0,0)

height=380
width=650
x=(root.winfo_screenwidth()//2)-(width//2)
y=(root.winfo_screenheight()//2)-(height//2)

root.geometry('{}x{}+{}+{}'.format(width,height,x,y))
root.overrideredirect(1)#it hides title bar
root.wm_attributes('-alpha',1.0)#it makes transparent window
root.wm_attributes('-topmost',True)#will be on top of all windows
root.wm_attributes('-transparentcolor','white')


ph1=Image.open("C:\\Users\\BRAHMI\\Downloads\\black1.jpg")
ph2=Image.open("C:\\Users\\BRAHMI\\Downloads\\black.png")

photo=ph1.resize((650,380))
img1 = ImageTk.PhotoImage(photo)


ph2=ph2.resize((650,380))
img3 = ImageTk.PhotoImage(ph2)





bgLabel=Label(root,image=img3)
bgLabel.place(x=0,y=0)

hlabel=Label(root,text="CCTV Monitor Report",font=('Calibri',20,'bold'),fg='white',bg="gray6")
hlabel.place(x=200,y=10)


loading_l=Label(root,text="loading",font=('arial',10,'bold'),fg='blue')
loading_l.place(x=320,y=370)

progress=Progressbar(root,orient='horizontal',length=650,mode='determinate')
progress.place(x=0,y=370)



def exitWindow():
    sys.exit(root.destroy())
    sys.exit(window2.destroy())

def top():
    window2=Toplevel(root)
    window2.geometry("{}x{}+{}+{}".format(width,height,x,y))
    window2.title("CCTV Monitor Report")
    window2.resizable(0,0)
    label=Label(window2,image=img1,compound=TOP)
    label.place(x=0,y=0)
    
    label_1 = Label(window2,text="Enter the time limit:",font=('calibri',15),fg='black')
    label_1.place(x=150,y=100)

    tag_label=Label(window2,text=" © Pavani & Brahmamma",font=('calibri',13,'italic'),fg='white',bg='black')
    tag_label.place(x=250,y=350)
    window2.iconphoto(False,PhotoImage(file="C:/Users/pavani/Desktop/CCTV Monitor Report/black.png"))

    def valid(input,input1):
        if input==" " or input==" ":
            messagebox.showinfo("time","time format be like 00:00:00")
        if type(input)!='string' or type(input)!='string':
            messagebox.showinfo("time","time format be like 00:00:00")
        
    reg=root.register(valid)
    entry=Entry(window2,font=("Calibri",15),validate="all",validatecommand=(reg,'%P','%i'))
    entry.place(x=350,y=100,width=150,height=30)

    label_2=Label(window2,text="Select type of cam : ")
    label_2.place(x=150,y=170)
    label_2.config(font=("Calibri",15))
    cam=[0,1,2]
    cb=ttk.Combobox(window2,values=cam,width=13,height=30,font=("Calibri",14))
    cb.place(x=350,y=170)

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    cv2.startWindowThread()
    out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'XVID'),3.,(650,380))
    time1=[]
    font=cv2.FONT_HERSHEY_SIMPLEX
    date=str(datetime.datetime.now().date())
    def report_time():
        dict={'time':time1}
        df=pandas.DataFrame(dict)
        df.to_csv('video{}.csv'.format(date))
    
    def video_stream():
        app = Frame(window2)
        app.pack()
        lmain = Label(app)
        lmain.pack()
        t=entry.get()
        t=t.split(":")
        sec=float(t[0])*3600+float(t[1])*60+float(t[2])
        cam_t=int(cb.get())
        cap = cv2.VideoCapture(cam_t)
        start_time=time.time()
        start_time1=datetime.datetime.now()
        destroy_wid()
        def video():
            try:
                _, frame = cap.read()
                frame = cv2.resize(frame,(650, 380))
                boxes, weights = hog.detectMultiScale(frame, winStride=(8,8),padding=(4,4),scale=1.05)
                if len(boxes)!=0:
                    detect_time=datetime.datetime.now()
                    h=start_time1.hour
                    m=start_time1.minute
                    s=start_time1.second
                    printf("hi")
                    time1.append(detect_time-timedelta(hours=h,minutes=m,seconds=s))
                dtime=str(datetime.datetime.now())
                frame=cv2.putText(frame,dtime,(10,30),font,1,(0,220,220),2,cv2.LINE_AA)
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                out.write(frame.astype('uint8'))
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                lmain.imgtk = imgtk
                lmain.configure(image=imgtk)
                end_time=time.time()
                t_diff=end_time-start_time
                if(t_diff>sec):
                    report_time()
                    cap.release()
                    out.release()
                    cv2.destroyAllWindows()
                    window2.destroy()
                else:
                    lmain.after(10, video)
            except:
                if(cam_t)==1:
                    messagebox.showinfo("error","currently no external cameras connected ")
                    
                print("hello")
                cap.release()
                cv2.destroyAllWindows()
                root.destroy()
        video()
    def destroy_wid():
        label_1.destroy()
        entry.pack_forget()
        btn.destroy()
    btn=Button(window2,text="Start",command=video_stream,font=('Calibri',15),bg='green',fg='white')
    btn.place(x=300,y=240,height=30,width=80)




    exitBtn=Button(window2,text="Exit",fg='white',bg='red',command=exitWindow,font=('Calibri',15))
    exitBtn.place(x=300,y=280,width=80,height=30)
    root.withdraw()
i=0
def load():
    global i
    if i<=10:
        txt='loading'+('.'*i)+(str(10*i)+'%')
        loading_l.config(text=txt)
        loading_l.after(500,load)
        progress['value']=10*i
        i=i+1
    else:top()
load()






root.mainloop()
        











    





    

