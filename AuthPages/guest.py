import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from AuthPages.ENSAF import auth
from AuthPages.dbConnection import query_select

from AuthPages.tools import generate_code, email_guest


# this page created for the guest not from usmba he enters the academic email for someone from ENSA and his email
# send an authorise email that include a button to redirect to website
class auth_guest(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("WiFi")
        master.geometry("925x500+200+100")
        master.config(bg="#fff")
        master.resizable(False, False)
        self.create_widgets()
        self.pack()

        # Load and display the image
        image = Image.open("login.png")
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.master, image=photo, bg='white')
        label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
        label.place(x=50, y=50)

    def create_widgets(self):
        # the form that includes information
        frame = tk.Frame(self.master, width=350, height=350, bg="white")
        frame.place(x=480, y=70)
        heading = tk.Label(frame, text="WiFi", fg='#57A1F8', bg='white',
                           font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)

        # the email
        global email
        email = tk.Entry(frame, width=25, fg="black", border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        email.place(x=30, y=90)
        email.insert(0, "Academic Email")

        def on_enter(e):
            email.delete(0, 'end')

        def on_leave(e):
            m = email.get()
            if m == '':
                email.insert(0, "Academic Email")

        email.bind('<FocusIn>', on_enter)
        email.bind('<FocusOut>', on_leave)
        tk.Frame(frame, width=295, height=2, bg="black").place(x=25, y=117)
        global guestEmail
        guestEmail = tk.Entry(frame, width=25, fg="black", border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        guestEmail.place(x=30, y=150)
        guestEmail.insert(0, "Your Email")

        def on_enter(e):
            guestEmail.delete(0, 'end')

        def on_leave(e):
            m = guestEmail.get()
            if m == '':
                guestEmail.insert(0, "your email")

        guestEmail.bind('<FocusIn>', on_enter)
        guestEmail.bind('<FocusOut>', on_leave)

        tk.Frame(frame, width=295, height=2, bg="black").place(x=25, y=177)
        # button
        tk.Button(frame, width=39, pady=7, text="Connect", bg="#57A1F8", fg="white", border=0,
                  command=self.SingnIn).place(x=35, y=204)

    def SingnIn(self):
        mail = email.get()

        if "@usmba.ac.ma" in mail:
            status = query_select(mail, 'no')
            if status is not None and status == 'no':
                guest_email = guestEmail.get()
                code = generate_code(8)
                email_guest(mail, guest_email, code)
                self.master.destroy()
                root = tk.Tk()
                form = auth(master=root, email=guest_email, code=code)
                form.mainloop()
            else:
                messagebox.showerror("Invalid", "Invalid academic Email")
        else:
            messagebox.showerror("Invalid", "Enter an academic email")


if __name__ == "__main__":
    root = tk.Tk()
    form = auth_guest(master=root)
    form.mainloop()
