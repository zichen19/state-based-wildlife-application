#testing connector from Phase 1 Files
import mysql.connector as mysql
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import customtkinter as ctk

import os
import json
import display_advanced

def update_search_count(search_type):
    """Updates the count of searches for a given type in searchdata.json."""
    file_path = 'searchdata.json'

    # Check if the file exists, if not create it with an empty dictionary
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump({}, file)

    # Read the existing data
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Increment the count for the given search type
    if search_type in data:
        data[search_type] += 1
    else:
        data[search_type] = 1

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file)

class ANIMAL_SEARCH():
    def __init__(self, root, connection):
        self.root=root
        self.connection = connection
        self.root.title("Animal Search Window")
        self.root.geometry("500x500")

        self.label = ctk.CTkLabel(root, text="Search for an Animal: ")
        self.label.pack(pady=20, padx=20)


        self.search_by_animaltype_button = ctk.CTkButton(root, text="Search by Animal type", command=self.search_animaltype, state=tk.DISABLED)
        self.search_by_animaltype_button.pack(pady=10)
        self.search_by_animaltype_button.configure(state=tk.NORMAL)

        self.search_by_animal_commonname_button = ctk.CTkButton(root, text="Search by Animal Common Name", command=self.search_animalcommonname, state=tk.DISABLED)
        self.search_by_animal_commonname_button.pack(pady=10)
        self.search_by_animal_commonname_button.configure(state=tk.NORMAL)

        self.search_by_animal_scientific_name_button = ctk.CTkButton(root, text="Search by Animal Scientific Name", command=self.search_animalscientificname, state=tk.DISABLED)
        self.search_by_animal_scientific_name_button.pack(pady=10)
        self.search_by_animal_scientific_name_button.configure(state=tk.NORMAL)

        self.search_by_animal_size_button = ctk.CTkButton(root, text="Search by Animal's Size", command=self.search_animalsize, state=tk.DISABLED)
        self.search_by_animal_size_button.pack(pady=10)
        self.search_by_animal_size_button.configure(state=tk.NORMAL)

        self.search_by_animal_life_span_button = ctk.CTkButton(root, text="Search by Animal's Life Span", command=self.search_animal_life_span, state=tk.DISABLED)
        self.search_by_animal_life_span_button.pack(pady=10)
        self.search_by_animal_life_span_button.configure(state=tk.NORMAL)


    def search_animaltype(self):
        update_search_count('animal')
        animaltype_window = ctk.CTkToplevel(self.root)
        animaltype_window.focus()
        animaltype_app = SEARCH_ANIMAL_TYPE(animaltype_window, self.connection)

    def search_animalcommonname(self):
        update_search_count('animal')
        animalcname_window = ctk.CTkToplevel(self.root)
        animalcname_window.focus()
        animalcname_app = SEARCH_ANIMAL_CNAME(animalcname_window, self.connection)

    def search_animalscientificname(self):
        update_search_count('animal')
        animalsname_window = ctk.CTkToplevel(self.root)
        animalsname_window.focus()
        animalsname_app = SEARCH_ANIMAL_SNAME(animalsname_window, self.connection)
    
    def search_animalsize(self):
        update_search_count('animal')
        animalsize_window = ctk.CTkToplevel(self.root)
        animalsize_window.focus()
        animalsize_app = SEARCH_ANIMAL_SIZE(animalsize_window, self.connection)

    def search_animal_life_span(self):
        update_search_count('animal')
        animal_life_span_window = ctk.CTkToplevel(self.root)
        animal_life_span_window.focus()
        animal_life_span_app = SEARCH_ANIMAL_LIFE_SPAN(animal_life_span_window, self.connection)
    
