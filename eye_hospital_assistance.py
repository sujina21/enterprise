import smtplib
import traceback
import os
import tkinter as tk
from tkcalendar import *
from tkinter import *
from tkinter import Toplevel
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkinter import ttk
# from image_conversion import PhotoImage

import random
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from database import connect_to_database,execute_query,disconnect_database
from add_patient import open_toplevel


load_dotenv()

def on_connect():
    host = os.getenv("HOST")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    database = os.getenv("DATABASE_NAME")
    if connect_to_database(host,user,password,database):
        print("Success", "Connection to database established")

on_connect()


def fetch_doctor_location(doctor_id):
    # Joining Doctor and Location tables to get the location details
    location_info= execute_query(rf"SELECT floor_number, room_number FROM doctor JOIN location on Doctor.location_id = Location.id where Doctor.id='{doctor_id}'")
    if location_info:
        floor_number, room_number = location_info[0]
        return f"Room {room_number} on floor {floor_number}"
    else:
        return "N/A"

root = tk.Tk()

root.iconbitmap('HospitalIcon.ico')

root.geometry("1000x562+200+80")
root.resizable(False, False)
root.title("Eye Hospital Management System")

bg = PhotoImage(file =r"images/loginBackground.png")
bg = bg.subsample(1,1)

can = Canvas(root)
can.place(x=0,y=0,relwidth = 1 ,relheight = 1)
can.create_image(0,0,image = bg ,anchor = 'nw')

#Images Used inside Login Page
loginBackground = PhotoImage(file =r"images/loginBackground.png")
loginBackground = loginBackground.subsample(2,2)

HospitalLogoImg = PhotoImage(file=r'images/HospitalLogoImg.png')
HospitalLogoImg = HospitalLogoImg.subsample(10,10)

hospital_logo = PhotoImage(file=r'images/HospitalLogoImg.png')
hospital_logo = hospital_logo.subsample(4,4)

loginUserLogo = PhotoImage(file=r'images/loginUserLogo.png')
loginUserLogo = loginUserLogo.subsample(3, 3)

usernameimg = PhotoImage(file=r'images/usernnameIcon.png')
usernameimg = usernameimg.subsample(1, 1)

passwordimg = PhotoImage(file=r'images/passwordimg.png')
passwordimg = passwordimg.subsample(1, 1)

calanderimg = PhotoImage(file=r'images/Calendar.png')
calanderimg = calanderimg.subsample(1,1)

clockimg = PhotoImage(file=r'images/Clock.png')
clockimg = clockimg.subsample(1,1)

frontImage = PhotoImage(file=r'images/eh_front1.png')
# frontImage = frontImage.subsample(1,1)

editDoctorBtnIcon = PhotoImage(file=r'images/editDoctorBtnIcon.png')
editDoctorBtnIcon = editDoctorBtnIcon.subsample(6, 6)


deleteDoctorBtnIcon = PhotoImage(file=r'images/deleteDoctorBtnIcon.png')
deleteDoctorBtnIcon = deleteDoctorBtnIcon.subsample(5, 5)

viewBtnIcon = PhotoImage(file=r'images/viewBtnIcon.png')
viewBtnIcon = viewBtnIcon.subsample(1,1)

logoutimg = PhotoImage(file=r'images/logouticon.png')
logoutimg = logoutimg.subsample(1,1)

backbtnimg = PhotoImage(file=r'images/backbtnimg1.png')
backbtnimg = backbtnimg.subsample(5,6)

## Images in other Frames Backgrounds
addPatientimg =PhotoImage(file=r'images/addPatientimg.png')
addPatientimg = addPatientimg.subsample(6,6)

editDoctorFrameBg =PhotoImage(file=r'images/editDoctorFrameBg.png')
editDoctorFrameBg = editDoctorFrameBg.subsample(2,3)

viewPatientFramebg =PhotoImage(file=r'images/viewPatientFramebg.png')
viewPatientFramebg = viewPatientFramebg.subsample(1,1)

deleteDoctorFrameBg =PhotoImage(file=r'images/deleteDoctorFrameBg.png')
deleteDoctorFrameBg = deleteDoctorFrameBg.subsample(2,3)

addStudbg =PhotoImage(file=r'images/AddStudentFrameBg.png')
addStudbg = addStudbg.subsample(1,1)

# Label Widget Icons
UserIdimg =PhotoImage(file=r'images/UserIdimg.png')
UserIdimg = UserIdimg.subsample(18,18)

fullname = PhotoImage(file=r'images/fullname.png')
fullname = fullname.subsample(3,3)

location = PhotoImage(file=r'images/location.png')
location = location.subsample(13,13)

attandance = PhotoImage(file=r'images/attandance.png')
attandance = attandance.subsample(17,17)

status = PhotoImage(file=r'images/status.png')
status = status.subsample(1,1)


#Widget Used inside the login Frame

def loginbtnfunc():                                     #Login Button Function
    global full_name
    user = username.get()
    passw = password.get()
    if (user == "" or passw == ""):
        messagebox.showinfo("Notification", "All fields are required", parent=root)
    elif (len(passw) < 5):
        messagebox.showerror("Notification", "Password Must be of 5 Characters!!!", parent=root)
    else:
        query = rf'select * from eh_admin where username="{user}" and password="{passw}";'
        result = execute_query(query)
        if result:
            root.withdraw()
            data = execute_query(rf"select fullname from eh_admin where username='{user}'")
            for i in data:
                full_name = f"Dr. {i[0]}"
            openTop()
        else:
            messagebox.showerror('Notification', 'Incorrect Username or Password!!!\nPlease try again...',
                                    parent=root)
            loginForgetPassbtn.place(x=500, y=455)

# Login Frame Labels

titleLabel = Label(can ,text='RECEPTIONIST ADMIN LOGIN SYSTEM', font=('Georgia', 20, 'italic bold'), bg='#6D93B1', fg='White' ,height = 2,
                relief='groove' ,bd=2 )
titleLabel.place(x=1,y=1,relwidth = 1)

titleLabel2 = Label(can,image = hospital_logo , bg='azure' ,bd=2,relief='groove' )
titleLabel2.place(x=6,y=8)

can.create_image((430,80),image = loginUserLogo ,anchor = 'nw')

can.create_image((297,275),image = usernameimg ,anchor = 'nw')

can.create_text((370,289),text = "Username :",font=('times', 15, 'italic bold'), fill='black')

can.create_image((297,358),image = passwordimg ,anchor = 'nw')

can.create_text((370,368),text = "Password :",font=('times', 15, 'italic bold'))

#Login Entry Boxes
username = StringVar(value="")
password = StringVar(value="")

usernameEntry = Entry(root, textvariable=username, width=25, font=('times', 15, 'italic'), bd=5, bg='lightblue')
usernameEntry.place(x=420, y=270)
usernameEntry.focus()

