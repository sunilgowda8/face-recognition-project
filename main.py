from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter
import tkinter as tk
import tkinter.messagebox as messagebox
import os
import mysql.connector
from train import Train
from attendance import Attendance
from face_recognition import Face_Recognition
from deveoper import Developer
from help import Helpsupport
from time import strftime
from Student import Student

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Face Recognition System")
        self.root.geometry("1366x768+0+0")

        # variables 
        self.var_ssq = StringVar()
        self.var_sa = StringVar()
        self.var_pwd = StringVar()

        # Background image
        self.bg = ImageTk.PhotoImage(file=r"college_iimages\gg.jpg")
        lb1_bg = Label(self.root, image=self.bg)
        lb1_bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame1 = Frame(self.root, bg="#002B53")
        frame1.place(x=560, y=170, width=340, height=450)

        # Logo
        img1 = Image.open(r"college_iimages\ff.jpg")
        img1 = img1.resize((100, 100), Image.LANCZOS)
        self.photoimage1 = ImageTk.PhotoImage(img1)
        lb1img1 = Label(image=self.photoimage1, bg="#002B53")
        lb1img1.place(x=690, y=175, width=100, height=100)

        # title section
        title_lb1 = Label(self.root, text="WELCOME TO FACE RECOGNITION SYSTEM", 
                         font=("times new roman", 25, "bold"), bg="white", fg="Blue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # College image button
        img1_btn = Image.open(r"college_iimages\gg.jpg")
        img1_btn = img1_btn.resize((180, 180), Image.LANCZOS)
        self.img1 = ImageTk.PhotoImage(img1_btn)

        std_b1 = Button(self.root, image=self.img1, cursor="hand2")
        std_b1.place(x=250, y=200, width=200, height=200)

        std_b1_1 = Button(self.root, text="Face Recognition", cursor="hand2", 
                         font=("tahoma", 15, "bold"), bg="white", fg="black")
        std_b1_1.place(x=250, y=380, width=200, height=45)

        get_str = Label(frame1, text="Login", font=("times new roman", 20, "bold"), 
                       fg="white", bg="#002B53")
        get_str.place(x=140, y=100)    

        # Username
        username = Label(frame1, text="Username:", font=("times new roman", 15, "bold"), 
                        fg="white", bg="#002B53")
        username.place(x=30, y=160)

        self.txtuser = ttk.Entry(frame1, font=("times new roman", 15, "bold"))
        self.txtuser.place(x=33, y=190, width=270)

        # Password
        pwd = Label(frame1, text="Password:", font=("times new roman", 15, "bold"), 
                   fg="white", bg="#002B53")
        pwd.place(x=30, y=230)

        self.txtpwd = ttk.Entry(frame1, show="*", font=("times new roman", 15, "bold"))
        self.txtpwd.place(x=33, y=260, width=270)

        # Login Button
        loginbtn = Button(frame1, command=self.login, text="Login", 
                         font=("times new roman", 15, "bold"), bd=0, relief=RIDGE, 
                         fg="#002B53", bg="white", activeforeground="white", 
                         activebackground="#007ACC")
        loginbtn.place(x=33, y=320, width=270, height=35)

        # Forget Password Button
        forget_btn = Button(frame1, command=self.forget_pwd, text="Forget Password", 
                         font=("times new roman", 10, "bold"), bd=0, relief=RIDGE, 
                         fg="white", bg="#002B53", activeforeground="orange", 
                         activebackground="#002B53")
        forget_btn.place(x=33, y=370, width=100, height=20)

    def login(self):
        if self.txtuser.get() == "" or self.txtpwd.get() == "":
            messagebox.showerror("Error", "All Fields Required!")
            return
        
        # Always allow admin login
        if self.txtuser.get() == "admin" and self.txtpwd.get() == "admin":
            messagebox.showinfo("Success", "Welcome to Face Recognition Attendance System")
            self.open_main_system()
            return
        
        # Try MySQL connection for other users
        conn = self.get_mysql_connection()
        if conn is None:
            messagebox.showerror("Database Error", 
                "Cannot connect to MySQL database.\n\n"
                "Please use:\nUsername: admin\nPassword: admin\n\n"
                "Or ensure MySQL is running and database exists.")
            return
        
        try:
            mycursor = conn.cursor()
            mycursor.execute("SELECT * FROM regteach WHERE email=%s AND pwd=%s", 
                           (self.txtuser.get(), self.txtpwd.get()))
            row = mycursor.fetchone()
            
            if row is None:
                messagebox.showerror("Error", "Invalid Username and Password!")
            else:
                open_min = messagebox.askyesno("Access", "Access only Admin")
                if open_min:
                    self.open_main_system()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Database query error: {e}")
        finally:
            if conn:
                conn.close()

    def get_mysql_connection(self):
        """Try to establish MySQL connection with multiple options"""
        connection_options = [
            {'host': 'localhost', 'user': 'root', 'password': '', 'database': 'face_recognition'},
            {'host': 'localhost', 'user': 'root', 'password': 'root', 'database': 'face_recognition'},
            {'host': 'localhost', 'user': 'root', 'password': 'password', 'database': 'face_recognition'},
        ]
        
        for options in connection_options:
            try:
                conn = mysql.connector.connect(**options)
                return conn
            except mysql.connector.Error:
                continue
        
        return None

    def open_main_system(self):
        self.root.destroy()  # Close login window
        root = Tk()
        app = FaceRecognitionSystem(root)
        root.mainloop()

    def reset_pass(self):
        if self.var_ssq.get() == "Select":
            messagebox.showerror("Error", "Select the Security Question!", parent=self.root2)
        elif self.var_sa.get() == "":
            messagebox.showerror("Error", "Please Enter the Answer!", parent=self.root2)
        elif self.var_pwd.get() == "":
            messagebox.showerror("Error", "Please Enter the New Password!", parent=self.root2)
        else:
            conn = self.get_mysql_connection()
            if conn is None:
                messagebox.showerror("Database Error", "Cannot connect to database. Please use admin login.", parent=self.root2)
                return
                
            try:
                mycursor = conn.cursor()
                query = "SELECT * FROM regteach WHERE email=%s AND ss_que=%s AND s_ans=%s"
                value = (self.txtuser.get(), self.var_ssq.get(), self.var_sa.get())
                mycursor.execute(query, value)
                row = mycursor.fetchone()
                
                if row is None:
                    messagebox.showerror("Error", "Please Enter the Correct Answer!", parent=self.root2)
                else:
                    query = "UPDATE regteach SET pwd=%s WHERE email=%s"
                    value = (self.var_pwd.get(), self.txtuser.get())
                    mycursor.execute(query, value)
                    conn.commit()
                    messagebox.showinfo("Info", "Password reset successfully! Please login with new password.", parent=self.root2)
                    self.root2.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}", parent=self.root2)
            finally:
                if conn:
                    conn.close()

    def forget_pwd(self):
        if self.txtuser.get() == "":
            messagebox.showerror("Error", "Please Enter the Email ID to reset Password!")
            return

        conn = self.get_mysql_connection()
        if conn is None:
            messagebox.showerror("Database Error", 
                "Cannot connect to MySQL database.\n"
                "Password reset feature unavailable.\n"
                "Please use admin login or start MySQL service.")
            return

        try:
            mycursor = conn.cursor()
            query = "SELECT * FROM regteach WHERE email=%s"
            value = (self.txtuser.get(),)
            mycursor.execute(query, value)
            row = mycursor.fetchone()

            if row is None:
                messagebox.showerror("Error", "Please Enter a Valid Email ID!")
            else:
                self.root2 = Toplevel(self.root)
                self.root2.title("Forget Password")
                self.root2.geometry("400x400+610+170")
                self.root2.configure(bg="#F2F2F2")
                self.root2.resizable(False, False)
                
                l = Label(self.root2, text="Forget Password", 
                         font=("times new roman", 20, "bold"), 
                         fg="#002B53", bg="#F2F2F2")
                l.place(x=0, y=10, relwidth=1)

                # Security Question
                ssq = Label(self.root2, text="Select Security Question:", 
                           font=("times new roman", 12, "bold"), 
                           fg="#002B53", bg="#F2F2F2")
                ssq.place(x=70, y=80)

                self.combo_security = ttk.Combobox(self.root2, textvariable=self.var_ssq, 
                                                  font=("times new roman", 12), 
                                                  state="readonly")
                self.combo_security["values"] = ("Select", "Your Date of Birth", 
                                               "Your Nick Name", "Your Favorite Book")
                self.combo_security.current(0)
                self.combo_security.place(x=70, y=110, width=270)

                # Security Answer
                sa = Label(self.root2, text="Security Answer:", 
                          font=("times new roman", 12, "bold"), 
                          fg="#002B53", bg="#F2F2F2")
                sa.place(x=70, y=150)

                self.txt_sa = ttk.Entry(self.root2, textvariable=self.var_sa, 
                                       font=("times new roman", 12))
                self.txt_sa.place(x=70, y=180, width=270)

                # New Password
                new_pwd = Label(self.root2, text="New Password:", 
                               font=("times new roman", 12, "bold"), 
                               fg="#002B53", bg="#F2F2F2")
                new_pwd.place(x=70, y=220)

                self.new_pwd_entry = ttk.Entry(self.root2, textvariable=self.var_pwd, 
                                              show="*", font=("times new roman", 12))
                self.new_pwd_entry.place(x=70, y=250, width=270)

                # Reset Password Button
                reset_btn = Button(self.root2, command=self.reset_pass, text="Reset Password", 
                                  font=("times new roman", 12, "bold"), bd=0, relief=RIDGE, 
                                  fg="#fff", bg="#002B53", 
                                  activeforeground="white", activebackground="#007ACC")
                reset_btn.place(x=70, y=300, width=270, height=35)

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            if conn:
                conn.close()


class FaceRecognitionSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # Load and resize the first image
        img = Image.open(r"college_iimages\KK1.jpeg")
        img = img.resize((500, 150), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=500, height=150)

        # Load and resize the second image
        img1 = Image.open(r"college_iimages\JSS.jpeg")
        img1 = img1.resize((500, 150), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        f_lbl1 = Label(self.root, image=self.photoimg1)
        f_lbl1.place(x=500, y=0, width=500, height=150)

        # Load and resize the third image
        img2 = Image.open(r"college_iimages\KK1.jpeg")
        img2 = img2.resize((500, 150), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        f_lbl2 = Label(self.root, image=self.photoimg2)
        f_lbl2.place(x=1000, y=0, width=500, height=150)

        # Background image
        img3 = Image.open(r"college_iimages\face.jpeg")
        img3 = img3.resize((1530, 710), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        self.bg_img = Label(self.root, image=self.photoimg3)
        self.bg_img.place(x=0, y=150, width=1530, height=710)

        # Title
        title_lbl = Label(self.bg_img, text="FACE RECOGNITION ATTENDANCE SYSTEM SOFTWARE", 
                          font=("Times New Roman", 35, "bold"), bg="white", fg="red")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # ============ TIME DISPLAY ============
        time_lbl = Label(title_lbl, font=('times new roman', 14, 'bold'), 
                        background='white', foreground='blue')
        time_lbl.place(x=0, y=0, width=110, height=50)
        self.update_time(time_lbl)  # Start the time update

        # Student Button
        img4 = Image.open(r"college_iimages\button.jpeg")
        img4 = img4.resize((220, 220), Image.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)

        b1 = Button(self.bg_img, image=self.photoimg4, command=self.student_details, cursor="hand2")
        b1.place(x=200, y=100, width=220, height=220)

        b1_text = Button(self.bg_img, text="Student Details", command=self.student_details,
                         font=("tahoma", 15, "bold"), bg="blue", fg="white", cursor="hand2")
        b1_text.place(x=200, y=320, width=220, height=40)

        # Face Detector Button
        img5 = Image.open(r"college_iimages\face1.jpeg")
        img5 = img5.resize((220, 220), Image.LANCZOS)
        self.photoimg5 = ImageTk.PhotoImage(img5)

        b2 = Button(self.bg_img, image=self.photoimg5, cursor="hand2", command=self.face_data)
        b2.place(x=500, y=100, width=220, height=220)

        b2_text = Button(self.bg_img, text="Face Detector", cursor="hand2",
                         font=("tahoma", 15, "bold"), bg="blue", fg="white", command=self.face_data)
        b2_text.place(x=500, y=320, width=220, height=40)

        # Attendance Button
        img6 = Image.open(r"college_iimages\attendance.jpg")
        img6 = img6.resize((220, 220), Image.LANCZOS)
        self.photoimg6 = ImageTk.PhotoImage(img6)

        b3 = Button(self.bg_img, image=self.photoimg6, cursor="hand2",command=self.attendance_data)
        b3.place(x=800, y=100, width=220, height=220)

        b3_text = Button(self.bg_img, text="Attendance", cursor="hand2",command=self.attendance_data,
                         font=("tahoma", 15, "bold"), bg="blue", fg="white")
        b3_text.place(x=800, y=320, width=220, height=40)

        # Help Desk Button
        img7 = Image.open(r"college_iimages\help.jpeg")
        img7 = img7.resize((220, 220), Image.LANCZOS)
        self.photoimg7 = ImageTk.PhotoImage(img7)

        b4 = Button(self.bg_img, image=self.photoimg7, cursor="hand2",command=self.help_data)
        b4.place(x=1100, y=100, width=220, height=220)

        b4_text = Button(self.bg_img, text="Help Desk", cursor="hand2",command=self.help_data,
                         font=("tahoma", 15, "bold"), bg="blue", fg="white")
        b4_text.place(x=1100, y=320, width=220, height=40)

        # Train Data Button
        img8 = Image.open(r"college_iimages\DATA.jpeg")
        img8 = img8.resize((220, 220), Image.LANCZOS)
        self.photoimg8 = ImageTk.PhotoImage(img8)

        b5 = Button(self.bg_img, image=self.photoimg8, cursor="hand2", command=self.train_data)
        b5.place(x=200, y=400, width=220, height=220)

        b5_text = Button(self.bg_img, text="Train Data", cursor="hand2",
                         font=("tahoma", 15, "bold"), bg="blue", fg="white", command=self.train_data)
        b5_text.place(x=200, y=600, width=220, height=40)

        # Photo Button (Image)
        img9 = Image.open(r"college_iimages\photo.jpeg")
        img9 = img9.resize((220, 220), Image.LANCZOS)
        self.photoimg9 = ImageTk.PhotoImage(img9)

        b6 = Button(self.bg_img, image=self.photoimg9, cursor="hand2", command=self.open_photos)
        b6.place(x=500, y=400, width=220, height=220)

        # Photo Button (Text)
        b6_text = Button(self.bg_img, text="Photos", cursor="hand2", command=self.open_photos,
                 font=("tahoma", 15, "bold"), bg="blue", fg="white")
        b6_text.place(x=500, y=600, width=220, height=40)

        # Developer Button
        img10 = Image.open(r"college_iimages\deleper.jpg")
        img10 = img10.resize((220, 220), Image.LANCZOS)
        self.photoimg10 = ImageTk.PhotoImage(img10)

        b7 = Button(self.bg_img, image=self.photoimg10, cursor="hand2",command=self.developer_data)
        b7.place(x=800, y=400, width=220, height=220)

        b7_text = Button(self.bg_img, text="Developer", cursor="hand2",command=self.developer_data, 
                         font=("tahoma", 15, "bold"), bg="blue", fg="white")
        b7_text.place(x=800, y=600, width=220, height=40)

        # Exit Button
        img11 = Image.open(r"college_iimages\exit.jpeg")
        img11 = img11.resize((220, 220), Image.LANCZOS)
        self.photoImg11 = ImageTk.PhotoImage(img11)

        b8 = Button(self.bg_img, image=self.photoImg11, cursor="hand2", command=self.iExit)
        b8.place(x=1100, y=400, width=220, height=220)

        b8_text = Button(self.bg_img, text="Exit", cursor="hand2", command=self.iExit, 
                 font=("tahoma", 15, "bold"), bg="blue", fg="white")
        b8_text.place(x=1100, y=600, width=220, height=40)

    # ============ TIME UPDATE FUNCTION ============
    def update_time(self, time_label):
        string = strftime('%H:%M:%S %p')
        time_label.config(text=string)
        time_label.after(1000, lambda: self.update_time(time_label))

    # ============ Functions ============
    def iExit(self):
        result = tkinter.messagebox.askyesno("Face Recognition", "Are you sure you want to exit this project?")
        if result:
            self.root.destroy()

    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    def face_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)

    def attendance_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

    def developer_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Developer(self.new_window)

    def help_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Helpsupport(self.new_window)

    def open_photos(self):
        try:
            os.startfile("dataset")
        except:
            messagebox.showinfo("Info", "Dataset folder not found!")


if __name__ == "__main__":
    # Start with login screen
    root = Tk()
    app = Login(root)
    root.mainloop()