class SEARCH_ANIMAL_TYPE:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Animal Class Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for an Animal by Type")
        self.class_label.pack(pady=20)

        self.class_label = ctk.CTkLabel(root, text="Enter the Animal Class:")
        self.class_label.pack(pady=5)
        self.class_entry = ctk.CTkEntry(root)
        self.class_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Animals", command=self.find_commonname_by_class)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_commonname_by_class(self):
        animalclass = self.class_entry.get()
        animal_class_search_query = """ (SELECT ACommonName FROM Animal WHERE AnimalClass = %s); """

        if animalclass:
                mycursor = self.connection.cursor()
                vals = (self.class_entry.get(),) 
                mycursor.execute(animal_class_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                animals_common_names = [result[0] for result in results]

                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root , variable=self.entity_var ,values= animals_common_names, command = self.send_animal_to_print_cname) 
                self.dropdownEntity.pack() 

                self.class_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg_color="red")
            self.root.after(5000, self.clear_message)

    #not used?
    def find_speciesname_by_cname(self, commonname):
        animal_sname_search_query = """ (SELECT ASpeciesName FROM Animal WHERE ACommonName = %s); """

        mycursor = self.connection.cursor()
        vals = (commonname, ) 
        mycursor.execute(animal_sname_search_query, vals)
        results = mycursor.fetchall()
        mycursor.close()
        animals_scientific_names = [result[0] for result in results]

        self.entity_var = StringVar(self.root)
        self.dropdownEntity = OptionMenu(self.root , self.entity_var , *animals_scientific_names, command = self.send_animal_to_print_cname) 
        self.dropdownEntity.pack() 


    def send_animal_to_print_cname(self, selected_value):
        animal_search_query = """ SELECT * FROM Animal WHERE ACommonName = %s """
        
        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(animal_search_query, vals)
        animal_vals = mycursor.fetchall()
        mycursor.close()
        printing_animal_window = ctk.CTkToplevel(self.root)
        print_animal_app = display_advanced.Display_Page(printing_animal_window, *animal_vals, "Animal")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_ANIMAL_SIZE:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Animal Size Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for an Animal by it's size")
        self.class_label.pack(pady=20)

        self.size_label = ctk.CTkLabel(root, text="Enter the Animal Size:")
        self.size_label.pack(pady=5)
        self.size_entry = ctk.CTkEntry(root)
        self.size_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Animals", command=self.find_commonname_by_size)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_commonname_by_size(self):
        animalsize = self.size_entry.get()
        animal_size_search_query = """ (SELECT ACommonName FROM Animal WHERE Size = %s); """

        if animalsize:
                mycursor = self.connection.cursor()
                vals = (self.size_entry.get(),) 
                mycursor.execute(animal_size_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                animals_common_names = [result[0] for result in results]

                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root , variable=self.entity_var , values=animals_common_names, command = self.send_animal_to_print_cname) 
                self.dropdownEntity.pack() 

                self.size_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg_color="red")
            self.root.after(5000, self.clear_message)

    def find_speciesname_by_cname(self, commonname):
        animal_sname_search_query = """ (SELECT ASpeciesName FROM Animal WHERE ACommonName = %s); """

        mycursor = self.connection.cursor()
        vals = (commonname, ) 
        mycursor.execute(animal_sname_search_query, vals)
        results = mycursor.fetchall()
        mycursor.close()
        animals_scientific_names = [result[0] for result in results]

        self.entity_var = StringVar(self.root)
        self.dropdownEntity = OptionMenu(self.root , self.entity_var , *animals_scientific_names, command = self.send_animal_to_print_cname) 
        self.dropdownEntity.pack() 

        self.class_entry.delete(0, tk.END)

    def send_animal_to_print_cname(self,selected_value):
        animal_search_query = """ SELECT * FROM Animal WHERE ACommonName = %s """
        
        mycursor = self.connection.cursor()
        vals = (self.entity_var.get(),) 
        mycursor.execute(animal_search_query, vals)
        animal_vals = mycursor.fetchall()
        mycursor.close()
        printing_animal_window = ctk.CTkToplevel(self.root)
        print_animal_app = display_advanced.Display_Page(printing_animal_window, *animal_vals, "Animal")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_ANIMAL_LIFE_SPAN:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Animal Life Span Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for an Animal by it's life span")
        self.class_label.pack(pady=20)

        self.life_span_label = ctk.CTkLabel(root, text="Enter the Animal Life Span:")
        self.life_span_label.pack(pady=5)
        self.life_span_entry = ctk.CTkEntry(root)
        self.life_span_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Animals", command=self.find_commonname_by_life_span)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_commonname_by_life_span(self):
        animallifespan = self.life_span_entry.get()
        animal_lifespan_search_query = """ (SELECT ACommonName FROM Animal WHERE LifeSpan = %s); """

        if animallifespan:
                mycursor = self.connection.cursor()
                vals = (self.life_span_entry.get(),) 
                mycursor.execute(animal_lifespan_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                animals_common_names = [result[0] for result in results]

                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root , variable=self.entity_var , values=animals_common_names, command = self.send_animal_to_print_cname) 
                self.dropdownEntity.pack() 

                self.life_span_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def find_speciesname_by_cname(self, commonname):
        animal_sname_search_query = """ (SELECT ASpeciesName FROM Animal WHERE ACommonName = %s); """

        mycursor = self.connection.cursor()
        vals = (commonname, ) 
        mycursor.execute(animal_sname_search_query, vals)
        results = mycursor.fetchall()
        mycursor.close()
        animals_scientific_names = [result[0] for result in results]

        self.entity_var = StringVar(self.root)
        self.dropdownEntity = OptionMenu(self.root , self.entity_var , animals_scientific_names, command = self.send_animal_to_print_cname) 
        self.dropdownEntity.pack() 

    def send_animal_to_print_cname(self, selected_value):
        animal_search_query = """ SELECT * FROM Animal WHERE ASpeciesName = %s """
        
        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(animal_search_query, vals)
        animal_vals = mycursor.fetchall()
        mycursor.close()
        printing_animal_window = ctk.CTkToplevel(self.root)
        print_animal_app = display_advanced.Display_Page(printing_animal_window, *animal_vals, "Animal")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_ANIMAL_SNAME:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Animal Scientific Name Search")
        self.root.geometry("500x900")

        self.class_label = ctk.CTkLabel(root, text="Searching for an Animal by it's scientific name")
        self.class_label.pack(pady=20)

        self.sname_label = ctk.CTkLabel(root, text="Enter the Animal's Scientific Name:")
        self.sname_label.pack(pady=5)
        self.sname_entry = ctk.CTkEntry(root)
        self.sname_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Animal", command=self.send_sname_to_print)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def send_sname_to_print(self):
        animalsname = self.sname_entry.get()
        animal_sname_search_query = """ SELECT * FROM Animal WHERE ASpeciesName = %s """

        if animalsname:
            mycursor = self.connection.cursor()
            vals = (animalsname,) 
            mycursor.execute(animal_sname_search_query, vals)
            animal_vals = mycursor.fetchall()
            mycursor.close()
            printing_animal_window = ctk.CTkToplevel(self.root)
            print_animal_app = display_advanced.Display_Page(printing_animal_window, *animal_vals, "Animal")

            #self.sname_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_ANIMAL_CNAME:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Animal Common Name Search")
        self.root.geometry("500x900")

        self.class_label = ctk.CTkLabel(root, text="Searching for an Animal by it's common name")
        self.class_label.pack(pady=20)

        self.cname_label = ctk.CTkLabel(root, text="Enter the Animal's Common Name:")
        self.cname_label.pack(pady=5)
        self.cname_entry = ctk.CTkEntry(root)
        self.cname_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Animals", command=self.find_animals_by_cname)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_animals_by_cname(self):
        animalcname = self.cname_entry.get()
        animal_cname_search_query = """ (SELECT ASpeciesName FROM Animal WHERE ACommonName = %s); """

        if animalcname:
                mycursor = self.connection.cursor()
                vals = (self.cname_entry.get(),) 
                mycursor.execute(animal_cname_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                animals_scientific_names = [result[0] for result in results]
              
                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root , variable=self.entity_var , values=animals_scientific_names, command = self.send_animal_to_print_cname) 
                self.dropdownEntity.pack() 

                self.cname_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def send_animal_to_print_cname(self, selected_value):
        animal_search_query = """ SELECT * FROM Animal WHERE ASpeciesName = %s """
        
        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(animal_search_query, vals)
        animal_vals = mycursor.fetchall()
        mycursor.close()
        printing_animal_window = ctk.CTkToplevel(self.root)
        print_animal_app = display_advanced.Display_Page(printing_animal_window,*animal_vals, "Animal")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

###############
class PLANT_SEARCH():
    def __init__(self, root, connection):
        self.root=root
        self.connection = connection
        self.root.title("Plant Search Window")
        self.root.geometry("500x500")

        self.label = ctk.CTkLabel(root, text="Search for an Plant: ")
        self.label.pack(pady=20, padx=20)


        self.search_by_planttype_button = ctk.CTkButton(root, text="Search by Plant type", command=self.search_plant_type, state=tk.DISABLED)
        self.search_by_planttype_button.pack(pady=10)
        self.search_by_planttype_button.configure(state=tk.NORMAL)

        self.search_by_plant_commonname_button = ctk.CTkButton(root, text="Search by Plant Common Name", command=self.search_plant_commonname, state=tk.DISABLED)
        self.search_by_plant_commonname_button.pack(pady=10)
        self.search_by_plant_commonname_button.configure(state=tk.NORMAL)

        self.search_by_plant_scientific_name_button = ctk.CTkButton(root, text="Search by Plant Scientific Name", command=self.search_plant_scientificname, state=tk.DISABLED)
        self.search_by_plant_scientific_name_button.pack(pady=10)
        self.search_by_plant_scientific_name_button.configure(state=tk.NORMAL)

        self.search_by_plant_life_cycle_button = ctk.CTkButton(root, text="Search by Plant it's Life Cycle", command=self.search_plant_life_cycle, state=tk.DISABLED)
        self.search_by_plant_life_cycle_button.pack(pady=10)
        self.search_by_plant_life_cycle_button.configure(state=tk.NORMAL)

        self.search_by_plant_flowering_period_button = ctk.CTkButton(root, text="Search by Plant it's Flowering Period", command=self.search_plant_flowering_period, state=tk.DISABLED)
        self.search_by_plant_flowering_period_button.pack(pady=10)
        self.search_by_plant_flowering_period_button.configure(state=tk.NORMAL)
    
    def search_plant_type(self):
        update_search_count('plant')
        plant_type_window = ctk.CTkToplevel(self.root)
        plant_type_window.focus()
        plant_type_app = SEARCH_PLANT_TYPE(plant_type_window, self.connection)

    def search_plant_commonname(self):
        update_search_count('plant')
        plant_cname_window = ctk.CTkToplevel(self.root)
        plant_cname_window.focus()
        plant_cname_app = SEARCH_PLANT_CNAME(plant_cname_window, self.connection)

    def search_plant_scientificname(self):
        update_search_count('plant')
        plant_sname_window = ctk.CTkToplevel(self.root)
        plant_sname_window.focus()
        plant_sname_app = SEARCH_PLANT_SNAME(plant_sname_window, self.connection)

    def search_plant_life_cycle(self):
        update_search_count('plant')
        plant_life_cycle_window = ctk.CTkToplevel(self.root)
        plant_life_cycle_window.focus()
        plant_life_cycle_app = SEARCH_PLANT_LIFE_CYCLE(plant_life_cycle_window, self.connection)

    def search_plant_flowering_period(self):
        update_search_count('plant')
        plant_flowering_period_window = ctk.CTkToplevel(self.root)
        plant_flowering_period_window.focus()
        plant_flowering_period_app = SEARCH_PLANT_FLOWERING_PERIOD(plant_flowering_period_window, self.connection)

