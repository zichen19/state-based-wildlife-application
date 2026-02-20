from datetime import datetime
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk) 
import json, os

# Tkinter window
class Stats:
    def __init__(self, root, connection):
        self.root = root
        self.root.title("Signup Analysis")
        self.root.geometry(f"{900}x{350}")
        self.connection = connection

        # Frame for General Info
         # creation of a frame
        self.frame = ctk.CTkFrame(self.root,width=140, corner_radius=0)
        self.frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.frame.grid_rowconfigure(4, weight=1)

        self.total_admins_label = ctk.CTkLabel(self.frame,text = "Total number of admins: " + str(self.count_admin_signups()))
        self.total_admins_label.grid(row=0, column=1, padx=20, pady=(20, 10),sticky="ew")
        self.total_researchers_label = ctk.CTkLabel(self.frame,text = "Total number of users: " + str(self.count_researcher_signups()))
        self.total_researchers_label.grid(row=1, column=1, padx=20, pady=(20, 10),sticky="ew")


        # Col 1  Row 0 for bar chart
        self.plot_bar()
        self.grab_search_data()
        #self.plot_button = ctk.CTkButton(self.root,text="Plot" ,command= self.plot ) 
        #self.plot_button.grid(row=0, column=2, padx=20, pady=(20, 10),sticky="ew")


        # Col 1  Row 2 for Line/bar chart?
        self.plot_chart()
        # bar chart showing who is winning, animals or plants
        # This months winner is x
        # another chart to show how many users accounts are being made per month

    def plot_bar(self): 
  
        # the figure that will contain the plot 
        data = self.grab_search_data()
        names = list(data.keys())
        values = list(data.values())

        fig, axs = plt.subplots(figsize=(5, 3), sharey=True)
        axs.bar(names, values)
        fig.suptitle('Amount of Searches')
    
        # creating the Tkinter canvas 
        # containing the Matplotlib figure 
        canvas = FigureCanvasTkAgg(fig, master = self.root)   
        canvas.draw() 
        # placing the canvas on the Tkinter window 
        canvas.get_tk_widget().place(x = 500, y=20) 


    def plot_chart(self):
        self.grab_sign_up_data()    
        # the figure that will contain the plot 
        data = self.grab_sign_up_data() 
        names = list(data.keys())
        values = list(data.values())

        fig, axs = plt.subplots(figsize=(5, 3), sharey=True)
        axs.plot(names, values) # for line chart
        fig.suptitle('Number of Sign ups per month')
    
        # creating the Tkinter canvas 
        # containing the Matplotlib figure 
        canvas = FigureCanvasTkAgg(fig, master = self.root)   
        canvas.draw() 
        # placing the canvas on the Tkinter window 
        canvas.get_tk_widget().place(x = 1100, y=20) 

    def grab_search_data(self):
        
        file_path = 'searchdata.json'

        # Check if the file exists, if not create it with an empty dictionary
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump({}, file)

        # Read the existing data
        with open(file_path, 'r') as file:
            data = json.load(file)
            #print(dict(tuple(data.items())))

        return dict(tuple(data.items()))

    def grab_sign_up_data(self):
        thisdict = {"Jan": 0, "Feb": 0,"Mar": 0,"Apr": 0,"May": 0,"June": 0,"July": 0,"Aug": 0,"Sept": 0,"Oct": 0,"Nov": 0,"Dec": 0}
        query = "SELECT * FROM researcher"
        cursor = self.connection.cursor()
        cursor.execute(query)
        entries = cursor.fetchall()
        cursor.close()
        for entry in entries:
            for key in thisdict.keys():
                if key == entry[5]:
                    thisdict[key] +=1

        return thisdict

    # Function to count total number of sign-ups in 'admin' table
    def count_admin_signups(self):
        query = "SELECT COUNT(*) FROM admin"
        cursor = self.connection.cursor()
        cursor.execute(query)
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    # Function to count total number of sign-ups in 'researcher' table
    def count_researcher_signups(self):
        query = "SELECT COUNT(*) FROM researcher"
        cursor = self.connection.cursor()
        cursor.execute(query)
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    # Function to count daily sign-ups in 'admin' table
    def count_daily_admin_signups(self):
        today = datetime.today().strftime('%Y-%m-%d')
        query = "SELECT COUNT(*) FROM admin WHERE SignupDate = %s"
        cursor = self.connection.cursor()
        cursor.execute(query, (today,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    # Function to count daily sign-ups in 'researcher' table
    def count_daily_researcher_signups(self):
        today = datetime.today().strftime('%Y-%m-%d')
        query = "SELECT COUNT(*) FROM researcher WHERE SignupDate = %s"
        cursor = self.connection.cursor()
        cursor.execute(query, (today,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count