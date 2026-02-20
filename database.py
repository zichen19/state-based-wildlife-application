#testing connector from Phase 1 Files
#Class imports:
import mysql.connector as mysql
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import customtkinter as ctk

#Class imports:
import deleteT, insertT,updateT, searchT, requests, display_advanced, Statistics

class Sign_In:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign In Page")
        self.root.geometry("400x400")
        self.connection = None
        self.error = False # Keep track if an error occured, used for knowing if login failed because of an error, of if it was an exception
       
        try:
            # Modify these parameters to match your MySQL setup
            self.connection = mysql.connect(
                  host = 'localhost',
                  user = 'root',
                  password = 'dataSQ1lpr0j', 
                  port = '3306',
                  database = 'wildlife_database' #part of the test server
            ) 
        except mysql.Error as err:
            messagebox.showerror("Error", f"Failed to connect: {err}")

        # Username
        self.username_label = ctk.CTkLabel(root, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(root)
        self.username_entry.pack(pady=5)
        self.username_entry.focus_set() # Click the username box for the user

        # Password
        self.password_label = ctk.CTkLabel(root, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(root, show="*")
        self.password_entry.pack(pady=5)

         # Message Label
        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=5)

        # Sign In Button
        self.signin_button = ctk.CTkButton(root, text="Sign In", command=self.sign_in)
        self.signin_button.pack(pady=20)

        self.sign_up_button = ctk.CTkButton(root, text="Sign_up ", command=self.sign_up)
        self.sign_up_button.pack(pady=10)

    def sign_up(self):
       
        new_user_window = ctk.CTkToplevel(self.root)
        new_user_window.focus()
        new_user_app = insertT.ResearcherApp(new_user_window,self.connection)
        #Debug tools:
        self.launch_admin()
        #self.launch_researcher()


    def sign_in(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_role, user_id = self.verify_credentials(username, password)
        # Check if the login info matches

        if user_role:
            self.message_label.configure(text=f"Login successful as {user_role}", fg_color="green")
            if user_role == "Admin":
                self.launch_admin()
                #admin_page = Admin_Page(root, user_id=user_id)
            elif user_role == "Researcher":
                self.launch_researcher()
                #researcher_page = Researcher_Page(root, user_id=user_id)
            

        elif self.error: # Login falied because of an exception
            self.error = False # reset error for the next try

        else: # Login did not fail because of an exception -> login failed bcause of inccorect user/pass
            self.message_label.configure(text="Invalid username or password", fg_color="red")
       
    def verify_credentials(self, username, password):
        #hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            cursor = None
            self.connection = mysql.connect(
                  host = 'localhost',
                  user = 'root',
                  password = 'dataSQ1lpr0j', 
                  port = '3306',
                  database = 'wildlife_database' #part of the test server
            )
            cursor = self.connection.cursor()

            # Check in Admin table
            query_admin = "SELECT AdminID FROM admin WHERE AdminUserName = %s AND AdPassword = %s"
            cursor.execute(query_admin, (username,password)) # <------- HEX PASSWORD or PLAINTEXT PASSWORD
            result = cursor.fetchone()
            
            if result:
                cursor.close()
                return ("Admin", result[0])#return user type and ID
            
            # Check in Researcher table
            query_researcher = "SELECT UserID FROM researcher WHERE RUsername = %s AND password = %s"
            cursor.execute(query_researcher, (username, password)) # <------- HEX PASSWORD or PLAINTEXT PASSWORD
            result = cursor.fetchone()
            if result:
                cursor.close()
                return ("Researcher", result[0])#return user type and ID

            cursor.close()
            return (None, None)
        
        except Exception as error:
            self.error = True
            self.message_label.configure(text=f"Failed to query database: {error}", fg="red")
            if cursor:
                cursor.close()
            return (None,None)

    def launch_admin(self):
        admin_window = ctk.CTkToplevel(self.root)
        admin_window.focus()
        admin_app =Admin_Page(admin_window,self.connection,self.username_entry.get())

    def launch_researcher(self):
        reserarch_window = ctk.CTkToplevel(self.root)
        reserarch_window.focus()
        research_app = Researcher_Page(reserarch_window,self.connection, self.username_entry.get())
        

class Researcher_Page:
    def __init__(self, root, connection,user_id):
        self.root = root
        self.root.title("Researcher Page")
        self.root.geometry(f"{700}x{400}")

        # configure grid layout (4x4)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure((2, 3), weight=0)
        self.root.grid_rowconfigure((0, 1, 2), weight=1)

        self.connection = connection
        self.user_id = user_id

        # creation of a frame
        self.checkbox_frame = ctk.CTkFrame(self.root,width=140, corner_radius=0)
        self.checkbox_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.checkbox_frame.grid_rowconfigure(4, weight=1)
        
        self.options_label = ctk.CTkLabel(self.checkbox_frame,text="Options", font=ctk.CTkFont(size=20, weight="bold"))
        self.options_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        #view profile
        self.view_profile_button = ctk.CTkButton(self.checkbox_frame, text="View Profile", command=self.view_profile)
        self.view_profile_button.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        #Request Change 
        self.request_change_button = ctk.CTkButton(self.checkbox_frame, text="Request Change", command=self.request_change)
        self.request_change_button.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        # #change password button
        self.change_pw_button = ctk.CTkButton(self.checkbox_frame, text="Change Password", command=self.change_password)
        self.change_pw_button.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        #appearnce switcher
        self.appearance_mode_label = ctk.CTkLabel(self.checkbox_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=4, column=0, padx=20, pady=0)
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.checkbox_frame, values=[ "System","Light", "Dark"],command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=10)

        #log out button
        self.logout_button = ctk.CTkButton(self.checkbox_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=6, column=0, padx=20, pady=10, sticky="w")

        ###### Not in Frame
        self.search_button = ctk.CTkLabel(self.root, text="Search")
        self.search_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.search_a_button = ctk.CTkButton(self.root, text="Animal Search", command=self.open_a_search)
        self.search_a_button.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.search_b_button = ctk.CTkButton(self.root, text="Biome Search", command=self.open_b_search)
        self.search_b_button.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        self.search_f_button = ctk.CTkButton(self.root, text="Feature Search", command=self.open_f_search)
        self.search_f_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.search_h_button = ctk.CTkButton(self.root, text="Habitat Search", command=self.open_h_search)
        self.search_h_button.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        self.search_p_button = ctk.CTkButton(self.root, text="Plant Search", command=self.open_p_search)
        self.search_p_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    def view_profile(self):
        profile_window = ctk.CTkToplevel(self.root)
        profile_window.focus()
        admin_search_query = """ SELECT * FROM researcher WHERE RUserName = %s """
        mycursor = self.connection.cursor()
        vals = (self.user_id,) 
        mycursor.execute(admin_search_query, vals)
        animal_vals = mycursor.fetchone()
        mycursor.close()
        display_app = display_advanced.Display_Page(profile_window,animal_vals,"researcher")

    def request_change(self):
        request_change_window =  ctk.CTkToplevel(self.root)
        request_change_window.focus()
        update_app = requests.Requests_Handler(request_change_window, 'r')
        
    def logout(self):
        #close the current wnidow
        self.root.destroy()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_password(self):
        # Open a new window to change the password
        change_pw_window =  ctk.CTkToplevel(self.root)
        change_pw_window.focus()
        update_app = updateT.UPDATE_APP(change_pw_window, self.connection, user_id=self.user_id)
        update_app.setup_for_password_change("Researcher")

    def open_a_search(self):
        a_search_window =  ctk.CTkToplevel(self.root)
        a_search_window.focus()
        update_app = searchT.ANIMAL_SEARCH(a_search_window, self.connection)

    def open_p_search(self):
        a_search_window =  ctk.CTkToplevel(self.root)
        a_search_window.focus()
        update_app = searchT.PLANT_SEARCH(a_search_window, self.connection)

    def open_b_search(self):
        a_search_window =  ctk.CTkToplevel(self.root)
        a_search_window.focus()
        update_app = searchT.BIOME_SEARCH(a_search_window, self.connection)

    def open_h_search(self):
        a_search_window =  ctk.CTkToplevel(self.root)
        a_search_window.focus()
        update_app = searchT.HABITAT_SEARCH(a_search_window, self.connection)

    def open_f_search(self):
        a_search_window =  ctk.CTkToplevel(self.root)
        a_search_window.focus()
        update_app = searchT.FEATURES_SEARCH(a_search_window, self.connection)
        

class Admin_Page:
    def __init__(self, root, connection,user_id):
        self.root = root
        self.root.title("Admin Page")
        self.root.geometry(f"{700}x{400}")

        # configure grid layout (4x4)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure((2, 3), weight=0)
        self.root.grid_rowconfigure((0, 1, 2), weight=1)

        self.user_id = user_id
        self.connection = connection

        self.requests_file = open("requests.txt", "r+")# for admin usage
        number_o_requests = len(self.requests_file .readlines())

        # creation of a frame
        self.checkbox_frame = ctk.CTkFrame(self.root,width=140, corner_radius=0)
        self.checkbox_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.checkbox_frame.grid_rowconfigure(4, weight=1)

        #view_profile button
        self.view_profile_button = ctk.CTkButton(self.checkbox_frame, text="View Profile", command=self.view_profile)
        self.view_profile_button.grid(row=0, column=0, padx=20, pady=10,sticky="w")

        #approve requests
        self.approve_requests_button =  ctk.CTkButton(self.checkbox_frame,text="Approve Requests", command = self.approve_requests)
        self.approve_requests_button.grid(row=1, column=0, padx=20, pady=10,sticky="w")

        #Add new admin Button
        self.newAdmin_button = ctk.CTkButton(self.checkbox_frame,text="Add New Admin", command = self.open_newAdmin)
        self.newAdmin_button.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        #change password button
        self.change_pw_button = ctk.CTkButton(self.checkbox_frame, text="Change Password", command=self.change_password)
        self.change_pw_button.grid(row=3, column=0, padx=20, pady=10,sticky="w")

        #log out button
        self.logout_button = ctk.CTkButton(self.checkbox_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=4, column=0, padx=20, pady=10,sticky="w")

        ############# Options outside of frame   ####################

        #label for showing how many requests need aprroval
        self.options_label = ctk.CTkLabel(self.root,text="Number of Pending Requests: "+str(number_o_requests), font=ctk.CTkFont(size=10, weight="bold"),text_color = ("red"))
        self.options_label.grid(row=0, column=1, padx=20, pady=(20, 10),sticky="ew")
        
        #delete button
        self.delete_button =  ctk.CTkButton(self.root,text="DELETE", command = self.open_delete)
        self.delete_button.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        #insert button
        self.insert_button =  ctk.CTkButton(self.root,text="INSERT", command = self.open_insert)
        self.insert_button.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        #update button
        self.update_button =  ctk.CTkButton(self.root,text="UPDATE", command = self.open_update)
        self.update_button.grid(row=1, column=2, padx=20, pady=10, sticky="w")

        #Stat button
        self.stat_button = ctk.CTkButton(self.root, text="Stats", command=self.open_statistics)
        self.stat_button.grid(row=2, column=2, padx=20, pady=10,sticky="w")


    def approve_requests(self):
        request_change_window = ctk.CTkToplevel(self.root)
        request_change_window.focus()
        update_app = requests.Requests_Handler(request_change_window, 'a')
        
    def view_profile(self):
        profile_window = ctk.CTkToplevel(self.root)
        profile_window.focus()
        admin_search_query = """ SELECT * FROM admin WHERE AdminUserName = %s """
        mycursor = self.connection.cursor()
        vals = (self.user_id,) 
        mycursor.execute(admin_search_query, vals)
        animal_vals = mycursor.fetchone()
        mycursor.close()
        display_app = display_advanced.Display_Page(profile_window,animal_vals,"admin")

    def change_password(self):
        # Open a new window to change the password
        change_pw_window = ctk.CTkToplevel(self.root)
        change_pw_window.focus()
        update_app = updateT.UPDATE_APP(change_pw_window, self.connection, self.user_id)
        update_app.setup_for_password_change("Admin")

    def logout(self):
        #close the current wnidow
        self.root.destroy()
    
    def open_newAdmin(self):
        addAdmin_window = ctk.CTkToplevel(self.root)
        addAdmin_window.focus()
        addAdmin_ap = insertT.AdminApp(addAdmin_window, self.connection)

    def open_delete(self):
        delete_window = ctk.CTkToplevel(self.root)
        delete_window.focus()
        delete_app = deleteT.DELETE_APP(delete_window,self.connection)

    def open_insert(self):
        insert_window = ctk.CTkToplevel(self.root)
        insert_window.focus()
        insert_app = insertT.INSERT_APP(insert_window,self.connection)

    def open_update(self):
        update_window = ctk.CTkToplevel(self.root)
        update_window.focus()
        update_app = updateT.UPDATE_APP(update_window,self.connection)

    def open_animalsearch(self):
        animalsearch_window = ctk.CTkToplevel(self.root)
        animalsearch_window.focus()
        animalsearch_app = searchT.ANIMAL_SEARCH(animalsearch_window,self.connection)

    def open_plantsearch(self):
        animalsearch_window = ctk.CTkToplevel(self.root)
        animalsearch_window.focus()
        animalsearch_app = searchT.ANIMAL_SEARCH(animalsearch_window,self.connection)

    def open_statistics(self):
        stat_window = ctk.CTkToplevel(self.root)
        stat_window.focus()
        stat_app = Statistics.Stats(stat_window, self.connection)


if __name__ == "__main__":
    root = ctk.CTk()
    app = Sign_In(root)
    #app = Researcher_Page(root)
    #app = Admin_Page(root)
    root.mainloop()

# #mycursor.execute("CREATE TABLE biome (BiomeID int NOT NULL AUTO_INCREMENT,  Climate varchar(45) NOT NULL,  TempRange varchar(45) NOT NULL,  PRIMARY KEY (BiomeID),  UNIQUE KEY BiomeID_UNIQUE (BiomeID))")
# #mycursor.execute("CREATE TABLE feature ( FeatureID int NOT NULL AUTO_INCREMENT, Local_Materials varchar(45) NOT NULL, Terrain varchar(45) NOT NULL, Water_Feature varchar(45) NOT NULL, PRIMARY KEY (FeatureID), UNIQUE KEY FeatureID_UNIQUE (FeatureId))")
# #mycursor.execute("CREATE TABLE featureOf ( F_BiomeID INT, F_FeatureID INT, PRIMARY KEY (F_BiomeID, F_FeatureID), FOREIGN KEY (F_BiomeID) REFERENCES biome(BiomeID), FOREIGN KEY (F_FeatureID) REFERENCES feature(FeatureID))")
# #mycursor.execute("CREATE TABLE habitat ( HabitatID INT NOT NULL AUTO_INCREMENT, hname VARCHAR(45) NOT NULL, location VARCHAR(45) NOT NULL, avg_temp VARCHAR(45) NOT NULL, avg_rain VARCHAR(45) NOT NULL, climate VARCHAR(45) NOT NULL, altitude_range VARCHAR(45) NOT NULL, protected_areas VARCHAR(45) NOT NULL, soil_type VARCHAR(45) NOT NULL, h_BiomeID INT, PRIMARY KEY (HabitatID), UNIQUE KEY HabitatID_UNIQUE (HabitatID), FOREIGN KEY (h_BiomeID) REFERENCES biome(BiomeID))")
# #mycursor.execute("CREATE TABLE researcher ( UserId int NOT NULL AUTO_INCREMENT, password varchar(45)NOT NULL, name varchar(45) NOT NULL, Qualifications varchar(45) NOT NULL, R_AdminID INT, PRIMARY KEY (UserId),  UNIQUE KEY UserId_UNIQUE (UserID), FOREIGN KEY (R_AdminID) REFERENCES admin(AdminID))")
# #mycursor.execute("CREATE TABLE plant ( PSpeciesID INT AUTO_INCREMENT PRIMARY KEY, PCommonName VARCHAR(45), PScientificName VARCHAR(45), LifeCycle VARCHAR(45), PlantType VARCHAR(45), FloweringPeriod VARCHAR(45), P_BiomeID INT, P_HabitatID INT, P_ASpeciesID INT, P_UserID INT, P_AdminID int, UNIQUE KEY PSpeciesID_UNIQUE (PSpeciesID), FOREIGN KEY (P_BiomeID) REFERENCES biome(BiomeID), FOREIGN KEY (P_HabitatID) REFERENCES habitat(HabitatID), FOREIGN KEY (P_UserID) REFERENCES researcher(UserID), FOREIGN KEY (P_AdminID) REFERENCES Admin(AdminID))")
# #mycursor.execute("CREATE TABLE animal( ASpeciesID INT PRIMARY KEY AUTO_INCREMENT,  ACommonName VARCHAR(45), ASpeciesName VARCHAR(45), LifeSpan VARCHAR(45), Size VARCHAR(45), AnimalClass VARCHAR(45), T_SpeciesID INT, E_SpeciesID INT, A_BiomeID INT, A_HabitatID INT, P_SpeciesID INT, A_UserID INT, A_AdminID INT, UNIQUE KEY ASpeciesID_UNIQUE (ASpeciesID), FOREIGN KEY (A_BiomeID) REFERENCES biome(BiomeID), FOREIGN KEY (A_HabitatID) REFERENCES habitat(HabitatID), FOREIGN KEY (P_SpeciesID) REFERENCES plant(PSpeciesID), FOREIGN KEY (A_UserID) REFERENCES researcher(UserID), FOREIGN KEY (A_AdminID) REFERENCES admin(AdminID), FOREIGN KEY (T_SpeciesID) REFERENCES animal(ASpeciesID), FOREIGN KEY (E_SpeciesID) REFERENCES animal(ASpeciesID))")