passwordEntry = Entry(root, width=25, show='*', textvariable=password, font=('times', 15, 'italic'), bd=5, bg='lightblue')
passwordEntry.place(x=420, y=350)

#Login Submit Button
loginbtn = Button(root, text='Login', font=('times', 13, 'italic bold'), bg='lightgreen', bd=5, activebackground='green',
                activeforeground='white', command=loginbtnfunc ,width = 8)
loginbtn.place(x=580, y=410)

def ForGetPass(event):
    root.withdraw()
    Forget = Toplevel()
    Forget.geometry('500x290')
    Forget.resizable(False,False)
    Forget.title('Forget PassWord')

    for_frame =  Frame(Forget,bd= 4,relief ='groove',bg= 'red')
    for_frame.place(x=0,y=0,relwidth=1 ,relheight=1)

    forcan = Canvas(for_frame )
    forcan.place(x=0, y=0, relwidth=1, relheight=1)
    forcan.create_image(0, 0, image=loginBackground, anchor='nw')

    ForTitle = Label(forcan,text= 'Enter Verified Email ID' ,font= ('serif',15,'italic'), bg='#6D93B1', fg='White' ,bd=3,
                    relief = 'groove')
    ForTitle.place(x= 10 ,y= 5 ,width = 468)

    FortitleLabel2 = Label(forcan, image=HospitalLogoImg, bg='azure', bd=2, relief='groove')
    FortitleLabel2.place(x=16, y=9)

    forcan.create_text((115,125),text = 'Email : ', font= ('Time',12,'bold'))

    Emailval = StringVar()
    ForEmailVal = Entry(for_frame,textvariable = Emailval, font= ('Time',12,'italic') ,bd = 3 ,width = 28)
    ForEmailVal.place(x=145, y=110)

    def SendMail():
        if Emailval.get() == '' :
            messagebox.showerror('Error',"Email Field Cannot be Empty  !!!",parent = for_frame )
        else:
            try:
                query = rf'select password from eh_admin WHERE email ="{Emailval.get()}";'
                result = execute_query(query)
                if result:
                    Otp = random.randint(1000,9999)

                    # Create the email content
                    message = MIMEMultipart()
                    message['From'] = "Babita Eye Hospital"
                    message['To'] = Emailval.get()
                    message['Subject'] = "Your OTP Code"

                    # Create the OTP template
                    html = f"""
                    <html>
                    <body>
                        <h2>OTP Verification</h2>
                        <p>Dear user,</p>
                        <p>Your One-Time Password (OTP) is:</p>
                        <h1>{Otp}</h1>
                        <p>This OTP is valid for 10 minutes.</p>
                        <p>Thank you for using our service!</p>
                    </body>
                    </html>
                    """
                    
                    # Attach the HTML content to the email
                    message.attach(MIMEText(html, 'html'))

                    ## Send Mail
                    sender = 'sujinashrestha060@gmail.com'
                    reciver = Emailval.get()
                    server = smtplib.SMTP('smtp.gmail.com',587)
                    server.starttls()
                    server.login(sender,os.getenv("KEY"))
                    server.sendmail(sender,reciver,message.as_string())
                    server.quit()

                    Otp_frame = Frame(Forget, bd=4 , relief='groove',bg = 'green')
                    Otp_frame.place(x=0, y=0, relwidth=1, relheight=1)

                    forcan = Canvas(Otp_frame)
                    forcan.place(x=0, y=0, relwidth=1, relheight=1)
                    forcan.create_image(0, 0, image=loginBackground, anchor='nw')

                    ForTitle = Label(forcan, text='Enter OTP send to Email ID', font=('serif', 15, 'italic'),
                                    bg='#6D93B1', fg='White',bd= 3 ,relief= 'groove' )
                    ForTitle.place(x= 10 ,y= 5 ,width = 468)

                    FortitleLabel2 = Label(forcan, image=HospitalLogoImg, bg='azure', bd=2, relief='groove')
                    FortitleLabel2.place(x=16, y=9)

                    forcan.create_text((120,125), text='OTP : ', font=('Time', 12, 'bold'))

                    otpval = StringVar()
                    ForotpVal = Entry(Otp_frame, textvariable=otpval , font= ('Time',12,'italic'), bd=4)
                    ForotpVal.place(x=145, y=110)

                    def NewPass():
                        if otpval.get() == '':
                            messagebox.showinfo('INFORMATION',"OTP Field cannot be Empty !!!" , parent = for_frame)
                        else:
                            if otpval.get() == str(Otp):
                                NewPass_frame = Frame(Forget, bd=4, relief='groove' ,bg = 'yellow')
                                NewPass_frame.place(x=0, y=0, relwidth=1, relheight=1)

                                forcan = Canvas(NewPass_frame)
                                forcan.place(x=0, y=0, relwidth=1, relheight=1)
                                forcan.create_image(0, 0, image=loginBackground, anchor='nw')

                                NewPassTitle = Label(forcan, text='New PassWord',
                                                font=('serif', 15, 'italic'),
                                                bg='#6D93B1', fg='White' ,bd= 3 ,relief= 'groove')
                                NewPassTitle.place(x= 10 ,y= 5 ,width = 468)

                                FortitleLabel2 = Label(forcan, image=HospitalLogoImg, bg='azure', bd=2, relief='groove')
                                FortitleLabel2.place(x=16, y=9)

                                forcan.create_text((130,115), text='New Password : ', font=('Time', 12, 'bold'))

                                NewPassval = StringVar()
                                NewPassLabval = Entry(NewPass_frame, textvariable=NewPassval, font=('Times', 12, 'italic'), bd=4)
                                NewPassLabval.place(x=220, y=100)

                                forcan.create_text((142,167), text='Confirm Password : ', font=('Time', 12, 'bold'))

                                ConNewPassval = StringVar()
                                ConNewPassLabval = Entry(NewPass_frame,show = '*',textvariable=ConNewPassval,
                                                    font=('Times', 12, 'italic'), bd=4)
                                ConNewPassLabval.place(x=220, y=150)

                                def ConPass():
                                    if NewPassval.get() != '' and ConNewPassval.get() != '':
                                        if len(NewPassval.get()) >= 5:
                                            if NewPassval.get() == ConNewPassval.get():
                                                query= "select * from eh_admin;"
                                                execute_query(query)
                                                query = rf'UPDATE eh_admin  SET password = "{ConNewPassval.get()}" WHERE email ="{Emailval.get()}";'
                                                rowCount = execute_query(query)
                                                if rowCount == 1 :
                                                    messagebox.showinfo('INFORMATION',
                                                                        "Password Successfully Updated !!!",
                                                                        parent=for_frame)
                                                    Forget.destroy()
                                                    root.update()
                                                    root.deiconify()
                                                    username.set('')
                                                    password.set('')
                                                else:
                                                    messagebox.showwarning('WARNING',
                                                                        "New Password and Previews Password is Same \nTry Something New Password!!!",
                                                                        parent=for_frame)
                                            else:
                                                messagebox.showwarning('WARNING',
                                                                    "New Password and Confirm Password Must Same!!!",
                                                                    parent=for_frame)
                                        else:
                                            messagebox.showwarning('WARNING',"Password Must contain Atleast 5 Character!!!",
                                                                parent=for_frame)

                                    else :
                                        messagebox.showinfo('INFORMATION',"Any Field cannot be Empty !!!" , parent = for_frame)

                                ConfirmNewPassBtn = Button(NewPass_frame,font = ('Times',13,'bold') ,bd = 4 ,width = 8 ,
                                                        text='Confirm',bg = "sky blue",
                                                        command=ConPass)
                                ConfirmNewPassBtn.place(x=300, y=190)

                            else:
                                messagebox.showwarning("WARNING","Wrong OTP !!!" ,parent = for_frame)


                    ForotpBtn = Button(Otp_frame, text='Next',bg = "sky blue" ,bd= 4 ,font = ('Times',13,'bold'),width = 8,
                                    command = NewPass)
                    ForotpBtn.place(x=300, y=190)

                else:
                    Emailval.set('')
                    messagebox.showwarning('WARNING', "Such Email Id Is Not There In Record !!!", parent=for_frame)
            except:
                print(traceback.format_exc())
                messagebox.showerror('Error', "SomeThing Went Wrong Please Try Again Later!!!", parent=for_frame)

    ForBtn = Button(for_frame , text= 'Submit',font = ('Times',13,'bold'),width = 8,bd= 4 ,bg = 'sky blue',command =SendMail)
    ForBtn.place(x=300, y=190)


    for_frame.place()

