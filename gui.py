from tkinter import *
from PIL import Image, ImageTk
from student_login import student_login
from utils import clear_widgets
from constants import MANIT_LOGO_PATH

def front_win():
    main_window = Tk()
    main_window.title('MANIT Bhopal Online Attendance')
    main_window.minsize(600, 600)
    main_window.maxsize(600, 600)

    l1 = Label(main_window, text='ONLINE ATTENDANCE', font=("Helvetica", 20))
    l1.pack()

    image = Image.open(MANIT_LOGO_PATH)
    image = image.resize((150, 150))
    photo = ImageTk.PhotoImage(image)
    l2 = Label(main_window, image=photo)
    l2.photo = photo  # Keep a reference to the photo to avoid garbage collection
    l2.pack()

    scholar_number = StringVar()
    student_name = StringVar()

    l1 = Label(main_window, text='Scholar Number', fg='blue', font=("Helvetica", 15), anchor="center")
    l1.pack()
    scholar = Entry(main_window, textvariable=scholar_number, font=("Helvetica", 15))
    scholar.pack()

    l2 = Label(main_window, text='Student Name (in capital)', fg='blue', font=("Helvetica", 15), anchor="center")
    l2.pack()
    dob = Entry(main_window, textvariable=student_name, font=("Helvetica", 15))
    dob.pack()

    btn = Button(main_window, text='Log in', bg='blue', fg='white',
                 command=lambda: student_login(main_window, scholar_number.get(), student_name.get()))
    btn.pack()

    main_window.mainloop()