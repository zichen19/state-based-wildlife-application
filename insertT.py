#testing connector from Phase 1 Files
import mysql.connector as mysql
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk

biome_insert_query = "INSERT INTO biome (Climate, TempRange, bName) VALUES (%s, %s, %s)"
habitat_insert_query = "INSERT INTO habitat (hname, location, avg_temp, avg_rain, climate, altitude_range, protected_areas, soil_type, h_BiomeID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
feature_insert_sql = """ INSERT INTO feature(Local_Materials, Terrain, Water_Feature) VALUES (%s, %s, %s)""" 
featureOf_insert_sql = """
INSERT INTO FeatureOf 
(F_BiomeID, F_FeatureID) 
VALUES (%s, %s);
"""
reserch_insert_sql = """ INSERT INTO researcher(Password, Name, Qualifications, R_AdminID) VALUES (%s, %s, %s, %s); """ 
plant_insert_query = """
INSERT INTO Plant 
(PCommonName, PScientificName, LifeCycle, PlantType, FloweringPeriod, 
 P_BiomeID, P_HabitatID, P_ASpeciesID, P_UserID, P_AdminID) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""
animal_insert_query = """INSERT INTO Animal (ACommonName, ASpeciesName, LifeSpan, Size, AnimalClass, T_SpeciesID, E_SpeciesID, A_BiomeID, A_HabitatID, P_SpeciesID, A_UserID, A_AdminID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
admin_insert_query = """ INSERT INTO admin(Name, Password) VALUES (%s, %s); """ 

class INSERT_APP():
    def __init__(self, root, connection):
        self.root=root
        self.connection = connection
        self.root.title("Insert Window")
        self.root.geometry(f"{425}x{350}")

        self.label = ctk.CTkLabel(self.root, text="Insert what Entity into the table?")
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")

        # Insert Habitat button 
        self.habitat_button = ctk.CTkButton(self.root, text="Add to Habitat", command=self.open_habitat)
        self.habitat_button.grid(row=1, column=0, padx=20, pady=(20, 10),sticky="w")

        # Insert FeatureOf button 
        self.featureOf_button = ctk.CTkButton(self.root, text="Add to FeatureOf", command=self.open_featureOf)
        self.featureOf_button.grid(row=1, column=1, padx=20, pady=(20, 10),sticky="w")

        # Insert Plant button
        self.plant_button = ctk.CTkButton(self.root, text="Add to Plant", command=self.open_plant)
        self.plant_button.grid(row=2, column=0, padx=20, pady=(20, 10),sticky="w")

        # Insert Researcher button
        self.researcher_button = ctk.CTkButton(self.root, text="Add to Researcher", command=self.open_researcher)
        self.researcher_button.grid(row=2, column=1, padx=20, pady=(20, 10),sticky="w")

        # Insert Animal button
        self.animal_buttom = ctk.CTkButton(self.root, text="Add an Animal", command=self.add_animal)
        self.animal_buttom.grid(row=3, column=0, padx=20, pady=(20, 10),sticky="w")

        # Insert Feature button
        self.feature_button = ctk.CTkButton(self.root, text="Add a Feature", command=self.add_feature)
        self.feature_button.grid(row=3, column=1, padx=20, pady=(20, 10),sticky="w")

        # Insert Admin button
        self.admin_button = ctk.CTkButton(self.root, text="Add an Admin", command=self.add_admin)
        self.admin_button.grid(row=4, column=0, padx=20, pady=(20, 10),sticky="w")
        # Insert Biome button
        self.biome_button =ctk.CTkButton(self.root, text="Add a Biome", command=self.add_biome)
        self.biome_button.grid(row=4, column=1, padx=20, pady=(20, 10),sticky="w")
        



     # Here we add buttons for insert, update, delete
    # Connect to the insert, delete, and update class
    def open_featureOf(self):
        featureOf_window =  ctk.CTkToplevel(self.root)
        featureOf_window.focus()
        featureOf_app = FeatureOfApp(featureOf_window, self.connection)

    def open_habitat(self):
        habitat_window = ctk.CTkToplevel(self.root)
        habitat_window.focus()
        habitat_app = HabitatApp(habitat_window, self.connection)

    def open_plant(self):
        plant_window =  ctk.CTkToplevel(self.root)
        plant_window.focus()
        plant_app = PlantApp(plant_window, self.connection)

    def open_researcher(self):
        researcher_window =  ctk.CTkToplevel(self.root)
        researcher_window.focus()
        researcher_app = ResearcherApp(researcher_window, self.connection)

    def add_animal(self):
        animal_window =  ctk.CTkToplevel(self.root)
        animal_window.focus()
        animal_app = AnimalApp(animal_window, self.connection)

        # #create a button to close the popup
        # close_button = ctk.CTkToplevel(self.root, text ="Close", command = self.root.quit)
        # close_button.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")

    def add_feature(self):
        feature_window =  ctk.CTkToplevel(self.root)
        feature_window.focus()
        feature_app = FeatureApp(feature_window, self.connection)

        # #create a button to close the popup
        # close_button =  ctk.CTkToplevel(self.root, text ="Close", command = self.root.quit)
        # close_button.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")

        self.root.mainloop()

    def add_admin(self):
        admin_window =  ctk.CTkToplevel(self.root)
        admin_window.focus()
        admin_app = AdminApp(admin_window, self.connection)

        #create a button to close the popup
        # close_button =  ctk.CTkToplevel(self.root, text ="Close", command = self.root.quit)
        # close_button.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")

        # self.root.mainloop()

    def add_biome(self):
        biome_window =  ctk.CTkToplevel(self.root)
        biome_window.focus()
        biome_app = BiomeApp(biome_window, self.connection)

        #create a button to close the popup
        # close_button = ctk.CTkButton(self.root, text ="Close", command = self.root.quit)
        # close_button.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")

class FeatureOfApp:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Add Feature to FeatureOf")
        self.root.geometry(f"{425}x{350}")

        # Labels and Entry for F_BiomeID
        self.biome_label = ctk.CTkLabel(root, text="Enter F_BiomeID:")
        self.biome_label.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")
        self.biome_entry = ctk.CTkEntry(root)
        self.biome_entry.grid(row=1, column=0, padx=20, pady=(20, 10),sticky="w")

        # Labels and Entry for F_FeatureID
        self.feature_label = ctk.CTkLabel(root, text="Enter F_FeatureID:")
        self.feature_label.grid(row=0, column=1, padx=20, pady=(20, 10),sticky="w")
        self.feature_entry = ctk.CTkEntry(root)
        self.feature_entry.grid(row=1, column=1, padx=20, pady=(20, 10),sticky="w")

        # Button to add to FeatureOf
        self.add_button = ctk.CTkButton(root, text="Add to FeatureOf", command=self.add_to_featureOf)
        self.add_button.grid(row=3, column=0, padx=20, pady=(20, 10),sticky="ew")

        # Label for displaying messages
        self.message_label =ctk.CTkLabel(root, text="", fg="blue")
        self.message_label.grid(row=3, column=0, padx=20, pady=(20, 10),sticky="ew")

    def add_to_featureOf(self):
        f_biome_id = self.biome_entry.get()
        f_feature_id = self.feature_entry.get()

        # Insert the data to the database
        try:
            mycursor = self.connection.cursor()
            mycursor.execute(featureOf_insert_sql, (f_biome_id, f_feature_id))
            self.connection.commit()
            mycursor.close()
            messagebox.showinfo("Success", "Successfully added to FeatureOf")

            # Show success message and clear the fields
            self.message_label.config(text="Successfully added to FeatureOf", fg="green")
            self.biome_entry.delete(0, tk.END)
            self.feature_entry.delete(0, tk.END)

            #self.root.after(3000, self.clear_message) #only show the message for 3 secconds
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add data: {e}")

    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.config(text="")

class HabitatApp:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Add Habitat")
        self.root.geometry(f"{400}x{650}")

        # Title
        self.title_label = ctk.CTkLabel(root, text="Habitat Information")
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="ew")
        #hname, location, avg_temp, avg_rain, climate, altitude_range, protected_areas, soil_type, h_BiomeID
        # hname
        self.hname_label = ctk.CTkLabel(root, text="Enter habitat name:")
        self.hname_label.grid(row=1, column=0, padx=20, pady=(20, 10),sticky="w")
        self.hname_entry = ctk.CTkEntry(root)
        self.hname_entry.grid(row=2, column=0, padx=20, pady=(20, 10),sticky="w")

        # location
        self.location_label = ctk.CTkLabel(root, text="Enter habitat location:")
        self.location_label.grid(row=1, column=1, padx=20, pady=(20, 10),sticky="w")
        self.location_entry = ctk.CTkEntry(root)
        self.location_entry.grid(row=2, column=1, padx=20, pady=(20, 10),sticky="w")

        # avg_temp
        self.avg_temp_label = ctk.CTkLabel(root, text="Enter average temperature:")
        self.avg_temp_label.grid(row=3, column=0, padx=20, pady=(20, 10),sticky="w")
        self.avg_temp_entry = ctk.CTkEntry(root)
        self.avg_temp_entry.grid(row=4, column=0, padx=20, pady=(20, 10),sticky="w")

        # avg_rain
        self.avg_rain_label = ctk.CTkLabel(root, text="Enter average rainfall:")
        self.avg_rain_label.grid(row=3, column=1, padx=20, pady=(20, 10),sticky="w")
        self.avg_rain_entry = ctk.CTkEntry(root)
        self.avg_rain_entry.grid(row=4, column=1, padx=20, pady=(20, 10),sticky="w")

        # climate
        self.climate_label = ctk.CTkLabel(root, text="Enter habitat climate:")
        self.climate_label.grid(row=5, column=0, padx=20, pady=(20, 10),sticky="w")
        self.climate_entry = ctk.CTkEntry(root)
        self.climate_entry.grid(row=6, column=0, padx=20, pady=(20, 10),sticky="w")

        # altitude_range
        self.altitude_range_label = ctk.CTkLabel(root, text="Enter altitude range:")
        self.altitude_range_label.grid(row=5, column=1, padx=20, pady=(20, 10),sticky="w")
        self.altitude_range_entry = ctk.CTkEntry(root)
        self.altitude_range_entry.grid(row=6, column=1, padx=20, pady=(20, 10),sticky="w")

        # protected_areas
        self.protected_areas_label = ctk.CTkLabel(root, text="Enter protected areas:")
        self.protected_areas_label.grid(row=7, column=0, padx=20, pady=(20, 10),sticky="w")
        self.protected_areas_entry = ctk.CTkEntry(root)
        self.protected_areas_entry.grid(row=8, column=0, padx=20, pady=(20, 10),sticky="w")

        # soil_type
        self.soil_type_label = ctk.CTkLabel(root, text="Enter soil type:")
        self.soil_type_label.grid(row=7, column=1, padx=20, pady=(20, 10),sticky="w")
        self.soil_type_entry = ctk.CTkEntry(root)
        self.soil_type_entry.grid(row=8, column=1, padx=20, pady=(20, 10),sticky="w")

        # h_BiomeID
        self.h_BiomeID_label = ctk.CTkLabel(root, text="Enter Biome ID for the habitat:")
        self.h_BiomeID_label.grid(row=9, column=0, padx=20, pady=(20, 10),sticky="w")
        self.h_BiomeID_entry = ctk.CTkEntry(root)
        self.h_BiomeID_entry.grid(row=10, column=0, padx=20, pady=(20, 10),sticky="w")

        # Button to add to Habitat
        self.add_button = ctk.CTkButton(root, text="Add to Habitat", command=self.add_to_habitat)
        self.add_button.grid(row=10, column=1, padx=20, pady=(20, 10),sticky="w")

        # Label for displaying messages
        self.message_label = ctk.CTkLabel(root, text="", fg_color="blue")
        self.message_label.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")

    def add_to_habitat(self):
        hname = self.hname_entry.get()
        location = self.location_entry.get()
        avg_temp = self.avg_temp_entry.get()
        avg_rain = self.avg_rain_entry.get()
        climate = self.climate_entry.get()
        altitude_range = self.altitude_range_entry.get()
        protected_areas = self.protected_areas_entry.get()
        soil_type = self.soil_type_entry.get()
        h_BiomeID = self.h_BiomeID_entry.get()

        # SQL Query
        habitat_insert_query = """INSERT INTO Habitat (hname, location, avg_temp, avg_rain, climate, altitude_range, protected_areas, soil_type, h_BiomeID)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        try:
            mycursor = self.connection.cursor()
            mycursor.execute(habitat_insert_query, (hname, location, avg_temp, avg_rain, climate, altitude_range, protected_areas, soil_type, h_BiomeID))
            self.connection.commit()
            mycursor.close()

            # Show success message in label and clear the fields
            self.message_label.configure(text="Successfully added to Habitat", fg="green")
            self.hname_entry.delete(0, tk.END)
            self.location_entry.delete(0, tk.END)
            self.avg_temp_entry.delete(0, tk.END)
            self.avg_rain_entry.delete(0, tk.END)
            self.climate_entry.delete(0, tk.END)
            self.altitude_range_entry.delete(0, tk.END)
            self.protected_areas_entry.delete(0, tk.END)
            self.soil_type_entry.delete(0, tk.END)
            self.h_BiomeID_entry.delete(0, tk.END)
            
            self.root.after(3000, self.clear_message) #only show the message for 3 secconds

        except Exception as e:
            self.message_label.config(text=f"Failed to add data: {e}", fg="red")

    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.config(text="")

class PlantApp:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.geometry(f"{400}x{750}")

        # Title
        self.title_label = ctk.CTkLabel(root, text="Plant Information")
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")

        # Plant name
        self.pname_label = ctk.CTkLabel(root, text="Enter plant name:")
        self.pname_label.grid(row=1, column=0, padx=20, pady=(20, 10),sticky="w")
        self.pname_entry = ctk.CTkEntry(root)
        self.pname_entry.grid(row=2, column=0, padx=20, pady=(20, 10),sticky="w")

        # Scientific name
        self.scientific_name_label = ctk.CTkLabel(root, text="Enter scientific name:")
        self.scientific_name_label.grid(row=1, column=1, padx=20, pady=(20, 10),sticky="w")
        self.scientific_name_entry = ctk.CTkEntry(root)
        self.scientific_name_entry.grid(row=2, column=1, padx=20, pady=(20, 10),sticky="w")

        # Family
        self.family_label = ctk.CTkLabel(root, text="Enter plant family:")
        self.family_label.grid(row=3, column=0, padx=20, pady=(20, 10),sticky="w")
        self.family_entry = ctk.CTkEntry(root)
        self.family_entry.grid(row=4, column=0, padx=20, pady=(20, 10),sticky="w")

        # Habitat ID
        self.habitat_id_label = ctk.CTkLabel(root, text="Enter habitat ID:")
        self.habitat_id_label.grid(row=3, column=1, padx=20, pady=(20, 10),sticky="w")
        self.habitat_id_entry = ctk.CTkEntry(root)
        self.habitat_id_entry.grid(row=4, column=1, padx=20, pady=(20, 10),sticky="w")

        # Description
        self.description_label = ctk.CTkLabel(root, text="Enter description:")
        self.description_label.grid(row=5, column=0, padx=20, pady=(20, 10),sticky="w")
        self.description_entry = ctk.CTkEntry(root)
        self.description_entry.grid(row=6, column=0, padx=20, pady=(20, 10),sticky="w")

        # Life Cycle
        self.lifecycle_label = ctk.CTkLabel(root, text="Enter Life Cycle:")
        self.lifecycle_label.grid(row=5, column=1, padx=20, pady=(20, 10),sticky="w")
        self.lifecycle_entry = ctk.CTkEntry(root)
        self.lifecycle_entry.grid(row=6, column=1, padx=20, pady=(20, 10),sticky="w")

        # Plant Type
        self.planttype_label = ctk.CTkLabel(root, text="Enter Plant Type:")
        self.planttype_label.grid(row=7, column=0, padx=20, pady=(20, 10),sticky="w")
        self.planttype_entry = ctk.CTkEntry(root)
        self.planttype_entry.grid(row=8, column=0, padx=20, pady=(20, 10),sticky="w")

        # Flowering Period
        self.flowering_label = ctk.CTkLabel(root, text="Enter Flowering Period:")
        self.flowering_label.grid(row=7, column=1, padx=20, pady=(20, 10),sticky="w")
        self.flowering_entry = ctk.CTkEntry(root)
        self.flowering_entry.grid(row=8, column=1, padx=20, pady=(20, 10),sticky="w")

        # Biome ID
        self.biome_id_label = ctk.CTkLabel(root, text="Enter Biome ID:")
        self.biome_id_label.grid(row=9, column=0, padx=20, pady=(20, 10),sticky="w")
        self.biome_id_entry = ctk.CTkEntry(root)
        self.biome_id_entry.grid(row=10, column=0, padx=20, pady=(20, 10),sticky="w")

        # ASpecies ID
        self.aspecies_id_label = ctk.CTkLabel(root, text="Enter ASpecies ID:")
        self.aspecies_id_label.grid(row=9, column=1, padx=20, pady=(20, 10),sticky="w")
        self.aspecies_id_entry = ctk.CTkEntry(root)
        self.aspecies_id_entry.grid(row=10, column=1, padx=20, pady=(20, 10),sticky="w")

        # User ID
        self.user_id_label = ctk.CTkLabel(root, text="Enter User ID:")
        self.user_id_label.grid(row=11, column=0, padx=20, pady=(20, 10),sticky="w")
        self.user_id_entry = ctk.CTkEntry(root)
        self.user_id_entry.grid(row=12, column=0, padx=20, pady=(20, 10),sticky="w")

        # Admin ID
        self.admin_id_label = ctk.CTkLabel(root, text="Enter Admin ID:")
        self.admin_id_label.grid(row=11, column=0, padx=20, pady=(20, 10),sticky="w")
        self.admin_id_entry = ctk.CTkEntry(root)
        self.admin_id_entry.grid(row=12, column=0, padx=20, pady=(20, 10),sticky="w")

        # # Photo =====================================================
        # # Upload and Display Photo
        # def upload_image():
        #     file_path = filedialog.askopenfilename()
        #     if not file_path:
        #         return
        #     # Got the filepath, now create thumbnail to display in the window
        #     image = Image.open(file_path)
        #     image.thumbnail((150, 150))  # Thumbnail the image to a suitable size
        #     photo = ImageTk.PhotoImage(image)
        #     self.image_label.config(image=photo)
        #     self.image_label.photo = photo  # keep a reference to prevent garbage collection 
        #     self.file_path = file_path  # store file path for later use (e.g. if you want to save the path or copy the file)

        # self.photo_label = tk.Label(root, text="Upload photo:")
        # self.photo_label.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")
        # self.upload_button = ctk.CTkButton(root, text="Upload", command=upload_image)
        # self.upload_button.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")
        # self.image_label = tk.Label(root)
        # self.image_label.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")
        # # Photo =====================================================


        # Button to add plant
        self.add_button = ctk.CTkButton(root, text="Add Plant", command=self.add_to_plant)
        self.add_button.grid(row=13, column=0, padx=20, pady=(20, 10),sticky="w")

        # Message label to show success or error messages
        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")

    def add_to_plant(self):
        pname = self.pname_entry.get()
        scientific_name = self.scientific_name_entry.get()
        lifecycle = self.lifecycle_entry.get()
        planttype = self.planttype_entry.get()
        flowering = self.flowering_entry.get()
        biome_id = self.biome_id_entry.get()
        habitat_id = self.habitat_id_entry.get()
        aspecies_id = self.aspecies_id_entry.get()
        user_id = self.user_id_entry.get()
        admin_id = self.admin_id_entry.get()
        
        # with open(self.file_path, "rb") as file:
        #     binary_data = file.read()

        plant_insert_query = """
        INSERT INTO Plant 
        (PCommonName, PScientificName, LifeCycle, PlantType, FloweringPeriod, 
        P_BiomeID, P_HabitatID, P_ASpeciesID, P_UserID, P_AdminID) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        try:
            mycursor = self.connection.cursor()
            mycursor.execute(plant_insert_query, (pname, scientific_name, lifecycle, planttype, 
                                                  flowering, biome_id, habitat_id, aspecies_id, 
                                                  user_id, admin_id))
            self.connection.commit()
            mycursor.close()

           # Show success message in label and clear the fields
            self.message_label.config(text="Successfully added to Plant", fg="green")
            self.pname_entry.delete(0, tk.END)
            self.scientific_name_entry.delete(0, tk.END)
            self.lifecycle_entry.delete(0, tk.END)
            self.planttype_entry.delete(0, tk.END)
            self.flowering_entry.delete(0, tk.END)
            self.biome_id_entry.delete(0, tk.END)
            self.habitat_id_entry.delete(0, tk.END)
            self.aspecies_id_entry.delete(0, tk.END)
            self.user_id_entry.delete(0, tk.END)
            self.admin_id_entry.delete(0, tk.END)
            # self.image_label.config(image=None)
            # self.image_label.photo = None  # Clear the reference to the image
            # self.file_path = ""  # Reset the file path
            
            self.root.after(3000, self.clear_message)

        except Exception as e:
            self.message_label.config(text=f"Failed to add data: {e}", fg="red")
            #self.root.after(3000, self.clear_message)

    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.config(text="")

