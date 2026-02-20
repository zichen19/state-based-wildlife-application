import tkinter as tk
import mysql.connector as mysql
import customtkinter as ctk

class Display_Page:
    """
    Parameters:
    root (tk.Tk): The root window for the tkinter application.
    data_tuple (tuple): A tuple containing the data to be displayed. Each element 
                        in the tuple corresponds to a column value in the specified table.
    table_name (str): The name of the table from which the data originates. This 
                      is used to determine how to display the data and which labels to use.
    """
    def __init__(self, root, data_tuple, table_name):
        # Initialize the tkinter window, data tuple, and table name
        self.root = root
        self.data_tuple = data_tuple
        self.table_name = table_name
        self.root.geometry("300x300")

        # Attempt to establish a database connection
        try:
            self.connection = mysql.connect(
                host='localhost',
                user='root',
                password='your_password',  # Replace with your actual password
                database='wildlife_database'
            )
        except:
            # Set connection to None if connection fails
            self.connection = None

        # Mapping table names to their respective labels
        # Used for figureing out which foreign keys need to be retrived <---------
        self.table_labels = {
            "biome": ["Climate", "Temp Range", "Biome Name"],
            "habitat": ["Habitat Name", "Location", "Avg Temperature", "Avg Rainfall", "Climate", "Altitude Range", "Protected Areas", "Soil Type", "H_BiomeID"],
            "feature": ["Local Materials", "Terrain", "Water Feature"],
            "FeatureOf": ["F_BiomeID", "F_FeatureID"],
            "researcher": ["Password", "Name", "Qualifications", "R_AdminID"],
            "Plant": ["Common Name", "Scientific Name", "Life Cycle", "Plant Type", "Flowering Period", "P_BiomeID", "P_HabitatID", "P_ASpeciesID", "P_UserID", "P_AdminID"],
            "Animal": ["Common Name", "Species Name", "Life Span", "Size", "Animal Class", "T_SpeciesID", "E_SpeciesID", "A_BiomeID", "A_HabitatID", "P_SpeciesID", "A_UserID", "A_AdminID"],
            "admin": ["Name", "Password"]
        }

        # Used for displaying on the final page <----------
        self.clean_table_labels = {
            "biome": ["Climate", "Temp Range", "Biome Name"],
            "habitat": ["Habitat Name", "Location", "Avg Temperature", "Avg Rainfall", "Climate", "Altitude Range", "Protected Areas", "Soil Type", "H_BiomeID"], # <--TODO
            "feature": ["Local Materials", "Terrain", "Water Feature"],
            "FeatureOf": ["F_BiomeID", "F_FeatureID"], # <--TODO
            "researcher": ["Password", "Name", "Qualifications", "Approved By"],
            "Plant": ["Common Name", "Scientific Name", "Life Cycle", "Plant Type", "Flowering Period", "Lives In", "Habitat", "Eaten By", "Added By", "Added By"],
            "Animal": ["Common Name", "Species Name", "Life Span", "Size", "Animal Class", "Threat", "Eats", "Lives In", "Habitat", "Eats", "Added By", "Added By"],
            "admin": ["ID", "Password","Bad","Name"]
        }

        # Set the window title
        self.root.title(f"{self.table_name.capitalize()} Details")
        self.scrollable_frame = ctk.CTkScrollableFrame(self.root)
        self.scrollable_frame.pack(pady=5, padx=10, fill='x')
        # Call the method to spawn entity information
        self.create_widgets()

    # Spawn the information into the tk.root window
    def create_widgets(self):
        labels = self.table_labels.get(self.table_name, [])
        data = self.process_foreign_keys(self.data_tuple, labels) # Convert foreign keys (the number) into corresponding name (the relevant value in the databse)
        clean_labels = self.clean_table_labels.get(self.table_name, [])

        # Loop through each label-value pair and display them in the tkinter window
        for label, value in zip(clean_labels, data):
            frame = ctk.CTkFrame(self.scrollable_frame)
            frame.pack(pady=5, padx=10, fill='x')

            ctk.CTkLabel(frame, text=label, width=20, anchor='w').pack(side='left')
            ctk.CTkLabel(frame, text=value, anchor='w').pack(side='left')

    # Go through data and convert the foreign key into relevant info
    def process_foreign_keys(self, data_tuple, labels):
        # Find indices in data tuple that are foreign keys
        foreign_key_indices = [i for i, label in enumerate(labels) if label.endswith("ID")]
        print(foreign_key_indices)
        # Convert tuple to list for indexing
        data_list = list(data_tuple)
        print(data_list)
        for index in foreign_key_indices:
            foreign_key = data_list[index]
            table_identifyer = labels[index]

            # Fetch related data for each foreign key
            related_data = self.fetch_related_data(foreign_key, table_identifyer)
            data_list[index] = related_data

        return data_list

    # Given an ID and the table to find it from 
    def fetch_related_data(self, foreign_key, table_identifyer):
        print(foreign_key, table_identifyer)

        # Get name of SQL table
        # Example: T_SpeciesID -> Animal 
        related_table = self.determine_related_table(table_identifyer)

        # Given the SQL table, get the identifyer 
        # Example: Animal -> ACommonName
        table_to_field_map = {
            "admin" : "AdminUserName",
            "Animal" : "ACommonName",
            "biome" : "bName",
            "feature" : "Terrain",
            "habitat" : "hname",
            "Plant" : "PCommonName",
            "researcher" : "RUserName"
        }
        related_field = table_to_field_map[related_table]

        # Given the SQL table, get the ID attribute
        table_to_id_map = {
            "admin" : "AdminID",
            "Animal" : "ASpeciesID",
            "biome" : "BiomeID",
            "feature" : "FeatureID",
            "habitat" : "HabitatID",
            "Plant" : "PSpeciesID",
            "researcher" : "UserId"
        }
        ID_to_look_for = table_to_id_map[related_table]
        query = f"SELECT {related_field} FROM {related_table} WHERE {ID_to_look_for} = %s"
        print(query, foreign_key)


        # Establishing a connection to the database
        if not self.connection:
            return "Not Found"

        connection = self.connection
        # Initialize the result
        result = None

        try:
            cursor = connection.cursor()
            # Executing the query
            cursor.execute(query, (foreign_key,))
            result = cursor.fetchone()

        except mysql.Error as e:
            print("Error in database connection or query execution:", e)
        
        finally:
            if cursor:
                cursor.close()

        # Return the fetched data or a default value if not found
        return result[0] if result else "Not Found"
    
    # Convert label name to correct table name
    # Example: T_SpeciesID -> Animal 
    #        (threat species ID is an entry in the Animal table)
    def determine_related_table(self, foreign_key):

        # Mapping foreign key suffixes to their corresponding table names
        fk_to_table_map = {
            "F_BiomeID" : "biome",
            "F_FeatureID" : "feature",
            "R_AdminID" : "admin",
            "P_BiomeID" : "Plant",
            "P_HabitatID" : "habitat",
            "P_ASpeciesID" : "Animal",
            "P_UserID" : "researcher",
            "T_SpeciesID" : "Animal",
            "E_SpeciesID" : "Animal",
            "A_BiomeID" : "biome",
            "A_HabitatID" : "habitat",
            "P_SpeciesID" : "Plant",
            "A_UserID" : "researcher",
            "A_AdminID" : "admin"
        }

        # Lookup the corresponding table name using the suffix
        related_table = fk_to_table_map.get(foreign_key)

        # Return the table name or None if not found
        return related_table if related_table else None




# Example usage
if __name__ == "__main__":
    
    root = tk.Tk()

    # Example tuple 
    animal_data = ("Lion", "Panthera leo", "10-14 years", "Medium", "Mammal", 
                   "001", "002", "003", "004", "005", "006", "007")

    app = Display_Page(root, animal_data, "Animal")

    root.mainloop()