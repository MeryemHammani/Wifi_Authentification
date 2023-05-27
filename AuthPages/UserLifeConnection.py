import time
import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import datetime, timedelta
from PIL import Image, ImageTk

from AuthPages.dbConnection import query_select_time, delete_user_ended_time

# to delete guest after a day of his connection
class user_connected(tk.Frame):
    def __init__(self, master=None, email=None):
        super().__init__(master)
        self.master = master
        self.email = email
        master.title("inscription")
        master.geometry("925x500+200+100")
        master.config(bg="#fff")
        master.resizable(False, False)

        # Load and display the image
        image = Image.open("login.png")
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.master, image=photo, bg='white')
        label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
        label.place(x=50, y=80)

        # the form that includes information
        frame = tk.Frame(self.master, width=350, height=350, bg="white")
        frame.place(x=480, y=70)
        heading = tk.Label(frame, text="WiFi", fg='#57A1F8', bg='white',
                           font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=130, y=5)
        # progress bar
        progress = ttk.Progressbar(self.master, orient="horizontal", length=200, mode="determinate")
        # pack the progress bar widget
        progress.place(x=550, y=200)

        global timeLabel
        timeLabel = tk.Entry(frame, width=14, fg="white", border=0, bg="#33C4FF", font=('Helvetica', 14), bd=3, relief="groove")
        timeLabel.place(x=95, y=190)

        wait_and_delete_user(self.email, progress, self.master)


def wait_and_delete_user(email, progress, root):
    connect_time = query_select_time(email)
    print(type(connect_time))
    print(connect_time)
    one_day_from_now = connect_time + timedelta(days=1)
    print(one_day_from_now)
    if connect_time is not None:
        while True:
            print(datetime.now())
            if datetime.now() >= one_day_from_now:
                progress['value'] = 100
                delete_user_ended_time(email)
                messagebox.showerror('error', 'You are no longer connected')
                break
            else:
                remaining_time = one_day_from_now - datetime.now()
                print('remaining time=', remaining_time.total_seconds())
                percent = int((1 - remaining_time.total_seconds() / 86400) * 100)
                progres = "[" + "#" * int(percent / 10) + " " * (10 - int(percent / 10)) + "]"
                print(f"{percent}% {progres} {one_day_from_now:.0f}s")
                timeLabel.delete(0, 'end')
                timeLabel.insert(0, remaining_time)
                progress['value'] = percent
                root.update()
                time.sleep(1)


if __name__ == "__main__":
    root = tk.Tk()
    form = user_connected(master=root, email='meryem.hammani@usmba.ac.ma')
    form.mainloop()