class ResearcherApp:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.geometry(f"{400}x{350}")

        # Title
        self.title_label = ctk.CTkLabel(root, text="Researcher Information")
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")

        # Researcher Name
        self.name_label = ctk.CTkLabel(root, text="Enter researcher name:")
        self.name_label.grid(row=1, column=0, padx=20, pady=(20, 10),sticky="w")
        self.name_entry = ctk.CTkEntry(root)
        self.name_entry.grid(row=2, column=0, padx=20, pady=(20, 10),sticky="w")

        # Password
        self.password_label = ctk.CTkLabel(root, text="Enter password:")
        self.password_label.grid(row=1, column=1, padx=20, pady=(20, 10),sticky="w")
        self.password_entry = ctk.CTkEntry(root, show="*")  # password field
        self.password_entry.grid(row=2, column=1, padx=20, pady=(20, 10),sticky="w")

        # Qualifications
        self.qualifications_label = ctk.CTkLabel(root, text="Enter qualifications:")
        self.qualifications_label.grid(row=3, column=0, padx=20, pady=(20, 10),sticky="w")
        self.qualifications_entry = ctk.CTkEntry(root)
        self.qualifications_entry.grid(row=4, column=0, padx=20, pady=(20, 10),sticky="w")

        # Admin ID -- maybe no this
        self.admin_id_label = ctk.CTkLabel(root, text="Enter admin ID:")
        self.admin_id_label.grid(row=3, column=1, padx=20, pady=(20, 10),sticky="w")
        self.admin_id_entry = ctk.CTkEntry(root)
        self.admin_id_entry.grid(row=4, column=1, padx=20, pady=(20, 10),sticky="w")

        # Button to add researcher
        self.add_button = ctk.CTkButton(root, text="Add Researcher", command=self.add_to_researcher)
        self.add_button.grid(row=5, column=0, padx=20, pady=(20, 10),sticky="w")

        # Message label
        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.grid(row=7, column=0, padx=20, pady=(20, 10),sticky="w")

    def add_to_researcher(self):
        name = self.name_entry.get()
        password = self.password_entry.get()
        qualifications = self.qualifications_entry.get()
        admin_id = self.admin_id_entry.get()

        # SQL Query
        researcher_insert_query = """ INSERT INTO researcher(Password, Name, Qualifications, R_AdminID) VALUES (%s, %s, %s, %s); """ 

        try:
            mycursor = self.connection.cursor()
            mycursor.execute(researcher_insert_query, (password, name, qualifications, admin_id))
            self.connection.commit()
            mycursor.close()

            # Show success message in label and clear the fields
            self.message_label.config(text="Successfully added researcher", fg="green")
            self.name_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.qualifications_entry.delete(0, tk.END)
            self.admin_id_entry.delete(0, tk.END)
            self.root.after(3000, self.clear_message) #only show the message for 3 secconds

        except Exception as e:
            self.message_label.config(text=f"Failed to add data: {e}", fg="red")

    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.config(text="")

