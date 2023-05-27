import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

from AuthPages.UserLifeConnection import user_connected
from AuthPages.dbConnection import query_select, query_select_code


# use this page to connect to Wi-Fi after the first connection
class auth(tk.Frame):
    def __init__(self, master=None, email = None, code = None):
        super().__init__(master)
        self.email = email
        self.code = code
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
        heading.place(x=130, y=5)

        # the email
        global email
        Email = tk.Entry(frame, width=25, fg="black", border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        Email.place(x=30, y=90)
        Email.insert(0, self.email)
        Email.config(state="disabled")

        tk.Frame(frame, width=295, height=2, bg="black").place(x=25, y=117)
        global code
        code = tk.Entry(frame, width=25, fg="black", border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        code.place(x=30, y=150)
        code.insert(0, "password")

        def on_enter(e):
            code.delete(0, 'end')
            code.config(show='*')

        # def on_leave(e):
        #     m = code.get()
        #     if m == '':
        #         code.insert(0, "password")

        code.bind('<FocusIn>', on_enter)
        # code.bind('<FocusOut>', on_leave)

        tk.Frame(frame, width=295, height=2, bg="black").place(x=25, y=177)
        # button
        tk.Button(frame, width=39, pady=7, text="Connect", bg="#57A1F8", fg="white", border=0,
                  command=self.SingnIn).place(
            x=35, y=204)
        #

    def SingnIn(self):
        guest_code = code.get()
        if guest_code == self.code:
            status = query_select(self.email, 'yes')
            if status is not None and status == 'yes':
                self.master.destroy()
                root = tk.Tk()
                form = user_connected(master=root, email=self.email)
                form.mainloop()
            else:
                messagebox.showinfo('info', 'connected successfully')
        else:
            messagebox.showerror('error', 'incorrect password')


if __name__ == "__main__":
    root = tk.Tk()
    form = auth(master=root)
    form.mainloop()
