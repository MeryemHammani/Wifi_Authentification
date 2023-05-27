import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from AuthPages.ENSAF import auth
from AuthPages.dbConnection import connectionDB
from AuthPages.guest import auth_guest
from AuthPages.tools import email_send, generate_code

# allow the user who belong to usmba to connect by redirecting him to ENSAF page
class page(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("inscription")
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
        heading.place(x=130, y=5)

        # the email
        global email
        email = tk.Entry(frame, width=25, fg="black", border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        email.place(x=30, y=150)
        email.insert(0, "Academic Email")

        def on_enter(e):
            email.delete(0, 'end')

        email.bind('<FocusIn>', on_enter)
        tk.Frame(frame, width=295, height=2, bg="black").place(x=25, y=177)
        # button
        tk.Button(frame, width=39, pady=7, text="Connect", bg="#57A1F8", fg="white", border=0,
                  command=self.SingnIn).place(
            x=35, y=204)
        #
        label = tk.Label(frame, text="Not member of USMBA university ?", fg="black", bg="white",
                         font=('Microsoft YaHei UI Light', 9))
        label.place(x=45, y=270)
        tk.Button(frame, width=6, text="Guest", border=0, bg="white", fg="#57A1F8", cursor='hand2',
                  command=self.redirect_guest).place(x=245, y=270)

    def SingnIn(self):
        mail = email.get()
        if "@usmba.ac.ma" in mail:
            code = generate_code(8)
            code = connectionDB(mail, code)
            email_send(mail, code)
            self.master.destroy()
            root = tk.Tk()
            form = auth(master=root, email=mail, code=code)
            form.mainloop()
        else:
            messagebox.showerror("Invalid", "Enter an academic email")

    def redirect_guest(self):
        self.master.destroy()
        root = tk.Tk()
        form = auth_guest(master=root)
        form.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    form = page(master=root)
    form.mainloop()
