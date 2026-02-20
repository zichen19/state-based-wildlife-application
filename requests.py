request_types = ["insert","delete","update"]
import tkinter as tk
from tkinter import *
import customtkinter as ctk
class Requests_Handler:
    def __init__(self, root, type):
        self.root = root
        self.root.title("Page")
        self.type = type

        with open("requests.txt")as file:
            self.lines = file.readlines()
        print(self.lines)

        if type == 'r':
            self.root.geometry(f"{250}x{350}")
            print("Researcher")
            self.type_var= StringVar(self.root)
            request_type_dropdown  = ctk.CTkOptionMenu( self.root , variable=self.type_var , values=request_types) 
            request_type_dropdown.grid(row=0, column=0, padx=20, pady=(20, 10))
            self.entry_var = StringVar(self.root)
            entry_box = ctk.CTkEntry(self.root,textvariable=self.entry_var, width=200,height=70)
            entry_box.grid(row=1, column=0, padx=20, pady=(20, 10))
            self.submit = ctk.CTkButton(root, text="Submit", command=self.submit_request)
            self.submit.grid(row=2, column=0, padx=20, pady=(20, 10))
            

        else:
            self.root.geometry(f"{400}x{350}")
            self.display = ctk.CTkTextbox(root,height = 70, width = 300)
            self.display.insert(tk.END, self.lines)
            self.display.grid(row=0, column=1, padx=20, pady=(20, 10))
            
            print("Admin")
            self.entry_var = StringVar(self.root)
            entry = ctk.CTkEntry(self.root,textvariable=self.entry_var)
            entry.grid(row=1, column=1, padx=20, pady=(20, 10))
            self.approve = ctk.CTkButton(root, text="Approve", command=self.approve_requests)
            self.approve.grid(row=2, column=1, padx=20, pady=(20, 10))

            self.deny = ctk.CTkButton(root, text="Deny", command=self.deny_requests)
            self.deny.grid(row=3, column=1, padx=20, pady=(20, 10))


    def submit_request(self):
        f = open("requests.txt", "a")
        f.write(self.type_var.get() +" "+self.entry_var.get()+"\n")
        f.close()

    def update_file(self):
        with open("requests.txt","w") as f:
            for line in self.lines:
                f.write(line)
        self.display.delete("1.0", END)
        self.display.insert(tk.END, self.lines)
        
    def deny_requests(self):
        del self.lines[int(self.entry_var.get()) -1]
        self.update_file()
        
    def approve_requests(self):
        del self.lines[int(self.entry_var.get()) -1]
        self.update_file()