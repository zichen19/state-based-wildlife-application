import mysql.connector as mysql

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import customtkinter as ctk

# List of entities and their attributes for the sake of the example
Entity_List = ["admin", "habitat", "animal", "biome", "feature", "feature_of", "researcher", "plant"]
Biome_Attr = ["Climate", "TempRange", "bName"]
Other_Attr = ["Other", "Attr"]
Adm_Attr = ["AdminID", "AdPassword","temp"]
Habi_Attr = ["hname", "location", "avg_temp", "avg_rain", "climate", "altitude_range", "protected_areas", "soil_type", "h_BiomeID"]
Anim_Attr = ["ACommonName", "ASpeciesName", "LifeSpan", "Size", "AnimalClass", "T_SpeciesID", "E_SpeciesID", "A_BiomeID", "A_HabitatID", "P_SpeciesID", "A_UserID", "A_AdminID"]
Feat_Attr = ["Local_Materials", "Terrain", "Water_Feature"]
FeatOf_Attr = ["F_BiomeID", "F_FeatureID"]
Reas_Attr = ["Password", "Name", "Qualifications", "R_AdminID"]
Pla_Attr = ["PCommonName", "PScientificName", "LifeCycle", "PlantType", "FloweringPeriod", 
 "P_BiomeID", "P_HabitatID", "P_ASpeciesID", "P_UserID", "P_AdminID"]
# Update query template
Update_Query_Template = "UPDATE {entity} SET {attribute} = '{new_value}' WHERE {condition_attribute} = '{condition_value}'"

class UPDATE_APP:
    def __init__(self, root, connection, user_id):
        self.root = root
        self.connection = connection
        self.root.title("Update Window")
        self.root.geometry(f"{650}x{275}")

        self.label = ctk.CTkLabel(root, text="Update entries where:")
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10),sticky="w")
        
        self.entity_var = tk.StringVar(root)
        self.attribute_var = tk.StringVar(root)
        self.new_value_var = tk.StringVar(root)
        self.condition_attribute_var = tk.StringVar(root)
        self.condition_value_var = tk.StringVar(root)

        self.dropdownEntity = ctk.CTkOptionMenu(root,  values= Entity_List, command=self.setup_attributes, variable = self.entity_var)
        self.dropdownEntity.grid(row=0, column=1, padx=20, pady=(20, 10),sticky="w")

        #self.labelCondition = ctk.CTkLabel(root, text="Condition (attribute = value):")
        self.labelCondition = ctk.CTkLabel(root, text="To :")
        self.labelCondition.grid(row=3, column=0, padx=20, pady=(20, 10),sticky="w")

        self.dropdownConditionAttribute = ctk.CTkOptionMenu(root,values='' ,variable=self.condition_attribute_var)
        self.dropdownConditionAttribute.grid(row=3, column=1, padx=20, pady=(20, 10),sticky="w")

        self.entryConditionValue = ctk.CTkEntry(root, textvariable=self.condition_value_var)
        self.entryConditionValue.grid(row=3, column=3, padx=20, pady=(20, 10),sticky="w")

        self.update_button = ctk.CTkButton(root, text="Update", command=self.update_func)
        self.update_button.grid(row=4, column=1, padx=20, pady=(20, 10),sticky="w")

        # what the data is being updated to
        self.labelCondition = ctk.CTkLabel(root, text="Where ")
        self.labelCondition.grid(row=2, column=0, padx=20, pady=(20, 10),sticky="w")

        self.dropdownAttribute = ctk.CTkOptionMenu(root, values='',variable=self.attribute_var)
        self.dropdownAttribute.grid(row=2, column=1, padx=20, pady=(20, 10),sticky="w")

        self.labelCondition = ctk.CTkLabel(root, text="Is equal to ")
        self.labelCondition.grid(row=2, column=2, padx=20, pady=(20, 10),sticky="w")

        self.entryNewValue = ctk.CTkEntry(root, textvariable=self.new_value_var)
        self.entryNewValue.grid(row=2, column=3, padx=20, pady=(20, 10),sticky="w")

        #update password
        self.user_id = user_id
        if user_id:
            self.setup_for_password_change(user_id)

    def setup_attributes(self, *args):
        # Reset the attribute and condition attribute dropdowns
        # for menu in [self.dropdownAttribute['menu'], self.dropdownConditionAttribute['menu']]:
        #     menu.delete(0, 'end')

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
        print(str(attributes))

        #for attr in attributes:
            #self.dropdownAttribute['menu'].add_command(label=attr, command=lambda value=attr: self.attribute_var.set(value))
            #self.dropdownConditionAttribute['menu'].add_command(label=attr, command=lambda value=attr: self.condition_attribute_var.set(value))
        self.dropdownAttribute.configure(values = attributes)
        self.dropdownConditionAttribute.configure(values = attributes)

        # Set the default attribute for both dropdowns if attributes list is not empty
        if attributes:
            self.attribute_var.set(attributes[0])
            self.condition_attribute_var.set(attributes[0])

    # set up password
    def setup_for_password_change(self, user_role):
        # Set parameters based on user role
        entity = "admin" if user_role == "Admin" else "researcher"
        self.entity_var.set(entity)
        
        #attribute_var
        condition_attr = "AdPassword" if user_role == "Admin" else "password"
        self.condition_attribute_var.set(condition_attr)
        self.attribute_var.set(condition_attr)
        #self.condition_value_var.set(self.user_id)

        # Create UI elements for new password entry
        #self.label = ctk.CTkLabel(self.root, text="Enter New Password:")
        self.label.configure(text = "Change Password")
        #self.new_password_entry = ctk.CTkEntry(self.root, show="*")
        #self.new_password_entry.grid(row=1, column=0, padx=20, pady=(20, 10),sticky="w")
        # Submit button
        #self.submit_button = ctk.CTkButton(self.root, text="Submit", command=self.update_password)
        #self.submit_button.grid(row=2, column=0, padx=20, pady=(20, 10),sticky="w")

    def update_password(self):
        new_password = self.new_value_var.get()
        #hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        # Construct and execute the SQL UPDATE query
        update_query = self.Update_Query_Template.format(
            entity=self.entity_var.get(),
            attribute=self.attribute_var.get(),
            new_value=new_password,
            condition_attribute=self.condition_attribute_var.get(),
            condition_value=self.condition_value_var.get()
        )

    def update_func(self, *args):
        entity = self.entity_var.get()
        attribute = self.attribute_var.get()
        new_value = self.new_value_var.get()
        condition_attribute = self.condition_attribute_var.get()
        condition_value = self.condition_value_var.get()

        if entity and attribute and new_value and condition_attribute and condition_value:
            update_query = Update_Query_Template.format(
                entity=entity,
                attribute=attribute,
                new_value=new_value,
                condition_attribute=condition_attribute,
                condition_value=condition_value
            )
            print(update_query)

            # Connect to your test database
            mycursor = self.connection.cursor()

            try:
                mycursor.execute(update_query)
                self.connection.commit()
                messagebox.showinfo("Success", "The database has been updated.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update sqlite table: {e}")
                #conn.rollback()
            finally:
                # Close the cursor and connection
                mycursor.close()
                self.connection.close()
        else:
            messagebox.showerror("Error", "All fields must be filled out to update.")
