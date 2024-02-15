import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("ContactBook Management")
        self.root.attributes('-fullscreen', True)

        title = Label(self.root, text="ContactBook Management", font=("Comic Sans MS", 20), bd=8, bg='black', fg='white')
        title.pack(side=TOP, fill=X)

        self.firstname = StringVar()
        self.lastname = StringVar()
        self.mobile = StringVar()
        self.addr = StringVar()
        self.pin = StringVar()

        Detail_F = Frame(self.root, bd=4, relief=RIDGE, bg='white')
        Detail_F.place(x=10, y=150, width=390, height=260)

        lbl_name = Label(Detail_F, text="First Name", font=("Comic Sans MS", 12))
        lbl_name.grid(row=1, column=0, pady=10, padx=20, sticky="w")
        txt_name = Entry(Detail_F, font=("Comic Sans MS", 10), bd=3, textvariable=self.firstname)
        txt_name.grid(row=1, column=1, pady=10, sticky="w")

        lbl_mob = Label(Detail_F, text="Last Name", font=("Comic Sans MS", 12))
        lbl_mob.grid(row=2, column=0, pady=10, padx=20, sticky="w")
        txt_mob = Entry(Detail_F, font=("Comic Sans MS", 10), bd=3, textvariable=self.lastname)
        txt_mob.grid(row=2, column=1, pady=10, sticky="w")

        lbl_aa = Label(Detail_F, text="Mobile No.", font=("Comic Sans MS", 12))
        lbl_aa.grid(row=3, column=0, pady=10, padx=20, sticky="w")
        txt_aa = Entry(Detail_F, font=("Comic Sans MS", 10), bd=3, textvariable=self.mobile)
        txt_aa.grid(row=3, column=1, pady=10, sticky="w")

        lbl_add = Label(Detail_F, text="Address", font=("Comic Sans MS", 12))
        lbl_add.grid(row=4, column=0, pady=10, padx=20, sticky="w")
        txt_add = Entry(Detail_F, font=("Comic Sans MS", 10), bd=3, textvariable=self.addr)
        txt_add.grid(row=4, column=1, pady=10, sticky="w")

        lbl_pin = Label(Detail_F, text="PinCode", font=("Comic Sans MS", 12))
        lbl_pin.grid(row=5, column=0, pady=10, padx=20, sticky="w")
        txt_pin = Entry(Detail_F, font=("Comic Sans MS", 10), bd=3, textvariable=self.pin)
        txt_pin.grid(row=5, column=1, pady=10, sticky="w")

        recordFrame = Frame(self.root, bd=5, relief=RIDGE)
        recordFrame.place(x=450, y=160, width=550, height=260)
        yscroll = Scrollbar(recordFrame, orient=VERTICAL)

        self.contact_table = ttk.Treeview(recordFrame, columns=("firstname", "lastname", "mobile", "address", "pin"), yscrollcommand=yscroll.set)
        yscroll.pack(side=RIGHT, fill=Y)
        yscroll.config(command=self.contact_table.yview)

        self.contact_table.heading("firstname", text="First Name")
        self.contact_table.heading("lastname", text="Last Name")
        self.contact_table.heading("mobile", text="Mobile No.")
        self.contact_table.heading("address", text="Address")
        self.contact_table.heading("pin", text="PinCode")
        self.contact_table['show'] = 'headings'

        self.contact_table.column("firstname", width=100)
        self.contact_table.column("lastname", width=100)
        self.contact_table.column("mobile", width=100)
        self.contact_table.column("address", width=100)
        self.contact_table.column("pin", width=110)

        self.contact_table.pack(fill=BOTH, expand=1)
        self.fetch_data()
        self.contact_table.bind("<ButtonRelease-1>", self.get_cursor)

        btnFrame = Frame(self.root, bd=5, relief=RIDGE)
        btnFrame.place(x=250, y=450, width=600, height=60)

        btn1 = Button(btnFrame, text='Add record', font='arial 12 bold', bg='black', fg='white', width=9, command=self.addrecord)
        btn1.grid(row=0, column=0, padx=10, pady=10)

        btn2 = Button(btnFrame, text='Update', font='arial 12 bold', bg='black', fg='white', width=9, command=self.update)
        btn2.grid(row=0, column=1, padx=8, pady=10)

        btn3 = Button(btnFrame, text='Delete', font='arial 12 bold', bg='black', fg='white', width=9, command=self.delete)
        btn3.grid(row=0, column=2, padx=8, pady=10)

        btn4 = Button(btnFrame, text='Reset', font='arial 12 bold', bg='black', fg='white', width=9, command=self.reset)
        btn4.grid(row=0, column=3, padx=8, pady=10)
        
        btn5 = Button(btnFrame, text='Exit', font='arial 12 bold', bg='black', fg='white', width=9, command=self.exit_program)
        btn5.grid(row=0, column=4, padx=8, pady=10)

        self.search_frame = Frame(self.root, bd=4, relief=RIDGE)
        self.search_frame.place(x=450, y=90, width=390, height=50)

        self.search_label = Label(self.search_frame, text="Search:", font=("Comic Sans MS", 12))
        self.search_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.search_entry = Entry(self.search_frame, font=("Comic Sans MS", 10), bd=3)
        self.search_entry.grid(row=0, column=1, pady=10, sticky="w")

        self.search_button = Button(self.search_frame, text="Search", font='arial 12 bold', bg='black', fg='white', width=9, command=self.search_record)
        self.search_button.grid(row=0, column=2, padx=8, pady=10)

        

    def addrecord(self):
        if self.firstname.get() == '' or self.lastname.get() == '' or self.mobile.get() == '' or self.addr.get() == '' or self.pin.get() == '':
            messagebox.showerror('Error', 'Please enter details')
        else:
            con = sqlite3.connect('contactbook.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM contact")
            rows = cur.fetchall()
            for row in rows:
                if row[2] == self.mobile.get():
                    messagebox.showerror('Error', 'Duplicates not allowed')
                    return
            cur.execute("INSERT INTO contact (firstname, lastname, mobile, addr, pin) VALUES (?, ?, ?, ?, ?)",
                        (self.firstname.get(), self.lastname.get(), self.mobile.get(), self.addr.get(), self.pin.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Record added successfully.')
            self.fetch_data()
            self.reset()

    def fetch_data(self):
        con = sqlite3.connect('contactbook.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM contact")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.contact_table.delete(*self.contact_table.get_children())
            for row in rows:
                self.contact_table.insert('', END, values=row)
            con.commit()
            con.close()

    def update(self):
        if self.mobile.get() == '':
            messagebox.showerror('Error', 'Please select a record to update.')
        else:
            con = sqlite3.connect('contactbook.db')
            cur = con.cursor()
            cur.execute("UPDATE contact SET firstname=?, lastname=?, addr=?, pin=? WHERE mobile=?",
                        (self.firstname.get(), self.lastname.get(), self.addr.get(), self.pin.get(), self.mobile.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Record updated successfully.')
            self.fetch_data()
            self.reset()

    def delete(self):
        if self.mobile.get() == '':
            messagebox.showerror('Error', 'Please select a record to delete.')
        else:
            con = sqlite3.connect('contactbook.db')
            cur = con.cursor()
            cur.execute("DELETE FROM contact WHERE mobile=?", (self.mobile.get(),))
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Record deleted successfully.')
            self.fetch_data()
            self.reset()

    def reset(self):
        self.firstname.set('')
        self.lastname.set('')
        self.mobile.set('')
        self.addr.set('')
        self.pin.set('')

    def get_cursor(self, ev):
        cursor_row = self.contact_table.focus()
        content = self.contact_table.item(cursor_row)
        row = content['values']
        self.firstname.set(row[0])
        self.lastname.set(row[1])
        self.mobile.set(row[2])
        self.addr.set(row[3])
        self.pin.set(row[4])

    def search_record(self):
        con = sqlite3.connect('contactbook.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM contact WHERE firstname LIKE ? OR lastname LIKE ?",
                    ('%' + self.search_entry.get() + '%', '%' + self.search_entry.get() + '%'))
        rows = cur.fetchall()
        if len(rows) != 0:
            self.contact_table.delete(*self.contact_table.get_children())
            for row in rows:
                self.contact_table.insert('', END, values=row)
        else:
            messagebox.showinfo('Info', 'No records found.')
        con.commit()
        con.close()

    def exit_program(self):
        self.root.destroy()

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book Management System")
        self.root.geometry("300x150")
        self.username = StringVar()
        self.password = StringVar()

        Label(self.root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        Entry(self.root, textvariable=self.username).grid(row=0, column=1, padx=10, pady=10)
        Label(self.root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        Entry(self.root, textvariable=self.password, show="*").grid(row=1, column=1, padx=10, pady=10)
        Button(self.root, text="Login", command=self.login).grid(row=2, column=1, padx=10, pady=10)

    def login(self):
        if self.username.get() == "root" and self.password.get() == "root":
            self.root.destroy()
            nroot = Tk()
            ContactManager(nroot)
        else:
            messagebox.showerror("Error", "Invalid username or password")

con = sqlite3.connect('contactbook.db')
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS contact (firstname TEXT, lastname TEXT, mobile TEXT PRIMARY KEY, addr TEXT, pin TEXT)')
cur.close()
con.close()

root = Tk()
obj = Login(root)
root.mainloop()