class SEARCH_PLANT_TYPE:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Plant Type Search")
        self.root.geometry("500x500")

        self.query_label = ctk.CTkLabel(root, text="Searching for an Plant by Type")
        self.query_label.pack(pady=20)

        self.type_label = ctk.CTkLabel(root, text="Enter the Plant Type:")
        self.type_label.pack(pady=5)
        self.type_entry = ctk.CTkEntry(root)
        self.type_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Plants", command=self.find_plants_by_class)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_plants_by_class(self):
        planttype = self.type_entry.get()
        plant_type_search_query = """ (SELECT PCommonName FROM Plant WHERE PlantType = %s); """

        if planttype:
                mycursor = self.connection.cursor()
                vals = (self.type_entry.get(),) 
                mycursor.execute(plant_type_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                plants_common_names = [result[0] for result in results]

                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root , variable=self.entity_var , values=plants_common_names, command = self.find_plants_by_cname) 
                self.dropdownEntity.pack() 

                self.type_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def find_plants_by_cname(self, commonname):
        plant_cname_search_query = """ (SELECT PScientificName FROM Plant WHERE PCommonName = %s); """

        mycursor = self.connection.cursor()
        vals = (commonname,) 
        mycursor.execute(plant_cname_search_query, vals)
        results = mycursor.fetchall()
        mycursor.close()
        plants_scientific_names = [result[0] for result in results]

        self.entity_var = StringVar(self.root)
        self.dropdownEntity = ctk.CTkOptionMenu(self.root , variable=self.entity_var , values=plants_scientific_names, command = self.send_plant_to_print_cname) 
        self.dropdownEntity.pack()

    def send_plant_to_print_cname(self, selected_value):
        plant_search_query =  """SELECT * FROM Plant WHERE PScientificName = %s """

        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(plant_search_query, vals)
        plant_vals = mycursor.fetchall()
        mycursor.close()
        
        printing_plant_window = ctk.CTkToplevel(self.root)
        printing_plant_window.focus()
        print_plant_app = display_advanced.Display_Page(printing_plant_window, *plant_vals, "Plant")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_PLANT_SNAME:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Plant Scientific Name Search")
        self.root.geometry("500x900")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Plant by it's scientific name")
        self.class_label.pack(pady=20)

        self.sname_label = ctk.CTkLabel(root, text="Enter the Plant's Scientific Name:")
        self.sname_label.pack(pady=5)
        self.sname_entry = ctk.CTkEntry(root)
        self.sname_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Plant", command=self.send_plant_sname_to_print)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def send_plant_sname_to_print(self):
        plantsname = self.sname_entry.get()
        plant_sname_search_query = """ SELECT * FROM Plant WHERE PScientificName = %s """

        if plantsname:
            mycursor = self.connection.cursor()
            vals = (self.sname_entry.get(),) 
            mycursor.execute(plant_sname_search_query, vals)
            plant_vals = mycursor.fetchall()
            mycursor.close()
            printing_plant_window = ctk.CTkToplevel(self.root)
            printing_plant_window.focus()
            print_plant_app = display_advanced.Display_Page(printing_plant_window, *plant_vals, "Plant")
            self.sname_entry.delete(0, tk.END)

        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_PLANT_CNAME:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Plant Common Name Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Plant by it's common name")
        self.class_label.pack(pady=20)

        self.cname_label = ctk.CTkLabel(root, text="Enter the Plant's Common Name:")
        self.cname_label.pack(pady=5)
        self.cname_entry = ctk.CTkEntry(root)
        self.cname_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Plants:", command=self.find_plants_by_cname)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_plants_by_cname(self):
        plantcname = self.cname_entry.get()
        plant_cname_search_query = """ (SELECT PScientificName FROM Plant WHERE PCommonName = %s); """

        if plantcname:
                mycursor = self.connection.cursor()
                vals = (self.cname_entry.get(),) 
                mycursor.execute(plant_cname_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                plants_scientific_names = [result[0] for result in results]
                
                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root , variable= self.entity_var , values= plants_scientific_names, command = self.send_plant_to_print_cname) 
                self.dropdownEntity.pack() 

                self.cname_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def send_plant_to_print_cname(self, selected_value):
        plant_search_query =  """SELECT * FROM Plant WHERE PScientificName = %s """

        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(plant_search_query, vals)
        plant_vals = mycursor.fetchall()
        mycursor.close()
        
        printing_plant_window = ctk.CTkToplevel(self.root)
        printing_plant_window.focus()
        print_plant_app = display_advanced.Display_Page(printing_plant_window, *plant_vals, "Plant")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_PLANT_LIFE_CYCLE:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Plant Life Cycle Search")
        self.root.geometry("500x900")

        self.query_label = ctk.CTkLabel(root, text="Searching for an Plant by it's Life Cycle")
        self.query_label.pack(pady=20)

        self.life_cycle_label = ctk.CTkLabel(root, text="Enter the Plant's Life Cycle:")
        self.life_cycle_label.pack(pady=5)
        self.life_cycle_entry = ctk.CTkEntry(root)
        self.life_cycle_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Plants", command=self.find_plants_by_life_cycle)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_plants_by_life_cycle(self):
        plant_life_cycle = self.life_cycle_entry.get()
        plant_life_cycle_search_query = """ (SELECT PCommonName FROM Plant WHERE LifeCycle = %s); """

        if plant_life_cycle:
                mycursor = self.connection.cursor()
                vals = (self.life_cycle_entry.get(),) 
                mycursor.execute(plant_life_cycle_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                plants_common_names = [result[0] for result in results]

                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root ,variable= self.entity_var ,values=plants_common_names, command = self.find_plants_by_cname) 
                self.dropdownEntity.pack() 

                self.life_cycle_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def find_plants_by_cname(self, commonname):
        plant_cname_search_query = """ (SELECT PScientificName FROM Plant WHERE PCommonName = %s); """

        mycursor = self.connection.cursor()
        vals = (commonname,) 
        mycursor.execute(plant_cname_search_query, vals)
        results = mycursor.fetchall()
        mycursor.close()
        plants_scientific_names = [result[0] for result in results]

        self.entity_var = StringVar(self.root)
        self.dropdownEntity = ctk.CTkOptionMenu(self.root ,variable= self.entity_var , values=plants_scientific_names, command = self.send_plant_to_print_cname) 
        self.dropdownEntity.pack() 

    def send_plant_to_print_cname(self, selected_value):
        plant_search_query =  """ SELECT * FROM Plant WHERE PScientificName = %s """

        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(plant_search_query, vals)
        plant_vals = mycursor.fetchall()
        mycursor.close()
        
        printing_plant_window = ctk.CTkToplevel(self.root)
        printing_plant_window.focus()
        print_plant_app = display_advanced.Display_Page(printing_plant_window, self.connection, *plant_vals, "Plant")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_PLANT_FLOWERING_PERIOD:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Plant Flowering Period Search")
        self.root.geometry("500x500")

        self.query_label = ctk.CTkLabel(root, text="Searching for an Plant by it's Flowering Period")
        self.query_label.pack(pady=20)

        self.flowering_period_label = ctk.CTkLabel(root, text="Enter the Plant's Flowering Period:")
        self.flowering_period_label.pack(pady=5)
        self.flowering_period_entry = ctk.CTkEntry(root)
        self.flowering_period_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Plants", command=self.find_plants_by_flowering_period)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_plants_by_flowering_period(self):
        plant_flowering_period = self.flowering_period_entry.get()
        plant_flowering_period_search_query = """ (SELECT PCommonName FROM Plant WHERE FloweringPeriod = %s); """

        if plant_flowering_period:
                mycursor = self.connection.cursor()
                vals = (self.flowering_period_entry.get(),) 
                mycursor.execute(plant_flowering_period_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                plants_common_names = [result[0] for result in results]

                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root ,variable= self.entity_var ,values=plants_common_names, command = self.find_plants_by_cname) 
                self.dropdownEntity.pack() 

                self.flowering_period_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def find_plants_by_cname(self, commonname):
        plant_cname_search_query = """ (SELECT PScientificName FROM Plant WHERE PCommonName = %s); """

        mycursor = self.connection.cursor()
        vals = (commonname,) 
        mycursor.execute(plant_cname_search_query, vals)
        results = mycursor.fetchall()
        mycursor.close()
        plants_scientific_names = [result[0] for result in results]

        self.entity_var = StringVar(self.root)
        self.dropdownEntity = ctk.CTkOptionMenu(self.root , variable =self.entity_var , values=plants_scientific_names, command = self.send_plant_to_print_cname) 
        self.dropdownEntity.pack()

    def send_plant_to_print_cname(self, selected_value):
        plant_search_query =  """ SELECT * FROM Plant WHERE PScientificName = %s """

        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(plant_search_query, vals)
        plant_vals = mycursor.fetchall()
        mycursor.close()
        
        printing_plant_window = ctk.CTkToplevel(self.root)
        print_plant_app = display_advanced.Display_Page(printing_plant_window, self.connection, *plant_vals, "Plant")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

