import mysql.connector as mysql
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import customtkinter as ctk


#Biome_Delete_Query = "DELETE FROM biome WHERE bName = %s"
Delete_Query_Template = "DELETE FROM {entity} WHERE {attribute} = '{value}'"

Entity_List = ["admin", "habitat", "animal", "biome", "feature", "feature_of", "researcher", "plant"]
Biome_Attr  = ["Climate", "TempRange", "bName"]
Other_Attr  = ["Other", "Attr"]
Adm_Attr    = ["AdminID", "AdPassword","temp"]
Habi_Attr   = ["hname", "location", "avg_temp", "avg_rain", "climate", "altitude_range", "protected_areas", "soil_type", "h_BiomeID"]
Anim_Attr   = ["ACommonName", "ASpeciesName", "LifeSpan", "Size", "AnimalClass", "T_SpeciesID", "E_SpeciesID", "A_BiomeID", "A_HabitatID", "P_SpeciesID", "A_UserID", "A_AdminID"]
Feat_Attr   = ["Local_Materials", "Terrain", "Water_Feature"]
FeatOf_Attr = ["F_BiomeID", "F_FeatureID"]
Reas_Attr   = ["Password", "Name", "Qualifications", "R_AdminID"]
Pla_Attr    = ["PCommonName", "PScientificName", "LifeCycle", "PlantType", "FloweringPeriod",  "P_BiomeID", "P_HabitatID", "P_ASpeciesID", "P_UserID", "P_AdminID"]

class DELETE_APP():
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        print(self.connection)
        self.root.title("Delete Window")
        self.root.geometry(f"{450}x{350}")
        #create a label for the window
        self.label = ctk.CTkLabel(root,text= "Delete entries where:")
        self.label.grid(row=1, column=0, padx=20, pady=(20, 10),sticky="w")
        
        # datatype of menu text | STUPID ROOT
        self.entity_var = StringVar(root)
        self.attr_var = StringVar(root)  
        self.value_var = StringVar(root)

        self.dropdownEntity = ctk.CTkOptionMenu( root , variable=self.entity_var , values = Entity_List, command = self.setup_attributes) 
        self.dropdownEntity.grid(row=1, column=1, padx=20, pady=(20, 10),sticky="w")


        #self.dropdownAttribute = None
        self.dropdownAttribute = ctk.CTkOptionMenu(root, variable= self.attr_var, values=Other_Attr)
        self.dropdownAttribute.grid(row=2, column=1, padx=20, pady=(20, 10),sticky="w")


        self.entry_box = ctk.CTkEntry(root,textvariable=self.value_var)
        self.entry_box.grid(row=3, column=1, padx=20, pady=(20, 10),sticky="w")

        
        self.delete_button = ctk.CTkButton(root,text="Delete from Database", command= self.delete_func)
        self.delete_button.grid(row=4, column=1, padx=20, pady=(20, 10),sticky="ew")

    def setup_attributes(self, *args):
        # Based on the entity selected, choose the correct attributes list
        entity = self.entity_var.get()
        attributes_map = {
            "admin": Adm_Attr,
            "habitat": Habi_Attr,
            "animal": Anim_Attr,
            "biome": Biome_Attr,
            "feature": Feat_Attr,
            "feature_of": FeatOf_Attr,
            "researcher": Reas_Attr,
            "plant": Pla_Attr
        }

        # Get attributes for the selected entity, default to Other_Attr if entity not in map
        attributes = attributes_map.get(entity, Other_Attr)
        self.dropdownAttribute.configure(values = attributes)

        # Set the default attribute for both dropdowns if attributes list is not empty
        if attributes:
            self.dropdownAttribute.set(attributes[0])

    def delete_func(self, *args):
        print("Deleting inserted Query")
        entity = self.entity_var.get()
        attribute = self.attr_var.get()
        value = self.value_var.get()
        
        try:    
            mycursor = self.connection.cursor()
            delete_query = Delete_Query_Template.format(entity = entity,attribute = attribute,value= value)
            mycursor.execute(delete_query) 
            self.connection.commit()
            #print(mycursor.rowcount, "record(s) deleted")
            mycursor.close()
        
        
        except Exception as e:
            print("BAD")
            #self.message_label.config(text=f"Failed to add data: {e}", fg_color="red")