class AnimalApp:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Adding an Animal")
        self.root.geometry(f"{450}x{875}")

        self.title_label = ctk.CTkLabel(root, text="Enter Animal Information")
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")

        self.aname_label = ctk.CTkLabel(root, text="Enter the Animal's common name:")
        self.aname_label.grid(row=1, column=0, padx=20, pady=(20, 10),sticky="w")
        self.aname_entry = ctk.CTkEntry(root)
        self.aname_entry.grid(row=2, column=0, padx=20, pady=(20, 10),sticky="w")

        self.ascientific_name_label = ctk.CTkLabel(root, text="Enter the Animal's scientific name:")
        self.ascientific_name_label.grid(row=1, column=1, padx=20, pady=(20, 10),sticky="w")
        self.ascientific_name_entry = ctk.CTkEntry(root)
        self.ascientific_name_entry.grid(row=2, column=1, padx=20, pady=(20, 10),sticky="w")

        self.lifespan_label = ctk.CTkLabel(root, text="Enter the Animal's LifeSpan:")
        self.lifespan_label.grid(row=3, column=0, padx=20, pady=(20, 10),sticky="w")
        self.lifespan_entry = ctk.CTkEntry(root)
        self.lifespan_entry.grid(row=4, column=0, padx=20, pady=(20, 10),sticky="w")

        # might be something we add later but should we have the user enter the biome name and species
        # name and we pull the ID from the corresponding table using the name?
        self.habitat_id_label = ctk.CTkLabel(root, text="Enter habitat ID:")
        self.habitat_id_label.grid(row=3, column=1, padx=20, pady=(20, 10),sticky="w")
        self.habitat_id_entry = ctk.CTkEntry(root)
        self.habitat_id_entry.grid(row=4, column=1, padx=20, pady=(20, 10),sticky="w")

        self.size_label = ctk.CTkLabel(root, text="Enter the Size of the Animal:")
        self.size_label.grid(row=5, column=0, padx=20, pady=(20, 10),sticky="w")
        self.size_entry = ctk.CTkEntry(root)
        self.size_entry.grid(row=6, column=0, padx=20, pady=(20, 10),sticky="w")

        #drop down?
        self.class_label = ctk.CTkLabel(root, text="Enter the Animal Class:")
        self.class_label.grid(row=5, column=1, padx=20, pady=(20, 10),sticky="w")
        self.class_entry = ctk.CTkEntry(root)
        self.class_entry.grid(row=6, column=1, padx=20, pady=(20, 10),sticky="w")

        self.biome_id_label = ctk.CTkLabel(root, text="Enter Biome ID:")
        self.biome_id_label.grid(row=7, column=0, padx=20, pady=(20, 10),sticky="w")
        self.biome_id_entry = ctk.CTkEntry(root)
        self.biome_id_entry.grid(row=8, column=0, padx=20, pady=(20, 10),sticky="w")

        self.pspecies_id_label = ctk.CTkLabel(root, text="Enter PSpecies ID:")
        self.pspecies_id_label.grid(row=7, column=1, padx=20, pady=(20, 10),sticky="w")
        self.pspecies_id_entry = ctk.CTkEntry(root)
        self.pspecies_id_entry.grid(row=8, column=1, padx=20, pady=(20, 10),sticky="w")

        self.tspecies_id_label = ctk.CTkLabel(root, text="Enter Threat Species ID:")
        self.tspecies_id_label.grid(row=9, column=0, padx=20, pady=(20, 10),sticky="w")
        self.title_labelspecies_id_entry = ctk.CTkEntry(root)
        self.title_labelspecies_id_entry.grid(row=10, column=0, padx=20, pady=(20, 10),sticky="w")

        self.especies_id_label = ctk.CTkLabel(root, text="Enter Prey Species ID:")
        self.especies_id_label.grid(row=9, column=1, padx=20, pady=(20, 10),sticky="w")
        self.especies_id_entry = ctk.CTkEntry(root)
        self.especies_id_entry.grid(row=10, column=1, padx=20, pady=(20, 10),sticky="w")

        self.auser_id_label = ctk.CTkLabel(root, text="Enter User ID:")
        self.auser_id_label.grid(row=11, column=0, padx=20, pady=(20, 10),sticky="w")
        self.auser_id_entry = ctk.CTkEntry(root)
        self.auser_id_entry.grid(row=12, column=0, padx=20, pady=(20, 10),sticky="w")

        self.aadmin_id_label = ctk.CTkLabel(root, text="Enter Admin ID:")
        self.aadmin_id_label.grid(row=11, column=1, padx=20, pady=(20, 10),sticky="w")
        self.aadmin_id_entry = ctk.CTkEntry(root)
        self.aadmin_id_entry.grid(row=12, column=1, padx=20, pady=(20, 10),sticky="w")

        self.add_button = ctk.CTkButton(root, text="Add Animal", command=self.add_animal_to_database)
        self.add_button.grid(row=13, column=0, padx=20, pady=(20, 10),sticky="w")

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.grid(row=14, column=0, padx=20, pady=(20, 10),sticky="w")

    def add_animal_to_database(self):
        acommon_name = self.aname_entry.get()
        ascientific_name = self.ascientific_name_entry.get()
        lifespan = self.lifespan_entry.get()
        size = self.size_entry.get()
        animalclass = self.class_entry.get()
        tspecies_id = self.title_labelspecies_id_entry.get()
        especies_id = self.especies_id_entry.get()
        pspecies_id = self.pspecies_id_entry.get()
        biome_id = self.biome_id_entry.get()
        habitat_id = self.habitat_id_entry.get()
        auser_id = self.auser_id_entry.get()
        aadmin_id = self.aadmin_id_entry.get()
        
        if acommon_name and ascientific_name and lifespan and size and animalclass and tspecies_id and especies_id and pspecies_id and biome_id and habitat_id and auser_id and aadmin_id:
            try:
                mycursor = self.connection.cursor()
                mycursor.execute(animal_insert_query, (acommon_name, ascientific_name, lifespan, size, 
                                                    animalclass, tspecies_id, especies_id, biome_id, habitat_id, pspecies_id, 
                                                    auser_id, aadmin_id))
                self.connection.commit()
                mycursor.close()

                self.message_label.config(text="Successfully added to Animal", fg="green")
                self.aname_entry.delete(0, tk.END)
                self.ascientific_name_entry.delete(0, tk.END)
                self.lifespan_entry.delete(0, tk.END)
                self.size_entry.delete(0, tk.END)
                self.class_entry.delete(0, tk.END)
                self.title_labelspecies_id_entry.delete(0, tk.END)
                self.especies_id_entry.delete(0, tk.END)
                self.pspecies_id_entry.delete(0, tk.END)
                self.biome_id_entry.delete(0, tk.END)
                self.habitat_id_entry.delete(0, tk.END)
                self.auser_id_entry.delete(0, tk.END)
                self.aadmin_id_entry.delete(0, tk.END)

                self.root.after(3000, self.clear_message)

            except Exception as e:
                self.message_label.config(text=f"Failed to add data: {e}", fg="red")
                self.root.after(5000, self.clear_message)
        else:
            self.message_label.config(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.config(text="")

class FeatureApp:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Adding a Feature")
        self.root.geometry(f"{400}x{350}")

        self.title_label = ctk.CTkLabel(root, text="Enter Feature Information")
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")

        self.local_materials_label = ctk.CTkLabel(root, text="Enter Local Materials:")
        self.local_materials_label.grid(row=1, column=0, padx=20, pady=(20, 10),sticky="w")
        self.local_materials_entry = ctk.CTkEntry(root)
        self.local_materials_entry.grid(row=2, column=0, padx=20, pady=(20, 10),sticky="w")

        self.terrain_label =ctk.CTkLabel(root, text="Enter Terrain:")
        self.terrain_label.grid(row=1, column=1, padx=20, pady=(20, 10),sticky="w")
        self.terrain_entry = ctk.CTkEntry(root)
        self.terrain_entry.grid(row=2, column=1, padx=20, pady=(20, 10),sticky="w")

        self.wfeature_label = ctk.CTkLabel(root, text="Enter Water Feature:")
        self.wfeature_label.grid(row=3, column=0, padx=20, pady=(20, 10),sticky="w")
        self.wfeature_entry = ctk.CTkEntry(root)
        self.wfeature_entry.grid(row=4, column=0, padx=20, pady=(20, 10),sticky="w")

        self.add_button = ctk.CTkButton(root, text="Add to Feature", command=self.add_feature_to_database)
        self.add_button.grid(row=5, column=0, padx=20, pady=(20, 10),sticky="ew")

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")

    def add_feature_to_database(self):
        local_material = self.local_materials_entry.get()
        terrain = self.terrain_entry.get()
        water_feature = self.wfeature_entry.get()

        if local_material and terrain and water_feature:
            try:
                mycursor = self.connection.cursor()
                mycursor.execute(feature_insert_sql, (local_material, terrain, water_feature))
                self.connection.commit()
                mycursor.close()
                self.message_label.configure(text="Successfully added to Feature", fg="green")
                self.local_materials_entry.delete(0, tk.END)
                self.terrain_entry.delete(0, tk.END)
                self.wfeature_entry.delete(0, tk.END)
                self.root.after(3000, self.clear_message)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to add data: {e}")
                self.root.after(5000, self.clear_message)
        else:
            self.message_label.configure(text=f"Invalid input, try again", fg="red")
            self.root.after(5000, self.clear_message)
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.config(text="")

class AdminApp:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Adding an Administrator")
        self.root.geometry(f"{400}x{350}")

        self.title_label = ctk.CTkLabel(root, text="Enter Admin Information")
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")

        self.name_label = ctk.CTkLabel(root, text="Enter Admin name:")
        self.name_label.grid(row=1, column=0, padx=20, pady=(20, 10),sticky="w")
        self.name_entry = ctk.CTkEntry(root)
        self.name_entry.grid(row=2, column=0, padx=20, pady=(20, 10),sticky="w")

        self.password_label = ctk.CTkLabel(root, text="Enter password:")
        self.password_label.grid(row=1, column=1, padx=20, pady=(20, 10),sticky="w")
        self.password_entry = ctk.CTkEntry(root, show="*")  # password field
        self.password_entry.grid(row=2, column=1, padx=20, pady=(20, 10),sticky="w")

        self.add_button = ctk.CTkButton(root, text="Add", command=self.add_admin_to_database)
        self.add_button.grid(row=3, column=0, padx=20, pady=(20, 10),sticky="ew")

        self.message_label =ctk.CTkLabel(root, text="")
        self.message_label.grid(row=4, column=0, padx=20, pady=(20, 10),sticky="w")

    def add_admin_to_database(self):
        name = self.name_entry.get()
        password = self.password_entry.get()

        if password:
            if len(password) >= 6 and len(password) <= 64:
                    try:
                        mycursor = self.connection.cursor()
                        mycursor.execute(admin_insert_query, (name, password))
                        self.connection.commit()
                        mycursor.close()

                        self.message_label.configure(text="Successfully added admin", fg="green")
                        self.name_entry.delete(0, tk.END)
                        self.password_entry.delete(0, tk.END)
                        self.root.after(3000, self.clear_message)

                    except Exception as e:
                        self.message_label.configure(text=f"Failed to add admin data: {e}", fg="red")
                        self.root.after(5000, self.clear_message)
            else:
                self.message_label.configure(text=f"Password must be at least 6 character and at most 64 long", fg="red")
                self.root.after(5000, self.clear_message)
                
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class BiomeApp:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Adding a Biome")
        self.root.geometry(f"{400}x{350}")

        self.title_label = ctk.CTkLabel(root, text="Enter Biome Information")
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")

        # drop down?
        self.bname_label = ctk.CTkLabel(root, text="Enter Biome name:")
        self.bname_label.grid(row=1, column=0, padx=20, pady=(20, 10),sticky="w")
        self.biome_entry = ctk.CTkEntry(root)
        self.biome_entry.grid(row=2, column=0, padx=20, pady=(20, 10),sticky="w")

        # drop down?
        self.temp_range_label = ctk.CTkLabel(root, text="Enter Temperature Range:")
        self.temp_range_label.grid(row=1, column=1, padx=20, pady=(20, 10),sticky="w")
        self.temp_range_entry = ctk.CTkEntry(root)
        self.temp_range_entry.grid(row=2, column=1, padx=20, pady=(20, 10),sticky="w")
        
        self.climate_label = ctk.CTkLabel(root, text="Enter the Climate of the Biome:")
        self.climate_label.grid(row=3, column=0, padx=20, pady=(20, 10),sticky="w")
        self.climate_entry = ctk.CTkEntry(root)
        self.climate_entry.grid(row=4, column=0, padx=20, pady=(20, 10),sticky="w")

        self.add_button = ctk.CTkButton(root, text="Add to Biome", command=self.add_biome_to_database)
        self.add_button.grid(row=5, column=0, padx=20, pady=(20, 10),sticky="w")

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.grid(row=5, column=1, padx=20, pady=(20, 10),sticky="w")

    def add_biome_to_database(self):
        bname = self.biome_entry.get()
        temp_range = self.temp_range_entry.get()
        climate = self.climate_entry.get()

        if bname and temp_range and climate:
            try:
                mycursor = self.connection.cursor()
                mycursor.execute(biome_insert_query, (climate, temp_range, bname))
                self.connection.commit()
                mycursor.close()

                self.message_label.config(text="Successfully added to Biome", fg="green")
                self.biome_entry.delete(0, tk.END)
                self.temp_range_entry.delete(0, tk.END)
                self.climate_entry.delete(0, tk.END)
                self.root.after(3000, self.clear_message)

            except Exception as e:
                self.message_label.config(text=f"Failed to add data: {e}", fg="red")
                self.root.after(5000, self.clear_message)
        else:
            self.message_label.config(text=f"Invalid input, try again", fg="red")
            self.root.after(5000, self.clear_message)
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.config(text="")