loginForgetPassbtn = Label(root, text='Click if Forget Password', font=('times', 13, 'italic bold'), bg='#76ABB6',fg ='red')
loginForgetPassbtn.place_forget()
loginForgetPassbtn.bind( "<Button>", ForGetPass )

def on_enterdeliveredbtn(e):
    loginForgetPassbtn.configure(fg='blue')
def on_leavedeliveredbtn(e):
    loginForgetPassbtn.configure(fg='red')

loginForgetPassbtn.bind('<Enter>',on_enterdeliveredbtn)
loginForgetPassbtn.bind('<Leave>',on_leavedeliveredbtn)

def getGenderAbb(gender):
        return "M" if str(gender).lower() == "male" else "F"

def openTop():

    def Date_Time():
        time_string = time.strftime("%H:%M:%S")
        date_string = time.strftime("%d/%m/%Y")
        clockdateLabel.configure(text=" Date : " + date_string)
        clocktimLabel.configure(text=" Time : " + time_string )
        clocktimLabel.after(1000, Date_Time)

    ## TopLevel Frame

    dashwin = Toplevel()
    dashwin.geometry("900x550+300+100")
    # dashwin.resizable(False, False)
    dashwin.iconbitmap('HospitalIcon.ico')
    dashwin.title("Eye Hospital Management System")

    ## TopLevel Frame Title
    root_title = Label(dashwin, text="DASHBOARD", fg="white", bg='#6D93B1', font=("Courier New", 40, "bold"),relief='groove',bd=2)
    root_title.pack(side = 'top', fill ='x')

    titleLabel2 = Label(dashwin, image=hospital_logo, bg='azure', bd=2, relief='groove')
    titleLabel2.place(x=6, y=8)

    ## TopLevel Date Time Admin Frame

    Admin_dateFrame = Frame(dashwin, bg="#E5EACA", height=64 , relief='groove',bd=5)
    Admin_dateFrame.pack(fill ='x')

    nameLabel = Label(Admin_dateFrame, text="Name:", font=("Arial", 13, "bold"),bg="#E5EACA")
    nameLabel.place(x=10, y=0 ,relheight=1)

    nameValLabel = Label(Admin_dateFrame, text = full_name, font=("Arial", 14, "italic bold"), fg='red',bg="#E5EACA", padx=5)
    nameValLabel.place(x=68, y=0 ,relheight=1)

    clockdateLabel = Label(Admin_dateFrame,image = calanderimg, font=('times', 14, 'bold'), relief='flat', bg='#E5EACA',compound ='left')
    clockdateLabel.place(x=470, y=0,relheight=1)

    clocktimLabel = Label(Admin_dateFrame,image = clockimg, font=('times', 14, 'bold'), relief='flat', bg='#E5EACA',compound ='left')
    clocktimLabel.place(x=690, y=0, relheight=1)
    Date_Time()

    ## DashBoard Button Frame and Image
    dashboardframe = Frame(dashwin)
    dashboardframe.pack(fill ='both')

    imageLabel = Label(dashboardframe, image=frontImage,bd = 5,relief = 'groove', bg="#B07138")
    imageLabel.pack()

    ## Frame Raise Function
    def raise_frame(fm):
        fm.tkraise()


    ## ADD Patient Button
    add_patientbtn = Button(dashboardframe, text="Add Patient", font=("Arial", 12, "bold italic"), fg='white',
                        bg="#B07138",
                        activebackground='red'
                        , activeforeground='white', bd=10, width=150, height=40, image=addPatientimg, compound='left',
                        command=lambda : print("click bhayo"))
    add_patientbtn.place(x= 30 ,y = 35 )


    def showAllPatient():
        ## Search Patient Frame
        showPatientframe = Frame(dashwin, bg="#AAC8C6", relief='ridge', bd=4)
        showPatientframe.place(x=0, y=132, relwidth=1,height =418)

        ShowPatientframeBgImg = Label(showPatientframe, image=viewPatientFramebg)
        ShowPatientframeBgImg.place(x=0, y=0, relwidth=1, relheight=1)

        showPatientbackbtn = Button(showPatientframe, bd=5, font=("Arial", 14, "bold"), image=backbtnimg,
                                command=lambda: raise_frame(dashboardframe),bg= '#AAC8C6')
        showPatientbackbtn.place(x=10, y=10)

        MinisearchPatientFrame = Frame(showPatientframe, width=500, height=70, bd=5, relief='ridge', bg='#AAC8C6')
        MinisearchPatientFrame.place(x=220, y=10)

        SearchPatientIdLabelImg = Label(MinisearchPatientFrame, image=UserIdimg, font=("Arial", 12, "bold"), bg='#AAC8C6')
        SearchPatientIdLabelImg.place(x=20, y=10)

        SearchPatientIdLabel = Label(MinisearchPatientFrame, text="Patient ID :", font=("Arial", 12, "bold"), bg='#AAC8C6')
        SearchPatientIdLabel.place(x=60, y=15)

        SearchPatientIdEntryval = StringVar()
        SearchPatientidEntry = Entry(MinisearchPatientFrame, textvariable=SearchPatientIdEntryval, bg='snow',
                                font=("Arial", 12), bd=5,
                                relief=GROOVE,
                                width=10)
        SearchPatientidEntry.place(x=150, y=13)

        def SearchPatientSubmitbtnfun():
            if SearchPatientIdEntryval.get() == '':
                messagebox.showinfo('INFORMATION', 'Search Patient Id cannot Be Empty...', parent=dashwin)
            else:
                query = rf'select pt.name,pt.age,pt.gender,pt.phone,pt.problem, dt.name from patient pt join doctor dt on pt.visited_to = dt.id where pt.patient_id= "{SearchPatientIdEntryval.get()}";'
                result = execute_query(query)
                if result:
                    for i in result:
                        allPatientinfoTable.delete(*allPatientinfoTable.get_children())
                        tabVal = [str(i[0]).title(), f"{i[1]}/{getGenderAbb(i[2])}", i[3], i[4], i[5]]   
                        allPatientinfoTable.insert('', END, values=tabVal)
                else:
                    messagebox.showinfo('INFORMATION', 'No Patient Available With Such Patient Id...', parent=dashwin)

        def SearchPatientResetbtnfun():
            SearchPatientIdEntryval.set('')
            allPatientinfoTable.delete(*allPatientinfoTable.get_children())
            query = 'select pt.name,pt.age,pt.gender,pt.phone,pt.problem, dt.name from patient pt join doctor dt on pt.visited_to = dt.id;'
            data = execute_query(query)
            for i in data:
                tabVal = [str(i[0]).title(), f"{i[1]}/{getGenderAbb(i[2])}", i[3], i[4],i[5]]
                allPatientinfoTable.insert('', END, values = tabVal)


        SearchPatientsubmitbtn = Button(MinisearchPatientFrame, text="Search", bg='blue2', fg='white',
                                        activebackground='red',
                                        bd=5,
                                        activeforeground='white'
                                        , width=8, font=("Arial", 12, "bold"), command=SearchPatientSubmitbtnfun)
        SearchPatientsubmitbtn.place(x=270, y= 10)

        SearchPatientsubmitbtn = Button(MinisearchPatientFrame, text="Reset", bg='blue2', fg='white',
                                        activebackground='red',
                                        bd=5,
                                        activeforeground='white'
                                        , width=8, font=("Arial", 12, "bold"), command=SearchPatientResetbtnfun)
        SearchPatientsubmitbtn.place(x=380, y= 10)

        MinishowPatientFrame = Frame(showPatientframe, width=850, height=10, bd=4, relief='ridge',bg = '#AAC8C6')
        MinishowPatientFrame.place(x=25, y=90)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', font=('times', 15, 'italic'),fieldbackground = '#AAC8C6',
                        background = '#AAC8C6',foreground='red',rowheight = 25)
        style.configure('Treeview.Heading', font=('times', 15, 'italic'), background='sky blue')
        style.map('Treeview',background = [('selected','blue2')])

        Scroll_x = Scrollbar(MinishowPatientFrame, orient=HORIZONTAL)
        Scroll_y = Scrollbar(MinishowPatientFrame, orient=VERTICAL )

        allPatientinfoTable = Treeview(MinishowPatientFrame, columns=('Name', 'Age/Sex', 'Phone', 'Problem', 'Visited To'),
                                    xscrollcommand=Scroll_x.set, yscrollcommand=Scroll_y.set)

        Scroll_x.pack(side=BOTTOM, fill=X ,anchor = W)
        Scroll_y.pack(side=RIGHT, fill=Y ,anchor = N)
        Scroll_x.configure(command=allPatientinfoTable.xview)
        Scroll_y.configure(command=allPatientinfoTable.yview)

        # Treeview Column Formate
        allPatientinfoTable.column('Name', width=180, anchor=CENTER)
        allPatientinfoTable.column('Age/Sex', width=90, anchor=CENTER)
        allPatientinfoTable.column('Phone', width=130, anchor=CENTER)
        allPatientinfoTable.column('Problem', width=240, anchor=CENTER)
        allPatientinfoTable.column('Visited To', width=160, anchor=CENTER)

        # Treeview Heading Tect
        allPatientinfoTable.heading('Name', text='Name'.upper())
        allPatientinfoTable.heading('Age/Sex', text='Age/Sex'.upper())
        allPatientinfoTable.heading('Phone', text='Phone'.upper())
        allPatientinfoTable.heading('Problem', text='Problem'.upper())
        allPatientinfoTable.heading('Visited To', text='Visited To'.upper())


        allPatientinfoTable.configure(show='headings')

        allPatientinfoTable.pack(fill='both')

        query = 'select pt.name,pt.age,pt.gender,pt.phone,pt.problem, dt.name from patient pt join doctor dt on pt.visited_to = dt.id;'
        data = execute_query(query)
        for i in data:
            tabVal = [str(i[0]).title(), f"{i[1]}/{getGenderAbb(i[2])}", i[3], i[4],i[5]]
            allPatientinfoTable.insert('', END, values = tabVal)


    show_Patientbtn = Button(dashboardframe, text="View Patient", font=("Arial", 12, "bold italic"), fg='white',
                        bg="#B07138",
                        activebackground='red'
                        , activeforeground='white', bd=10, width=150, height=40, image=viewBtnIcon,
                        compound='left',command=showAllPatient)
    show_Patientbtn.place(x=300, y=35)

    # Edit Doctor Button Function
    editDoctorframe = Frame(dashwin, bg="#FFD896", relief='ridge', bd=5)
    editDoctorframe.place(x=0, y=132, relwidth=1,height = 418)

    editDoctorframeBgImg = Label(editDoctorframe, image=editDoctorFrameBg)
    editDoctorframeBgImg.place(x=0, y=0, relwidth=1, relheight=1)

    editDoctorBackbtn = Button(editDoctorframe, bd=4, image=backbtnimg,
                            command=lambda: raise_frame(dashboardframe),bg='#FFD896')
    editDoctorBackbtn.place(x=10, y=10)

    ## Edit Doctor Mini Frame 1
    miniEditdoctorframe = Frame(editDoctorframe, bg='#FFD896', height =200, width=550, relief='ridge', bd=4)
    miniEditdoctorframe.place(x=180, y=100)

    editDoctorframe_title = Label(miniEditdoctorframe, text="EDIT Doctor", bg="#006600", font=("Arial", 15, "bold"),
                            relief='groove', fg='white', width=41)
    editDoctorframe_title.place(x=20, y=10)

    editDoctorIdLabelImg = Label(miniEditdoctorframe, image=UserIdimg, font=("Arial", 12, "bold"), bg='#FFD896')
    editDoctorIdLabelImg.place(x=140, y=70)

    editDoctorIdLabel = Label(miniEditdoctorframe, text="Doctor ID :", font=("Arial", 12, "bold"), bg='#FFD896')
    editDoctorIdLabel.place(x=180, y=75)

    editDoctorId = StringVar()
    editDoctorIdEntry = Entry(miniEditdoctorframe, textvariable=editDoctorId , font=("Arial", 12), bd=5, relief=GROOVE,
                    width=10)
    editDoctorIdEntry.place(x=270, y=75)

    
    def editDoctorsubmitbtnfun():
        isDoctorAbsent=False
        if editDoctorId.get() == '':
            messagebox.showinfo("INFORMATION","Doctor ID cannot be Empty !!!" ,parent = dashwin )
        else:
            query = rf"select name ,location_id, attendance, current_status from doctor where id  = '{editDoctorId.get()}';"
            result = execute_query(query)
            if result:
                for i in result:
                    print(f"Test -->{str(i[2]).lower() == 'absent'}")
                    if(str(i[2]).lower() == "absent"):
                        isDoctorAbsent = True
                    else:
                        isDoctorAbsent = False
                    editDoctorName.set(i[0])
                    location = fetch_doctor_location(editDoctorId.get())
                    editLocation.set(location)
                    editAttandance.set(i[2])
                    editStatus.set(i[3])
                miniEditdoctorframe.place_forget()
                miniEditDoctorframe2.place(x=160, y=20)
                editDoctoridEntry2.configure(state = 'disable')
                editLocationEntry.configure(state = 'disable')
                editAttandanceEntry.configure(state = 'disable')
                if isDoctorAbsent==True:
                    editStatus.configure(state = 'disable')
            else:
                messagebox.showinfo("INFORMATION", "No Doctor There With Such ID !!!", parent=dashwin)

    edit1Doctorsubmitbtn = Button(miniEditdoctorframe, text="Submit", bg='blue2', fg='white', activebackground='red', bd=5,
                            activeforeground='white'
                            , width=8, font=("Arial", 12, "bold"), command=editDoctorsubmitbtnfun)
    edit1Doctorsubmitbtn.place(x=310, y=140)

    ## edit Doctor MiniFrame2

    miniEditDoctorframe2 = Frame(editDoctorframe, bg='powder blue', height=380, width=550, relief='groove', bd=4)
    miniEditDoctorframe2.place_forget()

    editDoctorframe_title2 = Label(miniEditDoctorframe2, text="EDIT DOCTOR", bg="#006600", font=("Arial", 15, "bold"),
                                relief='groove', fg='white', width=41)
    editDoctorframe_title2.place(x=20, y=10)

    editDoctorIdLabelImg2 = Label(miniEditDoctorframe2, image=UserIdimg, font=("Arial", 12, "bold"), bg='powder blue')
    editDoctorIdLabelImg2.place(x=70, y=65)

    editDoctorIdLabel2 = Label(miniEditDoctorframe2, text="Doctor ID :", font=("Arial", 12, "bold"), bg='powder blue')
    editDoctorIdLabel2.place(x=110, y=70)

    editDoctoridEntry2 = Entry(miniEditDoctorframe2, textvariable=editDoctorId, bg='sky blue', font=("Arial", 12), bd=5,
                            relief=GROOVE,
                            width=10)
    editDoctoridEntry2.place(x=210, y=70)

    editDoctorNameLabelImg = Label(miniEditDoctorframe2, image=fullname, font=("Arial", 12, "bold"), bg='powder blue')
    editDoctorNameLabelImg.place(x=70, y=112)

    editDoctorNameLabel = Label(miniEditDoctorframe2, text="FullName", font=("Arial", 12, "bold"), bg='powder blue')
    editDoctorNameLabel.place(x=110, y=122)

    editDoctorName = StringVar()
    editDoctorNameEntry = Entry(miniEditDoctorframe2, textvariable=editDoctorName, bg='sky blue', font=("Arial", 12), bd=5, relief=GROOVE,
                    width=30)
    editDoctorNameEntry.place(x=210, y=120)

    editDoctorLocationLabelImg = Label(miniEditDoctorframe2, image=location, font=("Arial", 12, "bold"), bg='powder blue')
    editDoctorLocationLabelImg.place(x=70, y=160)

    editLocationLabel = Label(miniEditDoctorframe2, text="Location", font=("Arial", 12, "bold"), bg='powder blue')
    editLocationLabel.place(x=110, y=170)

    editLocation = StringVar()
    editLocationEntry = Entry(miniEditDoctorframe2, textvariable=editLocation, bg='sky blue', font=("Arial", 12), bd=5,
                        relief=GROOVE,
                        width=30)
    editLocationEntry.place(x=210, y=170)

    editDoctorAttendanceLabelImg = Label(miniEditDoctorframe2, image=attandance, font=("Arial", 12, "bold"), bg='powder blue')
    editDoctorAttendanceLabelImg.place(x=71, y=215)

    editDoctorAttendanceLabel = Label(miniEditDoctorframe2, text="Attendance", font=("Arial", 12, "bold"), bg='powder blue')
    editDoctorAttendanceLabel.place(x=110, y=222)

    editAttandance = StringVar()
    editAttandanceEntry = Entry(miniEditDoctorframe2, textvariable=editAttandance, bg='sky blue', font=("Arial", 12), bd=5,
                        relief=GROOVE, width=30)
    editAttandanceEntry.place(x=210, y=220)

    editDoctorStatusLabelImg = Label(miniEditDoctorframe2, image=status, font=("Arial", 12, "bold"), bg='powder blue')
    editDoctorStatusLabelImg.place(x=70, y=268)

    editDoctorStatusLabel = Label(miniEditDoctorframe2, text="Status", font=("Arial", 12, "bold"), bg='powder blue')
    editDoctorStatusLabel.place(x=110, y=272)


    # Create a combobox (dropdown menu)
    options = ["free", "busy"]
    editStatus = ttk.Combobox(miniEditDoctorframe2, values=options, state="readonly",font=("Arial", 12), width=30)
    editStatus.place(x=210, y=270)  # Place the combobox at x=190, y=270

    def editDoctorsavebtnfun():
        isEdited = False
        current_location=0
        getDoctorDetailQuery = rf"select name,current_status,location_id from doctor where id = '{editDoctorId.get()}'"
        doctor_detail_result = execute_query(getDoctorDetailQuery) 
        for i in doctor_detail_result:
            current_location=i[2]
            if i[0] != editDoctorName.get() or i[1] != editStatus.get():
                isEdited = True

        if editDoctorName.get() == '' or editLocation.get() == '' or editAttandance.get() == '' or editStatus.get() == '':
            messagebox.showinfo("INFORMATION", "Any Field Cannot be Empty !!!", parent=dashwin)
        else:
            if isEdited:
                query = rf'UPDATE doctor SET name = "{editDoctorName.get()}" , attendance = "{editAttandance.get()}" ,location_id = "{current_location}" , current_status = "{editStatus.get()}" WHERE id ="{editDoctorId.get()}"'
                rowCount = execute_query(query)
                if rowCount ==1:
                    messagebox.showinfo("INFORMATION", "Doctor Successfully Updated !!!", parent=dashwin)
                    editDoctorName.set('')
                    editLocation.set('')
                    editAttandance.set('')
                    editStatus.set("")
                    editDoctorId.set('')
                    miniEditDoctorframe2.place_forget()
                    miniEditdoctorframe.place(x=180, y=100)

                else:
                    messagebox.showerror("ERROR", "Doctor Failed To Updated !!!", parent=dashwin)
                    editDoctorName.set('')
                    editLocation.set('')
                    editAttandance.set('')
                    editStatus.set('')
                    editDoctorId.set('')
                    miniEditDoctorframe2.place_forget()
                    miniEditdoctorframe.place(x=180, y=100)
            else:
                messagebox.showinfo("INFORMATION", "Doctor Details are same !!!", parent=dashwin)
                miniEditDoctorframe2.place_forget()
                miniEditdoctorframe.place(x=180, y=100)
            
    editDoctorsavebtn = Button(miniEditDoctorframe2, text="SAVE", bg='blue2', fg='white', activebackground='red',
                                bd=5,
                                activeforeground='white'
                                , width=8, font=("Arial", 12, "bold"), command=editDoctorsavebtnfun)
    editDoctorsavebtn.place(x=310, y=320)

    ## Edit Doctor button
    edit_doctorbtn = Button(dashboardframe, text="Edit Doctor", font=("Arial", 12, "bold italic"), fg='white',
                        bg="#B07138",
                        activebackground='red'
                        , activeforeground='white', bd=10, width=150, height=40, image=editDoctorBtnIcon, compound='left',
                        command=lambda: raise_frame(editDoctorframe))
    edit_doctorbtn.place(x=30, y=130)


    def showAllDoctor():
        ## Search Doctor Frame
        showDoctorframe = Frame(dashwin, bg="#AAC8C6", relief='ridge', bd=4)
        showDoctorframe.place(x=0, y=132, relwidth=1,height =418)

        ShowDoctorframeBgImg = Label(showDoctorframe, image=viewPatientFramebg)
        ShowDoctorframeBgImg.place(x=0, y=0, relwidth=1, relheight=1)

        showAllPateient_backBtn = Button(showDoctorframe, bd=5, font=("Arial", 14, "bold"), image=backbtnimg,
                                command=lambda: raise_frame(dashboardframe),bg= '#AAC8C6')
        showAllPateient_backBtn.place(x=10, y=10)

        MinisearchDoctorFrame = Frame(showDoctorframe, width=500, height=70, bd=5, relief='ridge', bg='#AAC8C6')
        MinisearchDoctorFrame.place(x=220, y=10)

        SearchDoctorIdLabelImg = Label(MinisearchDoctorFrame, image=UserIdimg, font=("Arial", 12, "bold"), bg='#AAC8C6')
        SearchDoctorIdLabelImg.place(x=20, y=10)

        SearchDoctoridLabel = Label(MinisearchDoctorFrame, text="Doctor ID :", font=("Arial", 12, "bold"), bg='#AAC8C6')
        SearchDoctoridLabel.place(x=60, y=15)

        SearchDoctoridEntryval = StringVar()
        SearchDoctoridEntry = Entry(MinisearchDoctorFrame, textvariable=SearchDoctoridEntryval, bg='snow',
                                font=("Arial", 12), bd=5,
                                relief=GROOVE,
                                width=10)
        SearchDoctoridEntry.place(x=150, y=13)

        def SearchDoctorSubmitbtnfun():
            if SearchDoctoridEntryval.get() == '':
                messagebox.showinfo('INFORMATION', 'Search Doctor Id cannot Be Empty...', parent=dashwin)
            else:
                query = rf'select dt.id,dt.name,dt.current_status,dt.attendance,ln.room_number,ln.floor_number from doctor dt join location ln on dt.location_id= ln.id where dt.id= "{SearchDoctoridEntryval.get()}";'
                result = execute_query(query)
                if result:
                    for i in result:
                        allDoctorinfoTable.delete(*allDoctorinfoTable.get_children())
                        tabVal = [i[0], i[1],i[2], i[3], f"Room {i[4]} on Floor {i[5]}"]   
                        allDoctorinfoTable.insert('', END, values=tabVal)
                else:
                    messagebox.showinfo('INFORMATION', 'No Doctor Available With Such Doctor Id...', parent=dashwin)

        def SearchDoctorResetbtnfun():
            SearchDoctoridEntryval.set('')
            allDoctorinfoTable.delete(*allDoctorinfoTable.get_children())
            query = 'select dt.id,dt.name,dt.current_status,dt.attendance,ln.room_number,ln.floor_number from doctor dt join location ln on dt.location_id= ln.id;'
            data = execute_query(query)
            for i in data:
                tabVal = [i[0], i[1], i[2], i[3], f"Room {i[4]} on Floor {i[5]}"]   
                allDoctorinfoTable.insert('', END, values = tabVal)


        SearchDoctorbtn = Button(MinisearchDoctorFrame, text="Search", bg='blue2', fg='white',
                                        activebackground='red',
                                        bd=5,
                                        activeforeground='white'
                                        , width=8, font=("Arial", 12, "bold"), command=SearchDoctorSubmitbtnfun)
        SearchDoctorbtn.place(x=270, y= 10)

        ResetDoctorbtn = Button(MinisearchDoctorFrame, text="Reset", bg='blue2', fg='white',
                                        activebackground='red',
                                        bd=5,
                                        activeforeground='white'
                                        , width=8, font=("Arial", 12, "bold"), command=SearchDoctorResetbtnfun)
        ResetDoctorbtn.place(x=380, y= 10)

        MinishowAll_DcotorFrame = Frame(showDoctorframe, width=850, height=10, bd=4, relief='ridge',bg = '#AAC8C6')
        MinishowAll_DcotorFrame.place(x=25, y=90)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', font=('times', 15, 'italic'),fieldbackground = '#AAC8C6',
                        background = '#AAC8C6',foreground='red',rowheight = 25)
        style.configure('Treeview.Heading', font=('times', 15, 'italic'), background='sky blue')
        style.map('Treeview',background = [('selected','blue2')])

        Scroll_x = Scrollbar(MinishowAll_DcotorFrame, orient=HORIZONTAL)
        Scroll_y = Scrollbar(MinishowAll_DcotorFrame, orient=VERTICAL )

        allDoctorinfoTable = Treeview(MinishowAll_DcotorFrame, columns=('ID', 'Name', 'Availability', 'Attendance', 'Location'),
                                    xscrollcommand=Scroll_x.set, yscrollcommand=Scroll_y.set)

        Scroll_x.pack(side=BOTTOM, fill=X ,anchor = W)
        Scroll_y.pack(side=RIGHT, fill=Y ,anchor = N)
        Scroll_x.configure(command=allDoctorinfoTable.xview)
        Scroll_y.configure(command=allDoctorinfoTable.yview)

        # Treeview Column Formate
        allDoctorinfoTable.column('ID', width=90, anchor=CENTER)
        allDoctorinfoTable.column('Name', width=180, anchor=CENTER)
        allDoctorinfoTable.column('Availability', width=150, anchor=CENTER)
        allDoctorinfoTable.column('Attendance', width=150, anchor=CENTER)
        allDoctorinfoTable.column('Location', width=240, anchor=CENTER)

        # Treeview Heading Tect
        allDoctorinfoTable.heading('ID', text='ID'.upper())
        allDoctorinfoTable.heading('Name', text='Name'.upper())
        allDoctorinfoTable.heading('Availability', text='Availability'.upper())
        allDoctorinfoTable.heading('Attendance', text='Attendance'.upper())
        allDoctorinfoTable.heading('Location', text='Location'.upper())


        allDoctorinfoTable.configure(show='headings')

        allDoctorinfoTable.pack(fill='both')

        query = 'select dt.id,dt.name,dt.current_status,dt.attendance,ln.room_number,ln.floor_number from doctor dt join location ln on dt.location_id= ln.id;'
        data = execute_query(query)
        for i in data:
            tabVal = [i[0], i[1],i[2], i[3], f"Room {i[4]} on Floor {i[5]}"]     
            allDoctorinfoTable.insert('', END, values = tabVal)


    show_doctorbtn = Button(dashboardframe, text="View Doctor", font=("Arial", 12, "bold italic"), fg='white',
                        bg="#B07138",
                        activebackground='red'
                        , activeforeground='white', bd=10, width=150, height=40, image=viewBtnIcon,
                        compound='left',command=showAllDoctor)
    show_doctorbtn.place(x=300, y=130)
    
    # Delete Doctor Button Frame
    deleteDoctorframe = Frame(dashwin, bg="#FEBDAB", relief='ridge', bd=5)
    deleteDoctorframe.place(x=0, y=132, relwidth=1,height = 418)

    deleteDoctorframeBgImg = Label(deleteDoctorframe, image=deleteDoctorFrameBg)
    deleteDoctorframeBgImg.place(x=0, y=0, relwidth=1, relheight=1)

    DeleteDoctorBackbtn = Button(deleteDoctorframe, bd=5, font=("Arial", 14, "bold"), image=backbtnimg,
                            command=lambda: raise_frame(dashboardframe),bg='#FEBDAB')
    DeleteDoctorBackbtn.place(x=10, y=10)

    ## Delete Doctor Mini Frame 1
    miniDeleteDoctorframe = Frame(deleteDoctorframe, bg='#FEBDAB', height=200, width=550, relief='ridge', bd=4)
    miniDeleteDoctorframe.place(x=180, y=100)

    deleteDoctorframe_title = Label(miniDeleteDoctorframe, text="DELETE DOCTOR", bg="#006600", font=("Arial", 15, "bold"),
                                relief='groove', fg='white', width=41)
    deleteDoctorframe_title.place(x=20, y=10)

    deleteDoctorIdLabelImg = Label(miniDeleteDoctorframe, image=UserIdimg, font=("Arial", 12, "bold"), bg='#FEBDAB')
    deleteDoctorIdLabelImg.place(x=140, y=70)

    deleteDoctorIdLabel = Label(miniDeleteDoctorframe, text="Doctor ID :", font=("Arial", 12, "bold"), bg='#FEBDAB')
    deleteDoctorIdLabel.place(x=180, y=75)

    deleteDoctorIdEntryval = StringVar()
    deleteDoctorIdEntry = Entry(miniDeleteDoctorframe, textvariable=deleteDoctorIdEntryval, font=("Arial", 12), bd=5,
                            relief=GROOVE,
                            width=10)
    deleteDoctorIdEntry.place(x=270, y=75)

    def deleteDoctorsubmitbtnfun():
        if deleteDoctorIdEntryval.get() == '':
            messagebox.showinfo("INFORMATION","Doctor ID cannot be Empty !!!" ,parent = dashwin )
        else:
            query = rf'select dt.name,dt.attendance, dt.current_status,ln.room_number,ln.floor_number from doctor dt join location ln on dt.location_id= ln.id where dt.id= "{deleteDoctorIdEntryval.get()}";'
            result = execute_query(query)
            if result:
                for i in result:
                    pass
                    deleteDoctorNameval.set(i[0])
                    deleteDoctorAtendanceval.set(i[1])
                    deleteDoctorStatusval.set(i[2])
                    deleteDoctorLocationval.set(f"Room {i[3]} on Floor {i[4]}")
                miniDeleteDoctorframe.place_forget()
                miniDeleteDoctorframe2.place(x=160, y=20)
                deleteDoctorIdEntry2.configure(state = 'disable')
                deleteDoctorNameEntry.configure(state = 'disable')
                deleteDoctorLocationEntry.configure(state = 'disable')
                deleteDoctorAttendanceEntry.configure(state = 'disable')
                deleteDoctorStatusEntry.configure(state = 'disable')

            else:
                messagebox.showinfo("INFORMATION", "No Doctor There With Such ID !!!", parent=dashwin)

    deleteDoctorsubmitbtn = Button(miniDeleteDoctorframe, text="Submit", bg='blue2', fg='white', activebackground='red', bd=5,
                            activeforeground='white'
                            , width=8, font=("Arial", 12, "bold"), command=deleteDoctorsubmitbtnfun)
    deleteDoctorsubmitbtn.place(x=310, y=140)

    ## edit Doctor MiniFrame2

    miniDeleteDoctorframe2 = Frame(deleteDoctorframe, bg='#FEBDAB', height=380, width=550, relief='ridge', bd=4)
    miniDeleteDoctorframe2.place_forget()

    deleteDoctorframe_title2 = Label(miniDeleteDoctorframe2, text="DELETE DOCTOR", bg="#006600", font=("Arial", 15, "bold"),
                                relief='groove', fg='white', width=41)
    deleteDoctorframe_title2.place(x=20, y=10)

    deleteDoctorIdLabelImg2 = Label(miniDeleteDoctorframe2, image=UserIdimg, font=("Arial", 12, "bold"), bg='#FEBDAB')
    deleteDoctorIdLabelImg2.place(x=70, y=65)

    deleteDoctorIdLabel2 = Label(miniDeleteDoctorframe2, text="Doctor ID :", font=("Arial", 12, "bold"), bg='#FEBDAB')
    deleteDoctorIdLabel2.place(x=110, y=70)

    deleteDoctorIdEntry2 = Entry(miniDeleteDoctorframe2, textvariable=deleteDoctorIdEntryval, bg='sky blue', font=("Arial", 12), bd=5,
                            relief=GROOVE,
                            width=10)
    deleteDoctorIdEntry2.place(x=190, y=70)

    deleteDoctorNameLabelImg = Label(miniDeleteDoctorframe2, image=fullname, font=("Arial", 12, "bold"), bg='#FEBDAB')
    deleteDoctorNameLabelImg.place(x=70, y=112)

    deleteDoctorNameLabel = Label(miniDeleteDoctorframe2, text="NAME :", font=("Arial", 12, "bold"), bg='#FEBDAB')
    deleteDoctorNameLabel.place(x=110, y=122)

    deleteDoctorNameval = StringVar()
    deleteDoctorNameEntry = Entry(miniDeleteDoctorframe2, textvariable=deleteDoctorNameval, bg='sky blue', font=("Arial", 12),
                            bd=5, relief=GROOVE,
                            width=30)
    deleteDoctorNameEntry.place(x=190, y=120)

    deleteDoctorLocationLabelImg = Label(miniDeleteDoctorframe2, image=location, font=("Arial", 12, "bold"), bg='#FEBDAB')
    deleteDoctorLocationLabelImg.place(x=70, y=160)

    deleteDoctorLocationLabel = Label(miniDeleteDoctorframe2, text="Location", font=("Arial", 12, "bold"), bg='#FEBDAB')
    deleteDoctorLocationLabel.place(x=110, y=170)

    deleteDoctorLocationval = StringVar()
    deleteDoctorLocationEntry = Entry(miniDeleteDoctorframe2, textvariable=deleteDoctorLocationval, bg='sky blue', font=("Arial", 12),
                                bd=5,
                                relief=GROOVE,
                                width=30)
    deleteDoctorLocationEntry.place(x=190, y=170)

    deleteDoctorAttendenceLabelImg = Label(miniDeleteDoctorframe2, image=attandance, font=("Arial", 12, "bold"), bg='#FEBDAB')
    deleteDoctorAttendenceLabelImg.place(x=71, y=215)

    deleteDoctorAttendanceLabel = Label(miniDeleteDoctorframe2, text="Attendance", font=("Arial", 12, "bold"), bg='#FEBDAB')
    deleteDoctorAttendanceLabel.place(x=110, y=222)

    deleteDoctorAtendanceval = StringVar()
    deleteDoctorAttendanceEntry = Entry(miniDeleteDoctorframe2, textvariable=deleteDoctorAtendanceval, bg='sky blue', font=("Arial", 12),
                                bd=5,
                                relief=GROOVE, width=30)
    deleteDoctorAttendanceEntry.place(x=190, y=220)

    deleteDoctorStatusLabelImg = Label(miniDeleteDoctorframe2, image=status, font=("Arial", 12, "bold"), bg='#FEBDAB')
    deleteDoctorStatusLabelImg.place(x=70, y=268)

    deleteDoctorStatusLabel = Label(miniDeleteDoctorframe2, text="Status", font=("Arial", 12, "bold"), bg='#FEBDAB')
    deleteDoctorStatusLabel.place(x=110, y=272)

    deleteDoctorStatusval = StringVar()
    deleteDoctorStatusEntry = Entry(miniDeleteDoctorframe2, textvariable=deleteDoctorStatusval, bg='sky blue', font=("Arial", 12),
                            bd=5, relief=GROOVE,
                            width=10)
    deleteDoctorStatusEntry.place(x=190, y=270)

    def DoctorDeletebtnfun():
        delCon = messagebox.askyesno("CONFIRM","Do You Really Want To Delete This Doctor  !!!",parent = dashwin)
        if delCon == True :
            query = rf'DELETE FROM doctor  WHERE id = "{deleteDoctorIdEntryval.get()}"'
            rowCount = execute_query(query)
            if rowCount == 1:
                messagebox.showinfo("INFORMATION", "Doctor SuccessFully Deleted !!!", parent=dashwin)
                deleteDoctorNameval.set('')
                deleteDoctorLocationval.set('')
                deleteDoctorAtendanceval.set('')
                deleteDoctorStatusval.set('')
                deleteDoctorIdEntryval.set('')
                miniDeleteDoctorframe2.place_forget()
                miniDeleteDoctorframe.place(x=180, y=100)
            else:
                messagebox.showerror("ERROR", "Doctor Failed To Delete !!!", parent=dashwin)
                deleteDoctorNameval.set('')
                deleteDoctorLocationval.set('')
                deleteDoctorAtendanceval.set('')
                deleteDoctorStatusval.set('')
                deleteDoctorIdEntryval.set('')
                miniDeleteDoctorframe2.place_forget()
                miniDeleteDoctorframe.place(x=180, y=100)

    DeleteDoctordeletebtn = Button(miniDeleteDoctorframe2, text="DELETE", bg='blue2', fg='white', activebackground='red',
                                bd=5,
                                activeforeground='white'
                                , width=8, font=("Arial", 12, "bold"), command = DoctorDeletebtnfun)
    DeleteDoctordeletebtn.place(x=310, y=320)



    delete_Doctorbtn = Button(dashboardframe, text="Delete Doctor", font=("Arial", 12, "bold italic"), fg='white',
                        bg="#B07138",
                        activebackground='red',
                        activeforeground='white', bd=10, width=150, height=40, image=deleteDoctorBtnIcon, compound='left',
                        command=lambda: raise_frame(deleteDoctorframe))
    delete_Doctorbtn.place(x=30, y=225)


    def logoutbtnfun():
        logres = messagebox.askyesno("Confirmation", "Do you really want to logout?", parent=dashwin)
        if logres == True:
            ##Destroy Top
            dashwin.destroy()
            dashwin.update()
            disconnect_database()
            ## Back to Login Frame
            root.update()
            root.deiconify()
            username.set('')
            password.set('')
            on_connect()

    logoutbtn = Button(dashboardframe, text="  Log Out", font=("Arial", 12, "bold italic"), fg='white',
                            bg="#B07138",
                            activebackground='red'
                            , activeforeground='white', bd=10, width=150, height=40, image=logoutimg,
                            compound='left', command=logoutbtnfun)
    logoutbtn.place(x=300, y=225)
    dashboardframe.tkraise()


open_toplevel(root)
root.mainloop()
