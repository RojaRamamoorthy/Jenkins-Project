from tkinter import *
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
import os
import sys
py = sys.executable

#creating window
class issue(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(r'libico.ico')
        self.title('Library Admisintration')
        self.maxsize(500, 500)
        self.minsize(500, 500)
        c = StringVar()
        d = StringVar()

#verifying input
        def isb():
            if len(c.get()) == 0 or len(d.get()) == 0:
                messagebox.showinfo("Error","Please Enter The Id's")
            else:
                try:
                    self.conn = sqlite3.connect('library_administration.db')
                    self.mycursor = self.conn.cursor()
                    self.mycursor.execute("Select Availiability from books where Book_Id = ?",[c.get()])
                    temp = self.mycursor.fetchone()
                    try:
                        if str(temp[0]) == '0':
                            messagebox.showinfo("Oop's","Book Already Issued")
                        else:
                            self.mycursor.execute("Select Fine from students where Student_Id = ?", [d.get()])
                            fine = list(self.mycursor.fetchone())
                            self.mycursor.execute("Select Books_Issued from students where Student_Id = ?", [d.get()])
                            issue = list(self.mycursor.fetchone())
                            if issue[0] < 3:
                                if fine[0] > 100:
                                    messagebox.showerror('Oops', 'Cannot Issue.Please Pay the Fine')
                                elif fine[0] == 0:
                                    print("done")
                                    self.mycursor.execute("INSERT INTO issue VALUES (?,?,date('now'),date('now','+15 days'))",[c.get(), d.get()])
                                    self.mycursor.execute("UPDATE books set Availiability=0 where Book_Id = ?",[c.get()])
                                    issue[0] = issue[0] + 1
                                    print("done2")
                                    self.mycursor.execute("Update students set Books_Issued = ? where Student_Id = ?",[issue[0], d.get()])
                                    print("done3")
                                    self.conn.commit()
                                    self.conn.close()
                                    messagebox.showinfo('Save', 'Successfully Issued')
                                    conf = messagebox.askyesno("Confirm", "Do you want to issue another book?")
                                    if conf:
                                        self.destroy()
                                        os.system('%s %s' % (py, 'issueTable.py'))
                                    else:
                                        self.destroy()
                                elif fine[0] > 0:
                                    Confirm = messagebox.askyesno('Confirm','Are you sure you want to issue.There is a fine')
                                    if Confirm:
                                        self.mycursor.execute("INSERT INTO issue VALUES (?,?,date('now'),date('now','+15 days'))",[c.get(), d.get()])
                                        self.mycursor.execute("UPDATE books set Availiability=0 where Book_Id = ?",[c.get()])
                                        issue[0] = issue[0] + 1
                                        self.mycursor.execute("Update students set Books_Issued = ? where Student_Id = ?",[issue[0], d.get()])
                                        self.conn.commit()
                                        self.conn.close()
                                        messagebox.showinfo('Save', 'Successfully Issued')
                                        conf = messagebox.askyesno("Confirm", "Do you want to issue another book?")
                                        if conf:
                                            self.destroy()
                                            os.system('%s %s' % (py, 'issueTable.py'))
                                        else:
                                            self.destroy()
                                    else:
                                        messagebox.showinfo('Oops', 'Not Issued')
                                elif fine[0] > 100:
                                    messagebox.showerror('Oops', 'Cannot Issue.Please Pay the Fine')
                            else:
                                messagebox.showerror("Can't Issue", "Maximum number of books aleady issued")
                    except TypeError:
                        messagebox.showinfo("Oop's", "Either BookID or StudentId Not Available")
                except Error:
                    messagebox.showerror("Error","Something Goes Wrong")
                    
#label and input box
        Label(self, text='Book Issuing', font=('Georgia', 35)).place(x=100, y=40)
        Label(self, text='Book ID  :', font=('Georgia', 15), fg='red').place(x=60, y=153)
        Entry(self, textvariable=c, width=40).place(x=190, y=160)
        Label(self, text='Student ID  :', font=('Georgia', 15), fg='black').place(x=60, y=193)
        Entry(self, textvariable=d, width=40).place(x=190, y=200)
        Button(self, text="ISSUE", width=30, command=isb).place(x=150, y=290)
issue().mainloop()