#####
class BIOME_SEARCH():
    def __init__(self, root, connection):
        self.root=root
        self.connection = connection
        self.root.title("Biome Search Window")
        self.root.geometry("500x500")

        self.label = ctk.CTkLabel(root, text="Search for an Biome:")
        self.label.pack(pady=20, padx=20)

        self.search_by_name_button = ctk.CTkButton(root, text="Search by Name", command=self.search_name, state=tk.DISABLED)
        self.search_by_name_button.pack(pady=10)
        self.search_by_name_button.configure(state=tk.NORMAL)

        self.search_by_climate_button = ctk.CTkButton(root, text="Search by Climate", command=self.search_climate, state=tk.DISABLED)
        self.search_by_climate_button.pack(pady=10)
        self.search_by_climate_button.configure(state=tk.NORMAL)

        self.search_by_temp_range_button = ctk.CTkButton(root, text="Search by Temperature Range", command=self.search_temprange, state=tk.DISABLED)
        self.search_by_temp_range_button.pack(pady=10)
        self.search_by_temp_range_button.configure(state=tk.NORMAL)

    def search_name(self):
        update_search_count('biome')
        biome_name_window = ctk.CTkToplevel(self.root)
        biome_name_window.focus()
        biome_name_app = SEARCH_BIOME_NAME(biome_name_window, self.connection)

    def search_climate(self):
        update_search_count('biome')
        biome_climate_window = ctk.CTkToplevel(self.root)
        biome_climate_window.focus()
        biome_climate_app = SEARCH_BIOME_CLIMATE(biome_climate_window, self.connection)

    def search_temprange(self):
        update_search_count('biome')
        biome_temprage_window = ctk.CTkToplevel(self.root)
        biome_temprage_window.focus()
        biome_temprange_app = SEARCH_BIOME_TEMP_RANGE(biome_temprage_window, self.connection)

