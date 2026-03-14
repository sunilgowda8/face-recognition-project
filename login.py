from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
# --------------------------
from train import Train
from Student import Student
from face_recognition import Face_Recognition 
from attendance import Attendance
from deveoper import Developer
from help import Helpsupport 
import os


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1366x768+0+0")

        # variables 
        self.var_ssq = StringVar()
        self.var_sa = StringVar()
        self.var_pwd = StringVar()

        self.bg = ImageTk.PhotoImage(file=r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\gg.jpg")
        
        lb1_bg = Label(self.root, image=self.bg)
        lb1_bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame1 = Frame(self.root, bg="#002B53")
        frame1.place(x=560, y=170, width=340, height=450)

        img1 = Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\ff.jpg")
        img1 = img1.resize((100, 100), Image.LANCZOS)
        self.photoimage1 = ImageTk.PhotoImage(img1)
        lb1img1 = Label(image=self.photoimage1, bg="#002B53")
        lb1img1.place(x=690, y=175, width=100, height=100)

        # title section
        title_lb1 = Label(self.root, text="WELCOME TO SRI SIDDHARTHA POLYTECHNIC", 
                         font=("times new roman", 30, "bold"), bg="white", fg="Blue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        img1_btn = Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\gg.jpg")
        img1_btn = img1_btn.resize((180, 180), Image.LANCZOS)
        self.img1 = ImageTk.PhotoImage(img1_btn)

        std_b1 = Button(self.root, image=self.img1, cursor="hand2")
        std_b1.place(x=250, y=200, width=200, height=200)

        std_b1_1 = Button(self.root, text="546-SSP", cursor="hand2", 
                         font=("tahoma", 15, "bold"), bg="white", fg="black")
        std_b1_1.place(x=250, y=380, width=200, height=45)

        get_str = Label(frame1, text="Login", font=("times new roman", 20, "bold"), 
                       fg="white", bg="#002B53")
        get_str.place(x=140, y=100)    

        # label1 
        username = Label(frame1, text="Username:", font=("times new roman", 15, "bold"), 
                        fg="white", bg="#002B53")
        username.place(x=30, y=160)

        # entry1 
        self.txtuser = ttk.Entry(frame1, font=("times new roman", 15, "bold"))
        self.txtuser.place(x=33, y=190, width=270)

        # label2 
        pwd = Label(frame1, text="Password:", font=("times new roman", 15, "bold"), 
                   fg="white", bg="#002B53")
        pwd.place(x=30, y=230)

        # entry2 
        self.txtpwd = ttk.Entry(frame1, show="*", font=("times new roman", 15, "bold"))
        self.txtpwd.place(x=33, y=260, width=270)

        # Creating Button Login
        loginbtn = Button(frame1, command=self.login, text="Login", 
                         font=("times new roman", 15, "bold"), bd=0, relief=RIDGE, 
                         fg="#002B53", bg="white", activeforeground="white", 
                         activebackground="#007ACC")
        loginbtn.place(x=33, y=320, width=270, height=35)

        # Creating Button Forget
        loginbtn = Button(frame1, command=self.forget_pwd, text="Forget Password", 
                         font=("times new roman", 10, "bold"), bd=0, relief=RIDGE, 
                         fg="white", bg="#002B53", activeforeground="orange", 
                         activebackground="#002B53")
        loginbtn.place(x=33, y=370, width=100, height=20)

    def login(self):
        if self.txtuser.get() == "" or self.txtpwd.get() == "":
            messagebox.showerror("Error", "All Fields Required!")
            return
        
        # Always allow admin login
        if self.txtuser.get() == "admin" and self.txtpwd.get() == "admin":
            messagebox.showinfo("Success", "Welcome to Attendance Management System Using Facial Recognition")
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
        app = FaceRecognitionSystem(root)  # Use the class from main.py
        root.mainloop()

    # =======================Reset Password Function=============================
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

    # =====================Forget window=========================================
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


# =====================main program Face detection system====================
class FaceRecognitionSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition System")

        # This part is image labels setting start 
        # first header image  
        img = Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\bg.jpg")
        img = img.resize((1366, 130), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        # set image as label
        f_lb1 = Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=1366, height=130)

        # background image 
        bg1 = Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\bg.jpg")
        bg1 = bg1.resize((1366, 768), Image.LANCZOS)
        self.photobg1 = ImageTk.PhotoImage(bg1)

        # set image as label
        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=130, width=1366, height=768)

        # title section
        title_lb1 = Label(bg_img, text="Attendance Management System Using Facial Recognition", 
                         font=("verdana", 30, "bold"), bg="white", fg="red")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # Create buttons below the section 
        # Student button 1
        std_img_btn = Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\std1.jpg")
        std_img_btn = std_img_btn.resize((180, 180), Image.LANCZOS)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img, command=self.student_pannels, image=self.std_img1, cursor="hand2")
        std_b1.place(x=250, y=100, width=180, height=180)

        std_b1_1 = Button(bg_img, command=self.student_pannels, text="Student Panel", 
                         cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="red")
        std_b1_1.place(x=250, y=280, width=180, height=45)

        # Detect Face button 2
        det_img_btn = Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\det1.jpg")
        det_img_btn = det_img_btn.resize((180, 180), Image.LANCZOS)
        self.det_img1 = ImageTk.PhotoImage(det_img_btn)

        det_b1 = Button(bg_img, command=self.face_rec, image=self.det_img1, cursor="hand2")
        det_b1.place(x=480, y=100, width=180, height=180)

        det_b1_1 = Button(bg_img, command=self.face_rec, text="Face Detector", 
                         cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="red")
        det_b1_1.place(x=480, y=280, width=180, height=45)

        # Attendance System button 3
        att_img_btn = Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\att.jpg")
        att_img_btn = att_img_btn.resize((180, 180), Image.LANCZOS)
        self.att_img1 = ImageTk.PhotoImage(att_img_btn)

        att_b1 = Button(bg_img, command=self.attendance_pannel, image=self.att_img1, cursor="hand2")
        att_b1.place(x=710, y=100, width=180, height=180)

        att_b1_1 = Button(bg_img, command=self.attendance_pannel, text="Attendance", 
                         cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="red")
        att_b1_1.place(x=710, y=280, width=180, height=45)

        # Help Support button 4
        hlp_img_btn = Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\hlp.jpg")
        hlp_img_btn = hlp_img_btn.resize((180, 180), Image.LANCZOS)
        self.hlp_img1 = ImageTk.PhotoImage(hlp_img_btn)

        hlp_b1 = Button(bg_img, command=self.helpSupport, image=self.hlp_img1, cursor="hand2")
        hlp_b1.place(x=940, y=100, width=180, height=180)

        hlp_b1_1 = Button(bg_img, command=self.helpSupport, text="Help Support", 
                         cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="red")
        hlp_b1_1.place(x=940, y=280, width=180, height=45)

        # Train button 5
        tra_img_btn = Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\tra1.jpg")
        tra_img_btn = tra_img_btn.resize((180, 180), Image.LANCZOS)
        self.tra_img1 = ImageTk.PhotoImage(tra_img_btn)

        tra_b1 = Button(bg_img, command=self.train_pannels, image=self.tra_img1, cursor="hand2")
        tra_b1.place(x=250, y=330, width=180, height=180)

        tra_b1_1 = Button(bg_img, command=self.train_pannels, text="Data Train", 
                         cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="red")
        tra_b1_1.place(x=250, y=510, width=180, height=45)

        # Developers button 6
        dev_img_btn = Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\dev.jpg")
        dev_img_btn = dev_img_btn.resize((180, 180), Image.LANCZOS)
        self.dev_img1 = ImageTk.PhotoImage(dev_img_btn)

        dev_b1 = Button(bg_img, command=self.developr, image=self.dev_img1, cursor="hand2")
        dev_b1.place(x=480, y=330, width=180, height=180)

        dev_b1_1 = Button(bg_img, command=self.developr, text="Developers", 
                         cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="red")
        dev_b1_1.place(x=480, y=510, width=180, height=45)

        # Exit button 7
        exi_img_btn = Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\exi.jpg")
        exi_img_btn = exi_img_btn.resize((180, 180), Image.LANCZOS)
        self.exi_img1 = ImageTk.PhotoImage(exi_img_btn)

        exi_b1 = Button(bg_img, command=self.Close, image=self.exi_img1, cursor="hand2")
        exi_b1.place(x=710, y=330, width=180, height=180)

        exi_b1_1 = Button(bg_img, command=self.Close, text="Exit", 
                         cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="red")
        exi_b1_1.place(x=710, y=510, width=180, height=45)

    # ==================Functions Buttons=====================
    def student_pannels(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def train_pannels(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)
    
    def face_rec(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)
    
    def attendance_pannel(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)
    
    def developr(self):
        self.new_window = Toplevel(self.root)
        self.app = Developer(self.new_window)

    def helpSupport(self):
        self.new_window = Toplevel(self.root)
        self.app = Helpsupport(self.new_window)

    def Close(self):
        self.root.destroy()

    def open_img(self):
        os.startfile("dataset")


if __name__ == "__main__":
    root = Tk()
    app = Login(root)
    root.mainloop()