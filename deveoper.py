from tkinter import*
from tkinter import ttk
from train import Train
from PIL import Image,ImageTk

from train import Train
from face_recognition import Face_Recognition
from attendance import Attendance
import os

class Developer:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face_Recogonition_System")

# This part is image labels setting start 
        # first header image  
        img=Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\OIP.webp")
        img=img.resize((1366,130),Image.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)

        # set image as lable
        f_lb1 = Label(self.root,image=self.photoimg)
        f_lb1.place(x=0,y=0,width=1366,height=130)

        # backgorund image 
        bg1=Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\bg1.jpg")
        bg1=bg1.resize((1366,768),Image.LANCZOS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=130,width=1366,height=768)


        #title section
        title_lb1 = Label(bg_img,text="Developers Pannel",font=("verdana",30,"bold"),bg="white",fg="red")
        title_lb1.place(x=0,y=0,width=1366,height=45)

       
        

         # Attendance System  button 3
        att_img_btn=Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\SUNIL.jpeg")
        att_img_btn=att_img_btn.resize((350,350),Image.LANCZOS)
        self.att_img1=ImageTk.PhotoImage(att_img_btn)

        att_b1 = Button(bg_img,image=self.att_img1,cursor="hand2",)
        att_b1.place(x=610,y=200,width=280,height=300)

        att_b1_1 = Button(bg_img,text="SUNIL A M \n 1JS24CI408\n CSE(AIML)",cursor="hand2",font=("tahoma",13,"bold"),bg="white",fg="red")
        att_b1_1.place(x=610,y=480,width=280,height=80)
        
       

        

       




if __name__ == "__main__":
    root=Tk()
    obj=Developer(root)
    root.mainloop()