class SEARCH_BIOME_NAME:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Biome Name Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Biome by it's Name")
        self.class_label.pack(pady=20)

        self.name_label = ctk.CTkLabel(root, text="Enter the Biome's Name:")
        self.name_label.pack(pady=5)
        self.name_entry = ctk.CTkEntry(root)
        self.name_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Biomes:", command=self.find_biomes_by_name)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_biomes_by_name(self):
        biomename = self.name_entry.get()
        biome_name_search_query = """ (SELECT bName FROM biome WHERE bName = %s); """

        if biomename:
                mycursor = self.connection.cursor()
                vals = (self.name_entry.get(),) 
                mycursor.execute(biome_name_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                biome_names = [result[0] for result in results]
                
                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root , variable=self.entity_var , values=biome_names, command = self.send_biome_to_print) 
                self.dropdownEntity.pack() 

                self.name_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def send_biome_to_print(self, selected_value):
        biome_search_query =  """SELECT * FROM biome WHERE bname = %s """
        
        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(biome_search_query, vals)
        biome_vals = mycursor.fetchall()
        mycursor.close()

        printing_biome_window = ctk.CTkToplevel(self.root)
        printing_biome_window.focus()
        print_biome_app = display_advanced.Display_Page(printing_biome_window, *biome_vals, "biome")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_BIOME_CLIMATE:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Biome Climate Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Biome by it's Climate")
        self.class_label.pack(pady=20)

        self.climate_label = ctk.CTkLabel(root, text="Enter the Biome's Climate:")
        self.climate_label.pack(pady=5)
        self.climate_entry = ctk.CTkEntry(root)
        self.climate_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Biomes:", command=self.find_biomes_by_climate)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_biomes_by_climate(self):
        biomeclimate = self.climate_entry.get()
        biome_climate_search_query = """ (SELECT bName FROM biome WHERE Climate = %s); """

        if biomeclimate:
                mycursor = self.connection.cursor()
                vals = (self.climate_entry.get(),) 
                mycursor.execute(biome_climate_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                biome_names = [result[0] for result in results]
                
                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root , variable=self.entity_var , values=biome_names, command = self.send_biome_to_print) 
                self.dropdownEntity.pack() 

                self.climate_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def send_biome_to_print(self, selected_value):
        biome_search_query =  """ SELECT * FROM biome WHERE bname = %s """
        
        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(biome_search_query, vals)
        biome_vals = mycursor.fetchall()
        mycursor.close()

        printing_biome_window = ctk.CTkToplevel(self.root)
        printing_biome_window.focus()
        print_biome_app = display_advanced.Display_Page(printing_biome_window, *biome_vals, "biome")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_BIOME_TEMP_RANGE:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Biome Temperature Range Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Biome by it's Temperature Range")
        self.class_label.pack(pady=20)

        self.temprange_label = ctk.CTkLabel(root, text="Enter the Biome's Temperature Range:")
        self.temprange_label.pack(pady=5)
        self.temprange_entry = ctk.CTkEntry(root)
        self.temprange_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Biomes:", command=self.find_biomes_by_temp_range)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_biomes_by_temp_range(self):
        biometemprange = self.temprange_entry.get()
        biome_temprange_search_query = """ (SELECT bName FROM biome WHERE TempRange = %s); """

        if biometemprange:
                mycursor = self.connection.cursor()
                vals = (self.temprange_entry.get(),) 
                mycursor.execute(biome_temprange_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                biome_names = [result[0] for result in results]
                
                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root , variable=self.entity_var , values =biome_names, command = self.send_biome_to_print) 
                self.dropdownEntity.pack() 

                self.temprange_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def send_biome_to_print(self, selected_value):
        biome_search_query =  """ SELECT * FROM biome WHERE bname = %s """
        
        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(biome_search_query, vals)
        biome_vals = mycursor.fetchall()
        mycursor.close()
        
        printing_biome_window = ctk.CTkToplevel(self.root)
        printing_biome_window.focus()
        print_biome_app = display_advanced.Display_Page(printing_biome_window, *biome_vals, "biome")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

###########
class HABITAT_SEARCH():
    def __init__(self, root, connection):
        self.root=root
        self.connection = connection
        self.root.title("Habitat Search Window")
        self.root.geometry("500x700")

        self.label = ctk.CTkLabel(root, text="Search for an Habitat: ")
        self.label.pack(pady=20, padx=20)

        self.search_by_hname_button = ctk.CTkButton(root, text="Search by Name", command=self.search_hname, state=tk.DISABLED)
        self.search_by_hname_button.pack(pady=10)
        self.search_by_hname_button.configure(state=tk.NORMAL)

        self.search_by_climate_button = ctk.CTkButton(root, text="Search by Climate", command=self.search_climate, state=tk.DISABLED)
        self.search_by_climate_button.pack(pady=10)
        self.search_by_climate_button.configure(state=tk.NORMAL)

        self.search_location_button = ctk.CTkButton(root, text="Search by Location", command=self.search_location, state=tk.DISABLED)
        self.search_location_button.pack(pady=10)
        self.search_location_button.configure(state=tk.NORMAL)

        self.search_by_avg_temp_button = ctk.CTkButton(root, text="Search by the Average Temperature", command=self.search_avg_temp, state=tk.DISABLED)
        self.search_by_avg_temp_button.pack(pady=10)
        self.search_by_avg_temp_button.configure(state=tk.NORMAL)

        self.search_by_avg_rain_button = ctk.CTkButton(root, text="Search by the Average Rainfall", command=self.search_avg_rainfal, state=tk.DISABLED)
        self.search_by_avg_rain_button.pack(pady=10)
        self.search_by_avg_rain_button.configure(state=tk.NORMAL)

        self.search_by_alt_range_button = ctk.CTkButton(root, text="Search by the Altitude Range", command=self.search_alt_range, state=tk.DISABLED)
        self.search_by_alt_range_button.pack(pady=10)
        self.search_by_alt_range_button.configure(state=tk.NORMAL)

        self.search_by_soil_type_button = ctk.CTkButton(root, text="Search by the Soil Type", command=self.search_soil_type, state=tk.DISABLED)
        self.search_by_soil_type_button.pack(pady=10)
        self.search_by_soil_type_button.configure(state=tk.NORMAL)

        self.search_by_protected_areas_button = ctk.CTkButton(root, text="Search by the Protected Areas", command=self.search_protected_areas, state=tk.DISABLED)
        self.search_by_protected_areas_button.pack(pady=10)
        self.search_by_protected_areas_button.configure(state=tk.NORMAL)

    def search_hname(self):
        update_search_count('habitat')
        habitat_name_window = ctk.CTkToplevel(self.root)
        habitat_name_window.focus()
        habitat_name_app = SEARCH_HABITAT_NAME(habitat_name_window, self.connection)

    def search_climate(self):
        update_search_count('habitat')
        habitat_climate_window = ctk.CTkToplevel(self.root)
        habitat_climate_window.focus()
        habitat_climate_app = SEARCH_HABITAT_CLIMATE(habitat_climate_window, self.connection)

    def search_location(self):
        update_search_count('habitat')
        habitat_loc_window = ctk.CTkToplevel(self.root)
        habitat_loc_window.focus()
        habitat_loc_app = SEARCH_HABITAT_LOCATION(habitat_loc_window, self.connection)

    def search_avg_temp(self):
        update_search_count('habitat')
        habitat_avg_temp_window = ctk.CTkToplevel(self.root)
        habitat_avg_temp_window.focus()
        habitat_avg_temp_app = SEARCH_HABITAT_AVG_TEMP(habitat_avg_temp_window, self.connection)
        
    def search_avg_rainfal(self):
        update_search_count('habitat')
        habitat_avg_rain_window = ctk.CTkToplevel(self.root)
        habitat_avg_rain_window.focus()
        abitat_avg_rain_app = SEARCH_HABITAT_AVG_RAIN(habitat_avg_rain_window, self.connection)

    def search_alt_range(self):
        update_search_count('habitat')
        habitat_alt_range_window = ctk.CTkToplevel(self.root)
        habitat_alt_range_window.focus()
        habitat_alt_range_app = SEARCH_HABITAT_ALT_RANGE(habitat_alt_range_window, self.connection)
    
    def search_soil_type(self):
        update_search_count('habitat')
        habitat_soil_types_window = ctk.CTkToplevel(self.root)
        habitat_soil_types_window.focus()
        habitat_soil_types_app = SEARCH_HABITAT_SOIL_TYPE(habitat_soil_types_window, self.connection)
        
    def search_protected_areas(self):
        update_search_count('habitat')
        habitat_protected_areas_window = ctk.CTkToplevel(self.root)
        habitat_protected_areas_window.focus()
        habitat_protected_areas_app = SEARCH_HABITAT_PROTECTED_AREAS(habitat_protected_areas_window, self.connection)

