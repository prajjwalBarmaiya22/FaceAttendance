from tkinter import *
from PIL import Image, ImageTk
import cv2
import face_recognition
import pandas as pd

from attendance import attendence, create_student_csv, update_attendance_csv

# Constants
CLICKED_FACE_PATH = 'path/to/saved/faces'

cap = None
camera_update_flag = True


def encode_face(image_path):
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if encodings:
        return encodings[0]
    return None


def check_matching_face(known_encodings, face_encoding_to_check):
    matches = face_recognition.compare_faces(known_encodings, face_encoding_to_check)
    return any(matches)


def clear_widgets(widget):
    for child in widget.winfo_children():
        child.destroy()


def back_to_main_page(window):
    window.destroy()
    front_win()


def front_win():
    # Implement function to create the main window
    main_window = Tk()
    main_window.title("Student Login")

    Label(main_window, text="Scholar Number:").pack()
    scholar_number_entry = Entry(main_window)
    scholar_number_entry.pack()

    Label(main_window, text="Student Name:").pack()
    student_name_entry = Entry(main_window)
    student_name_entry.pack()

    login_button = Button(main_window, text="Login",
                          command=lambda: student_login(main_window, scholar_number_entry.get(), student_name_entry.get()))
    login_button.pack()

    main_window.mainloop()


def match(scholar_number, name):
    df = pd.read_csv('data.csv')
    x = df['Scholar No'].tolist()
    y = df['Name of Student'].tolist()
    for a, b in zip(x, y):
        if a == scholar_number and b == name:
            return True
    return False


def save_photo(frame, scholar_number, log1):
    global cap
    face_recognition.load_known_student_face_encodings()
    filename = f'{CLICKED_FACE_PATH}/{scholar_number}.png'
    cv2.imwrite(filename, frame)
    if cap is not None:
        cap.release()
    clear_widgets(log1)
    x = log1
    A = '{} : Information'.format(scholar_number)
    x.title(A)
    face_encoding = encode_face(filename)
    if face_encoding is not None:
        known_encodings = []  # Load your known encodings
        if check_matching_face(known_encodings, face_encoding):
            period = attendence()
            L = Label(x, text=f"Scholar Number: {scholar_number}\nPeriod: {period}", fg='red')
            L.pack()
            subject_list = ['Data Science', 'AI', 'CN', 'Statistical Modeling', 'Compiler Design', 'OS', 'CN LAB', 'OS LAB',
                            'COMPILER LAB']
            if period in subject_list:
                L1 = Label(x, text='{} Attendance marked '.format(period), fg='green')
                L1.pack()
                create_student_csv(scholar_number)
                update_attendance_csv(scholar_number, period)
                L2 = Label(x)
                L2.pack()
                btn = Button(x, text='Go to login Page', command=lambda: front_win())
                btn.pack()
            else:
                btn = Button(x, text='Go to login Page', command=lambda: back_to_main_page(x))
                btn.pack()
        else:
            L = Label(x, text='{} not found'.format(scholar_number), fg='red')
            L.pack()


def student_login(main_window, scholar_number, student_name):
    global cap, camera_label, camera_update_flag
    if match(scholar_number, student_name):
        clear_widgets(main_window)
        log1 = main_window
        log1.title('Student Info')
        camera_frame = Frame(log1, width=100, height=200)
        camera_frame.pack()

        def update_camera():
            global cap, camera_update_flag
            if cap is not None and camera_update_flag:
                ret, frame = cap.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    photo = ImageTk.PhotoImage(Image.fromarray(frame))
                    camera_label.config(image=photo)
                    camera_label.image = photo
                    camera_label.after(10, update_camera)

        camera_label = Label(camera_frame, height=400, width=300)
        camera_label.pack()
        cap = cv2.VideoCapture(0)
        update_camera()
        student_info = "Name: {}\nScholar Number: {}".format(student_name, scholar_number)
        L = Label(log1, text=student_info)
        L.pack()
        captured_frame = Frame(log1, width=400, height=200)
        captured_frame.pack()

        def capture_and_save(scholar_number, log1):
            ret, frame = cap.read()
            if ret:
                save_photo(frame, scholar_number, log1)

        save_button = Button(captured_frame, text="Save Photo", state=NORMAL,
                             command=lambda: capture_and_save(scholar_number, log1))
        save_button.pack()
        log1.mainloop()
    else:
        l = Label(main_window, text='Student Not Found', fg='red', font=("Helvetica", 15))
        l.pack()


if __name__ == "__main__":
    front_win()
