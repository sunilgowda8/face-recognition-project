import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
import cv2
from datetime import datetime

class Face_Recognition:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition Panel")

        # Header image
        try:
            header_img = Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\KK1.jpeg")
            header_img = header_img.resize((1366, 130), Image.LANCZOS)
            self.photoimg = ImageTk.PhotoImage(header_img)
            header_label = Label(self.root, image=self.photoimg)
            header_label.place(x=0, y=0, width=1366, height=130)
        except:
            header_label = Label(self.root, text="Face Recognition System", font=("verdana", 20, "bold"), bg="lightblue", fg="darkblue")
            header_label.place(x=0, y=0, width=1366, height=130)

        # Background image
        try:
            bg_img = Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\ss.jpg")
            bg_img = bg_img.resize((1366, 768), Image.LANCZOS)
            self.photobg = ImageTk.PhotoImage(bg_img)
            bg_label = Label(self.root, image=self.photobg)
            bg_label.place(x=0, y=130, width=1366, height=768)
        except:
            bg_label = Label(self.root, bg="lightgray")
            bg_label.place(x=0, y=130, width=1366, height=768)

        # Title section
        title_label = Label(bg_label, text="Welcome to Face Recognition Panel", font=("verdana", 30, "bold"), bg="white", fg="red")
        title_label.place(x=0, y=0, width=1366, height=45)

        # Training button
        try:
            train_img = Image.open(r"C:\Users\user\OneDrive\Desktop\Python_Test_Projects\college_iimages\banner.png")
            train_img = train_img.resize((200, 200), Image.LANCZOS)
            self.train_photo = ImageTk.PhotoImage(train_img)
            train_button = Button(bg_label, text="Face Detector", command=self.face_recognition, image=self.train_photo, cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="red")
            train_button.place(x=600, y=170, width=180, height=180)
        except:
            train_button = Button(bg_label, text="Face Detector\n(Click to Start)", command=self.face_recognition, cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="red")
            train_button.place(x=600, y=170, width=180, height=180)

        # Status label
        self.status_label = Label(bg_label, text="Ready", font=("verdana", 12), bg="white", fg="green")
        self.status_label.place(x=10, y=700, width=200, height=30)

    def get_db_connection(self):
        """Get database connection"""
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root", 
                password="Sunil@123",
                database="face_recognization"
            )
        except Exception as e:
            print(f"Database connection error: {e}")
            return None

    def mark_attendance(self, student_id, roll_no, name):
        """Mark attendance in CSV file"""
        try:
            with open("attendance.csv", "a+", newline="\n") as f:
                f.write(f"{student_id},{roll_no},{name},{datetime.now().strftime('%H:%M:%S')},{datetime.now().strftime('%d/%m/%Y')},Present\n")
            print(f"Attendance marked for {name}")
        except Exception as e:
            print(f"Attendance error: {e}")

    def face_recognition(self):
        """Main face recognition function"""
        self.status_label.config(text="Starting Camera...", fg="orange")
        self.root.update()

        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                
                try:
                    id, predict = clf.predict(gray_image[y:y+h, x:x+w])
                    confidence = int((100 * (1 - predict / 300)))

                    if confidence > 77:
                        conn = self.get_db_connection()
                        if conn:
                            cursor = conn.cursor()
                            # FIXED: Using correct column names
                            cursor.execute("SELECT Name, Roll FROM student WHERE id=%s", (id,))
                            result = cursor.fetchone()
                            
                            if result:
                                name = result[0]
                                roll_no = result[1]

                                cv2.putText(img, f"ID: {id}", (x, y-80), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 2)
                                cv2.putText(img, f"Name: {name}", (x, y-55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 2)
                                cv2.putText(img, f"Roll: {roll_no}", (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 2)
                                cv2.putText(img, f"Conf: {confidence}%", (x, y+h+25), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 0), 2)

                                self.mark_attendance(id, roll_no, name)
                            
                            cursor.close()
                            conn.close()
                    else:
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                        cv2.putText(img, "Unknown Face", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 0), 3)
                            
                except Exception as e:
                    print(f"Recognition error: {e}")

        def recognize(img, clf, face_cascade):
            draw_boundary(img, face_cascade, 1.1, 10, (235, 25, 235), "Face", clf)
            return img

        # Load classifiers
        try:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read("clf.xml")
            self.status_label.config(text="Camera Active - Press Enter to exit", fg="green")
        except Exception as e:
            self.status_label.config(text="Error loading models", fg="red")
            print(f"Error loading classifiers: {e}")
            return

        # Initialize camera
        video_cap = cv2.VideoCapture(0)
        
        if not video_cap.isOpened():
            self.status_label.config(text="Cannot access camera", fg="red")
            return

        try:
            while True:
                ret, img = video_cap.read()
                if not ret:
                    break
                    
                img = recognize(img, clf, face_cascade)
                cv2.imshow("Face Detector - Press Enter to exit", img)
                
                if cv2.waitKey(1) == 13:  # Enter key
                    break
                    
        except Exception as e:
            print(f"Camera error: {e}")
        finally:
            video_cap.release()
            cv2.destroyAllWindows()
            self.status_label.config(text="Ready", fg="green")


if __name__ == "__main__":
    root = Tk()
    app = Face_Recognition(root)
    root.mainloop()