class SEARCH_HABITAT_NAME:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Habitat Name Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Habitat by it's Name")
        self.class_label.pack(pady=20)

        self.hname_label = ctk.CTkLabel(root, text="Enter the Habitat's Name:")
        self.hname_label.pack(pady=5)
        self.hname_entry = ctk.CTkEntry(root)
        self.hname_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find the Habitat:", command=self.print_habitat_by_name)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def print_habitat_by_name(self):
        habitat_name = self.hname_entry.get()
        habitat_name_search_query = """ (SELECT * FROM habitat WHERE hname = %s); """

        if habitat_name:
                mycursor = self.connection.cursor()
                vals = (self.hname_entry.get(),) 
                mycursor.execute(habitat_name_search_query, vals)
                habitat_results = mycursor.fetchall()
                mycursor.close()
                printing_habitat_window = ctk.CTkToplevel(self.root)
                printing_habitat_window.focus()
                print_habitat_app = display_advanced.Display_Page(printing_habitat_window,  *habitat_results, "habitat")

        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_HABITAT_CLIMATE:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Habitat Climate Search")
        self.root.geometry("500x900")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Habitat by it's Climate")
        self.class_label.pack(pady=20)

        self.climate_label = ctk.CTkLabel(root, text="Enter the Habitat's Climate")
        self.climate_label.pack(pady=5)
        self.climate_entry = ctk.CTkEntry(root)
        self.climate_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Habitats", command=self.find_habitats_by_climate)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_habitats_by_climate(self):
        habitatclimate = self.climate_entry.get()
        habitat_climate_search_query = """ (SELECT hname FROM habitat WHERE climate = %s); """

        if habitatclimate:
                mycursor = self.connection.cursor()
                vals = (self.climate_entry.get(),) 
                mycursor.execute(habitat_climate_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                habitat_names = [result[0] for result in results]
                
                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root ,variable= self.entity_var , values=habitat_names, command = self.send_habitat_to_print) 
                self.dropdownEntity.pack() 

                self.climate_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def send_habitat_to_print(self, selected_value):
        habitat_name_search_query = """ (SELECT * FROM habitat WHERE hname = %s); """

        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(habitat_name_search_query, vals)
        habitat_vals = mycursor.fetchall()
        mycursor.close()
        
        printing_habitat_window = ctk.CTkToplevel(self.root)
        printing_habitat_window.focus()
        print_habitat_app = display_advanced.Display_Page(printing_habitat_window, self.connection, *habitat_vals, "habitat")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_HABITAT_LOCATION:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Habitat Location Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Habitat by it's Location")
        self.class_label.pack(pady=20)

        self.location_label = ctk.CTkLabel(root, text="Enter the Habitat's Location: ")
        self.location_label.pack(pady=5)
        self.location_entry = ctk.CTkEntry(root)
        self.location_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Habitats", command=self.find_habitats_by_location)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_habitats_by_location(self):
        habitatlocaiton = self.location_entry.get()
        habitat_location_search_query = """ (SELECT hname FROM habitat WHERE location = %s); """

        if habitatlocaiton:
                mycursor = self.connection.cursor()
                vals = (self.location_entry.get(),) 
                mycursor.execute(habitat_location_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                habitat_names = [result[0] for result in results]
                
                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root ,variable= self.entity_var ,values=habitat_names, command = self.send_habitat_to_print) 
                self.dropdownEntity.pack() 

                self.location_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg_color="red")
            self.root.after(5000, self.clear_message)

    def send_habitat_to_print(self, selected_value):
        habitat_name_search_query = """ (SELECT * FROM habitat WHERE hname = %s); """

        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(habitat_name_search_query, vals)
        habitat_vals = mycursor.fetchall()
        mycursor.close()
        
        printing_habitat_window = ctk.CTkToplevel(self.root)
        printing_habitat_window.focus()
        print_habitat_app = display_advanced.Display_Page(printing_habitat_window, *habitat_vals, "habitat")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_HABITAT_AVG_TEMP:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Habitat Average Temperature Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Habitat by it's Average Temperature")
        self.class_label.pack(pady=20)

        self.avg_temp_label = ctk.CTkLabel(root, text="Enter the Habitat's Average Temperature: ")
        self.avg_temp_label.pack(pady=5)
        self.avg_temp_entry = ctk.CTkEntry(root)
        self.avg_temp_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Habitats", command=self.find_habitats_by_avg_temp)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_habitats_by_location(self):
        habitatavgtemp = self.avg_temp_entry.get()
        habitat_avg_temp_search_query = """ (SELECT hname FROM habitat WHERE avg_temp = %s); """

        if habitatavgtemp:
                mycursor = self.connection.cursor()
                vals = (self.avg_temp_entry.get(),) 
                mycursor.execute(habitat_avg_temp_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                habitat_names = [result[0] for result in results]
                
                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root ,variable= self.entity_var , values=habitat_names, command = self.send_habitat_to_print) 
                self.dropdownEntity.pack() 

                self.avg_temp_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def send_habitat_to_print(self, selected_value):
        habitat_name_search_query = """ (SELECT * FROM habitat WHERE hname = %s); """

        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(habitat_name_search_query, vals)
        habitat_vals = mycursor.fetchall()
        mycursor.close()
        
        printing_habitat_window = ctk.CTkToplevel(self.root)
        printing_habitat_window.focus()
        print_habitat_app = display_advanced.Display_Page(printing_habitat_window, *habitat_vals, "habitat")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_HABITAT_AVG_RAIN:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Habitat Average Rainfall Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Habitat by it's Average Rainfall")
        self.class_label.pack(pady=20)

        self.avg_rain_label = ctk.CTkLabel(root, text="Enter the Habitat's Average Rainfall: ")
        self.avg_rain_label.pack(pady=5)
        self.avg_rain_entry = ctk.CTkEntry(root)
        self.avg_rain_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Habitats", command=self.find_habitats_by_avg_rain)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_habitats_by_avg_rain(self):
        habitatavg_rain = self.avg_rain_entry.get()
        habitat_avg_rain_search_query = """ (SELECT hname FROM habitat WHERE avg_rain = %s); """

        if habitatavg_rain:
                mycursor = self.connection.cursor()
                vals = (self.avg_rain_entry.get(),) 
                mycursor.execute(habitat_avg_rain_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                habitat_names = [result[0] for result in results]
                
                self.entity_var = StringVar(self.root)
                self.dropdownEntity = OptionMenu(self.root ,variable= self.entity_var ,values= habitat_names, command = self.send_habitat_to_print) 
                self.dropdownEntity.pack() 

                self.avg_rain_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg_color="red")
            self.root.after(5000, self.clear_message)

    def send_habitat_to_print(self, selected_value):
        habitat_name_search_query = """ (SELECT hname, location, avg_temp, avg_rain, climate, altitude_range, protected_areas, soil_type, h_BiomeID FROM habitat WHERE hname = %s); """

        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(habitat_name_search_query, vals)
        habitat_vals = mycursor.fetchall()
        mycursor.close()
        
        printing_habitat_window = ctk.CTkToplevel(self.root)
        printing_habitat_window.focus()
        print_habitat_app = display_advanced.Display_Page(printing_habitat_window, self.connection, *habitat_vals, "habitat")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_HABITAT_ALT_RANGE:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Habitat Altitude Range Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Habitat by it's Altitude Range")
        self.class_label.pack(pady=20)

        self.alt_range_label = ctk.CTkLabel(root, text="Enter the Habitat's Altitude Range: ")
        self.alt_range_label.pack(pady=5)
        self.alt_range_entry = ctk.CTkEntry(root)
        self.alt_range_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Habitats", command=self.find_habitats_by_alt_range)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_habitats_by_alt_range(self):
        habitat_alt_range = self.alt_range_entry.get()
        habitat_alt_range_search_query = """ (SELECT hname FROM habitat WHERE altitude_range = %s); """

        if habitat_alt_range:
                mycursor = self.connection.cursor()
                vals = (self.alt_range_entry.get(),) 
                mycursor.execute(habitat_alt_range_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                habitat_names = [result[0] for result in results]
                
                self.entity_var = StringVar(self.root)
                self.dropdownEntity = OptionMenu(self.root , variable= self.entity_var , values=habitat_names, command = self.send_habitat_to_print) 
                self.dropdownEntity.pack() 

                self.alt_range_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def send_habitat_to_print(self, selected_value):
        habitat_name_search_query = """ (SELECT hname, location, avg_temp, avg_rain, climate, altitude_range, protected_areas, soil_type, h_BiomeID FROM habitat WHERE hname = %s); """

        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(habitat_name_search_query, vals)
        habitat_vals = mycursor.fetchall()
        mycursor.close()
        
        printing_habitat_window = ctk.CTkToplevel(self.root)
        print_habitat_app.focus()
        print_habitat_app = display_advanced.Display_Page(printing_habitat_window, *habitat_vals, "habitat")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_HABITAT_SOIL_TYPE:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Habitat Soil Type Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Habitat by it's Soil Type")
        self.class_label.pack(pady=20)

        self.soil_type_label = ctk.CTkLabel(root, text="Enter the Habitat's Soil Type: ")
        self.soil_type_label.pack(pady=5)
        self.soil_type_entry = ctk.CTkEntry(root)
        self.soil_type_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Habitats", command=self.find_habitats_by_soil_type)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_habitats_by_soil_type(self):
        habitat_soil_type = self.soil_type_entry.get()
        habitat_soil_type_search_query = """ (SELECT hname FROM habitat WHERE soil_type = %s); """

        if habitat_soil_type:
                mycursor = self.connection.cursor()
                vals = (self.soil_type_entry.get(),) 
                mycursor.execute(habitat_soil_type_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                habitat_names = [result[0] for result in results]
                
                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root ,variable= self.entity_var ,values= habitat_names, command = self.send_habitat_to_print) 
                self.dropdownEntity.pack() 

                self.soil_type_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg_color="red")
            self.root.after(5000, self.clear_message)

    def send_habitat_to_print(self, selected_value):
        habitat_name_search_query = """ (SELECT * FROM habitat WHERE hname = %s); """

        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(habitat_name_search_query, vals)
        habitat_vals = mycursor.fetchall()
        mycursor.close()
        
        printing_habitat_window = ctk.CTkToplevel(self.root)
        print_habitat_app.focus()
        print_habitat_app = display_advanced.Display_Page(printing_habitat_window, *habitat_vals, "habitat")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_HABITAT_PROTECTED_AREAS:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Habitat Protected Areas Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Habitat by it's Protected Areas")
        self.class_label.pack(pady=20)

        self.p_areas_label = ctk.CTkLabel(root, text="Enter the Habitat's Protected Areas: ")
        self.p_areas_label.pack(pady=5)
        self.p_areas_entry = ctk.CTkEntry(root)
        self.p_areas_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Habitats", command=self.find_habitats_by_p_areas)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_habitats_by_p_areas(self):
        habitat_p_areas = self.p_areas_entry.get()
        habitat_p_areas_search_query = """ (SELECT hname FROM habitat WHERE protected_areas = %s); """

        if habitat_p_areas:
                mycursor = self.connection.cursor()
                vals = (self.p_areas_entry.get(),) 
                mycursor.execute(habitat_p_areas_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                habitat_names = [result[0] for result in results]
                
                self.entity_var = StringVar(self.root)
                self.dropdownEntity = OptionMenu(self.root ,variable= self.entity_var ,values=habitat_names, command = self.send_habitat_to_print) 
                self.dropdownEntity.pack() 

                self.p_areas_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def send_habitat_to_print(self, selected_value):
        habitat_name_search_query = """ (SELECT * FROM habitat WHERE hname = %s); """

        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(habitat_name_search_query, vals)
        habitat_vals = mycursor.fetchall()
        mycursor.close()
        
        printing_habitat_window = ctk.CTkToplevel(self.root)
        printing_habitat_window.focus()
        print_habitat_app = display_advanced.Display_Page(printing_habitat_window, *habitat_vals, "habitat")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

##########
class FEATURES_SEARCH():
    def __init__(self, root, connection):
        self.root=root
        self.connection = connection
        self.root.title("Features Search Window")
        self.root.geometry("500x500")

        self.label = ctk.CTkLabel(root, text="Search for an Feature: ")
        self.label.pack(pady=20, padx=20)

        self.search_by_name_button = ctk.CTkButton(root, text="Search by Feature Name", command=self.search_feature_name, state=tk.DISABLED)
        self.search_by_name_button.pack(pady=10)
        self.search_by_name_button.configure(state=tk.NORMAL)

        self.search_by_local_materials_button = ctk.CTkButton(root, text="Search by Local Materials", command=self.search_local_materials, state=tk.DISABLED)
        self.search_by_local_materials_button.pack(pady=10)
        self.search_by_local_materials_button.configure(state=tk.NORMAL)

        self.search_by_terrain_button = ctk.CTkButton(root, text="Search by Terrain", command=self.search_terrain, state=tk.DISABLED)
        self.search_by_terrain_button.pack(pady=10)
        self.search_by_terrain_button.configure(state=tk.NORMAL)

        self.search_by_water_features_button = ctk.CTkButton(root, text="Search by Water Features", command=self.search_water_features, state=tk.DISABLED)
        self.search_by_water_features_button.pack(pady=10)
        self.search_by_water_features_button.configure(state=tk.NORMAL)


    def search_feature_name(self):
        update_search_count('feature')
        features_name_window = ctk.CTkToplevel(self.root)
        features_name_window.focus()
        features_name_app = SEARCH_FEATURES_NAME(features_name_window, self.connection)

    def search_local_materials(self):
        update_search_count('feature')
        features_local_materials_window = ctk.CTkToplevel(self.root)
        features_local_materials_window.focus()
        features_local_materials_app = SEARCH_FEATURES_LOCAL_MATERIAL(features_local_materials_window, self.connection)

    def search_terrain(self):
        update_search_count('feature')
        features_terrain_window = ctk.CTkToplevel(self.root)
        features_terrain_window.focus()
        features_terrain_app = SEARCH_FEATURES_TERRAIN(features_terrain_window, self.connection)

    def search_water_features(self):
        update_search_count('feature')
        features_water_features_window = ctk.CTkToplevel(self.root)
        features_water_features_window.focus()
        features_water_features_app = SEARCH_FEATURES_WATER_FEATURES(features_water_features_window, self.connection)

class SEARCH_FEATURES_NAME:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Feature's Name Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Feature by it's name")
        self.class_label.pack(pady=20)

        self.name_label = ctk.CTkLabel(root, text="Enter the Feature's Name:")
        self.name_label.pack(pady=5)
        self.name_entry = ctk.CTkEntry(root)
        self.name_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Feature:", command=self.send_features_to_print)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def send_features_to_print(self):
        featureslocalmaterial = self.name_entry.get()
        feature_search_query =  """SELECT * FROM feature WHERE fname = %s """

        if featureslocalmaterial:
                mycursor = self.connection.cursor()
                vals = (featureslocalmaterial,) 
                mycursor.execute(feature_search_query, vals)
                feature_vals = mycursor.fetchall()
                mycursor.close()
                
                printing_feature_window = ctk.CTkToplevel(self.root)
                printing_feature_window.focus()
                print_feature_app = display_advanced.Display_Page(printing_feature_window, *feature_vals, "feature")
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_FEATURES_LOCAL_MATERIAL:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Features local materials Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Feature by it's Local Materials")
        self.class_label.pack(pady=20)

        self.lmaterial_label = ctk.CTkLabel(root, text="Enter the Feature's Local Material:")
        self.lmaterial_label.pack(pady=5)
        self.lmaterial_entry = ctk.CTkEntry(root)
        self.lmaterial_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Features:", command=self.find_features_by_local_materials)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_features_by_local_materials(self):
        featureslocalmaterial = self.lmaterial_entry.get()
        features_local_materials_search_query = """ (SELECT fname FROM feature WHERE Local_Materials = %s); """

        if featureslocalmaterial:
                mycursor = self.connection.cursor()
                vals = (self.lmaterial_entry.get(),) 
                mycursor.execute(features_local_materials_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                features_names = [result[0] for result in results]
                
                self.entity_var = StringVar(self.root)
                self.dropdownEntity = ctk.CTkOptionMenu(self.root ,variable= self.entity_var ,values=features_names, command = self.send_features_to_print) 
                self.dropdownEntity.pack() 

                self.lmaterial_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg_color="red")
            self.root.after(5000, self.clear_message)

    def send_features_to_print(self, selected_value):
        feature_search_query =   """ fname, Local_Materials, Terrain, Water_Feature FROM feature WHERE fname = %s """
        
        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(feature_search_query, vals)
        feature_vals = mycursor.fetchall()
        mycursor.close()
        
        printing_feature_window = ctk.CTkToplevel(self.root)
        printing_feature_window.focus()
        print_feature_app = display_advanced.Display_Page(printing_feature_window, *feature_vals, "feature")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_FEATURES_TERRAIN:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Feature's Terrain Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Feature by it's Terrain")
        self.class_label.pack(pady=20)

        self.terrain_label = ctk.CTkLabel(root, text="Enter the Feature's Terrain:")
        self.terrain_label.pack(pady=5)
        self.terrain_entry = ctk.CTkEntry(root)
        self.terrain_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Features:", command=self.find_features_by_terrain)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_features_by_terrain(self):
        featuresterrain = self.terrain_entry.get()
        features_terrain_search_query = """ (SELECT fname FROM feature WHERE Terrain = %s); """

        if featuresterrain:
                mycursor = self.connection.cursor()
                vals = (self.terrain_entry.get(),) 
                mycursor.execute(features_terrain_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                features_names = [result[0] for result in results]
                
                self.entity_var = StringVar(self.root)
                self.dropdownEntity = OptionMenu(self.root , self.entity_var , *features_names, command = self.send_features_to_print) 
                self.dropdownEntity.pack() 

                self.terrain_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def send_features_to_print(self, selected_value):
        feature_search_query =   """SELECT * FROM feature WHERE fname = %s """
        
        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(feature_search_query, vals)
        feature_vals = mycursor.fetchall()
        mycursor.close()
        
        printing_feature_window = ctk.CTkToplevel(self.root)
        printing_feature_window.focus()
        print_feature_app = display_advanced.Display_Page(printing_feature_window, *feature_vals, "feature")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")

class SEARCH_FEATURES_WATER_FEATURES:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("Feature's Water Feature Search")
        self.root.geometry("500x500")

        self.class_label = ctk.CTkLabel(root, text="Searching for a Feature by it's Water Feature")
        self.class_label.pack(pady=20)

        self.water_feature_label = ctk.CTkLabel(root, text="Enter the Feature's Water Feature:")
        self.water_feature_label.pack(pady=5)
        self.water_feature_entry = ctk.CTkEntry(root)
        self.water_feature_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Find Features:", command=self.find_features_by_water_feature)
        self.add_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(root, text="")
        self.message_label.pack(pady=20)

    def find_features_by_water_feature(self):
        featureswater_feature = self.water_feature_entry.get()
        features_water_feature_search_query = """ (SELECT fname FROM feature WHERE Water_Feature = %s); """

        if featureswater_feature:
                mycursor = self.connection.cursor()
                vals = (self.terrain_entry.get(),) 
                mycursor.execute(features_water_feature_search_query, vals)
                results = mycursor.fetchall()
                mycursor.close()
                features_names = [result[0] for result in results]
                
                self.entity_var = StringVar(self.root)
                self.dropdownEntity = OptionMenu(self.root , self.entity_var , *features_names, command = self.send_features_to_print) 
                self.dropdownEntity.pack() 

                self.water_feature_entry.delete(0, tk.END)
        else:
            self.message_label.configure(text=f"Invalid Data input, try again", fg="red")
            self.root.after(5000, self.clear_message)

    def send_features_to_print(self, selected_value):
        feature_search_query =   """SELECT * FROM feature WHERE fname = %s """
        
        mycursor = self.connection.cursor()
        vals = (selected_value,) 
        mycursor.execute(feature_search_query, vals)
        feature_vals = mycursor.fetchall()
        mycursor.close()
        
        printing_feature_window = ctk.CTkToplevel(self.root)
        printing_feature_window
        print_feature_app = display_advanced.Display_Page(printing_feature_window, *feature_vals, "feature")
        
    def clear_message(self):
        """Clears the message from the message_label."""
        self.message_label.configure(text="")