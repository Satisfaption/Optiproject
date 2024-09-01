import customtkinter as ctk

from baselayout import BaseLayout
from customwidgets import CustomTable, CustomEntryLabel
from functions import get_filtered_data
from database import Database


class MainPage(BaseLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.auth_manager = self.master.auth_manager
        self.db = Database(self.auth_manager.get_current_user_uri(), self.auth_manager.dbname)
        # pisa frame contains pisa label which will be a string to copy (C-15-123456)
        self.pisa_frame = None
        self.pisa_label = None
        # custom_table is a custom-made 'table' consisting of header & content frame with labels for text
        # the content will be populated by the populate_table method which produces the table_data attribute
        self.custom_table = None
        self.filtered_data = None
        # the 4 entry fields capture user input data, so does the greening_option but with 3 limited choices
        self.greening_option = None
        self.ort_entry = None
        self.plz_entry = None
        self.street_entry = None
        self.flaeche_entry = None
        # button to change DB documents only visible to authenticated users
        self.db_button = None
        # generate widgets
        self.setup_side_content()
        self.setup_table_content()
        self.setup_footer_content()
        #self.setup_header_content()
        #self.update_button_visibility()

    def setup_side_content(self):
        # 7 rows, 1 for each widget. 1 column
        self.side_frame.columnconfigure(0, weight=1)
        self.side_frame.rowconfigure(0, weight=1)
        self.side_frame.rowconfigure(1, weight=1)
        self.side_frame.rowconfigure(2, weight=1)
        self.side_frame.rowconfigure(3, weight=1)
        self.side_frame.rowconfigure(4, weight=1)
        self.side_frame.rowconfigure(5, weight=1)
        self.side_frame.rowconfigure(6, weight=1)
        self.side_frame.rowconfigure(7, weight=1)
        self.side_frame.rowconfigure(8, weight=1)

        side_label = ctk.CTkLabel(self.side_frame, text="Such-Optionen")
        side_label.grid(row=0, column=0)
        self.street_entry = CustomEntryLabel(self.side_frame, placeholder_text="Straße")
        self.street_entry.grid(row=3, column=0)
        self.plz_entry = CustomEntryLabel(self.side_frame, placeholder_text="Postleitzahl")
        self.plz_entry.grid(row=1, column=0)
        self.ort_entry = CustomEntryLabel(self.side_frame, placeholder_text="Ort")
        self.ort_entry.grid(row=4, column=0)
        self.flaeche_entry = CustomEntryLabel(self.side_frame, placeholder_text="Fläche")
        self.flaeche_entry.grid(row=2, column=0)

        collection = ["Partner", "Dachdecker", "Handel"]
        self.greening_option = ctk.CTkOptionMenu(self.side_frame, values=collection)  # command later
        self.greening_option.grid(row=5, column=0)
        options = ["Extensiv", "Intensiv", "Verkehrsdach"]
        self.greening_option = ctk.CTkOptionMenu(self.side_frame, values=options)
        self.greening_option.grid(row=6, column=0)

        side_button = ctk.CTkButton(self.side_frame, text="Suchen", command=self.populate_table)
        side_button.grid(row=7, column=0)

    def setup_table_content(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        columns = ['Name', 'Pisa', 'Gebietsleiter', 'PLZ', 'Ort', 'Entfernung']
        widths = [300, 120, 160, 60, 160, 100]
        self.custom_table = CustomTable(self.main_frame, columns, widths)
        self.custom_table.grid(row=0, column=0, padx=5, pady=5, sticky='nesw')

    def setup_footer_content(self):
        self.pisa_frame = ctk.CTkFrame(self.footer_frame, border_width=4, border_color='black', fg_color='#c8f7be')
        self.pisa_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.pisa_frame.columnconfigure(0, weight=1)
        self.pisa_frame.rowconfigure(0, weight=1)

        footer_label = ctk.CTkLabel(self.pisa_frame, text="Pisa Werte landen hier")
        footer_label.grid(row=0, column=0)
        pisa_button = ctk.CTkButton(self.footer_frame, text="Pisa Werte kopieren", command=self.copy_pisa_values)
        pisa_button.grid(row=0, column=1)

    """def setup_header_content(self):
        #self.header_frame.columnconfigure(0, weight=1)
        #self.header_frame.rowconfigure(0, weight=1)
        self.db_button = ctk.CTkButton(self.header_frame, text="Datenbank anpassen", command=self.update_db)
        self.db_button.grid(row=0, column=1)"""

    def populate_table(self):
        # Clear existing data
        self.custom_table.clear_table()

        street = self.street_entry.get()
        plz = self.plz_entry.get()
        town = self.ort_entry.get()
        flaeche = self.flaeche_entry.get()
        greening_selection = self.greening_option.get()
        if not plz:
            self.show_warning("Es wird mindestens eine Postleitzahl benötigt um die Suche zu starten.")
            return

        if flaeche:
            try:
                flaeche = int(flaeche)  # Convert area to integer
            except ValueError:
                self.show_warning("Der Bereich muss eine Ganzzahl sein.")
                return
        else:
            flaeche = None  # to do if fläche = leer

        query = {}
        data_all = self.db.get_table_data(query)

        self.filtered_data = get_filtered_data(street, plz, town, flaeche, data_all, greening_selection)

        for partner_id, partner_info in self.filtered_data.items():
            name = partner_info['Name']
            pisa = partner_info['Pisa']
            plz = partner_info['Postleitzahl']
            ort = partner_info['Ort']
            gl = partner_info['Gebietsleiter']

            # If no greening type is selected or all types are selected, add all distances
            if not greening_selection or greening_selection == "Begrünungsart":
                for greening_type, greening_info in partner_info['Distances'].items():
                    distance_km = greening_info['Distance_km']
                    row_data = [name, pisa, gl, plz, ort, distance_km]
                    self.custom_table.add_row(row_data)
            else:
                # If a specific greening type is selected, only add data for that type
                if greening_selection in partner_info['Distances']:
                    greening_info = partner_info['Distances'][greening_selection]
                    distance_km = greening_info['Distance_km']
                    row_data = [name, pisa, gl, plz, ort, distance_km]
                    self.custom_table.add_row(row_data)

            # Update footer with the final filtered data

        self.update_footer(self.filtered_data)

    def update_footer(self, filtered_data):
        # Clear existing footer data
        for widget in self.pisa_frame.winfo_children():
            widget.destroy()

            # Concatenate Pisa values separated by commas
            pisa_values = [data['Pisa'] for data in filtered_data.values() if data['Pisa'] is not None]
            pisa_text = " | ".join(pisa_values)
            self.pisa_label = ctk.CTkLabel(self.pisa_frame, text=pisa_text, justify="left", wraplength=700)
            self.pisa_label.grid(row=0, column=0)

    def copy_pisa_values(self):
        if self.pisa_label:
            pisa_text = self.pisa_label.cget("text")
            # Copy the text from the footer_label to the clipboard
            self.master.clipboard_clear()
            self.master.clipboard_append(self.pisa_label.cget("text"))
            self.master.update()  # Now it stays on the clipboard after the window is closed

    def show_warning(self, message):
        warning_popup = ctk.CTkToplevel(self)
        warning_popup.title("Warnung")

        # Center the popup on the screen
        window_width = 300
        window_height = 120
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        warning_popup.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        # Make the popup modal and always on top
        warning_popup.transient(self)
        warning_popup.grab_set()

        warning_label = ctk.CTkLabel(warning_popup, text=message, wraplength=250)
        warning_label.pack(padx=20, pady=20)

        ok_button = ctk.CTkButton(warning_popup, text="OK", command=warning_popup.destroy)
        ok_button.pack(pady=(0, 10))

        # Ensure the popup is closed properly
        warning_popup.protocol("WM_DELETE_WINDOW", warning_popup.destroy)

    def update_db(self):
        self.db.update_documents()

    '''def update_button_visibility(self):
        if self.auth_manager.get_current_user() == 'Guest':
            self.db_button.grid_forget()  # Hide the button
        else:
            self.db_button.grid()  # Show the button'''