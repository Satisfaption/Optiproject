import customtkinter as ctk

from baselayout import BaseLayout
from customtable import CustomTable
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
        self.table_data = None
        # the 4 entry fields capture user input data, so does the greening_option but with 3 limited choices
        self.greening_option = None
        self.ort_entry = None
        self.plz_entry = None
        self.street_entry = None
        # generate widgets
        self.setup_side_content()
        self.setup_table_content()
        self.setup_footer_content()

    def setup_side_content(self):
        # 7 rows, 1 for each widget. 1 column
        self.side_frame.columnconfigure(0, weight=1)
        self.side_frame.rowconfigure(0, weight=0)
        self.side_frame.rowconfigure(1, weight=1)
        self.side_frame.rowconfigure(2, weight=1)
        self.side_frame.rowconfigure(3, weight=1)
        self.side_frame.rowconfigure(4, weight=1)
        self.side_frame.rowconfigure(5, weight=1)
        self.side_frame.rowconfigure(6, weight=1)

        side_label = ctk.CTkLabel(self.side_frame, text="Such-Optionen")
        side_label.grid(row=0, column=0)
        self.street_entry = ctk.CTkEntry(self.side_frame, placeholder_text="Straße")
        self.street_entry.grid(row=1, column=0)
        self.plz_entry = ctk.CTkEntry(self.side_frame, placeholder_text="Postleitzahl")
        self.plz_entry.grid(row=2, column=0)
        self.ort_entry = ctk.CTkEntry(self.side_frame, placeholder_text="Ort")
        self.ort_entry.grid(row=3, column=0)

        side_button = ctk.CTkButton(self.side_frame, text="Suchen", command=self.populate_table)
        side_button.grid(row=4, column=0)
        options = ["Extensiv", "Intensiv", "Verkehrsdach"]
        self.greening_option = ctk.CTkOptionMenu(self.side_frame, values=options, command=self.on_greening_option_change)
        self.greening_option.set("Begrünungsart")
        self.greening_option.grid(row=5, column=0)

    def setup_table_content(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        columns = ['Name', 'Pisa', 'Begrünungsart', 'Fläche Min (m²)', 'Fläche Max (m²)', 'PLZ', 'Ort', 'Entfernung']
        widths = [120, 120, 120, 120, 120, 100, 100, 100]
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

    def populate_table(self):
        # Clear existing data
        self.custom_table.clear_table()

        street = self.street_entry.get()
        plz = self.plz_entry.get()
        town = self.ort_entry.get()
        greenings = self.greening_option.get()
        if not plz:
            self.show_warning("Es wird mindestens eine Postleitzahl benötigt um die Suche zu starten.")
            return
        query = {}
        data_all = self.db.get_table_data(query)

        self.table_data = get_filtered_data(street, plz, town, data_all)

        self.filter_table(self.table_data, greenings)

        self.update_footer()

    def filter_table(self, data, filter_option):
        self.custom_table.clear_table()
        if not filter_option or filter_option == "Begrünungsart":
            # If no greening type is selected, return all data
            for partner_id, partner_info in data.items():
                name = partner_info['Name']
                pisa = partner_info['Pisa']
                plz = partner_info['Postleitzahl']
                ort = partner_info['Ort']

                for greening_type, greening_info in partner_info['Distances'].items():
                    flache_min = greening_info['Fläche (Minimum)']
                    flache_max = greening_info['Fläche (Maximum)']
                    distance_km = greening_info['Distance_km']
                    row_data = [name, pisa, greening_type, flache_min, flache_max, plz, ort, distance_km]
                    self.custom_table.add_row(row_data)
        else:
            # Filter data based on selected greening type
            for partner_id, partner_info in data.items():
                name = partner_info['Name']
                pisa = partner_info['Pisa']
                plz = partner_info['Postleitzahl']
                ort = partner_info['Ort']

                if filter_option in partner_info['Distances']:
                    greening_info = partner_info['Distances'][filter_option]
                    flache_min = greening_info['Fläche (Minimum)']
                    flache_max = greening_info['Fläche (Maximum)']
                    distance_km = greening_info['Distance_km']
                    row_data = [name, pisa, filter_option, flache_min, flache_max, plz, ort, distance_km]
                    self.custom_table.add_row(row_data)

    def on_greening_option_change(self, selected_greening):
        if self.table_data:
            self.filter_table(self.table_data, selected_greening)

    def update_footer(self):
        # Clear existing footer data
        for widget in self.pisa_frame.winfo_children():
            widget.destroy()

            # Concatenate Pisa values separated by commas
            pisa_values = [data['Pisa'] for data in self.table_data.values() if data['Pisa'] is not None]
            pisa_text = ", ".join(pisa_values)
            self.pisa_label = ctk.CTkLabel(self.pisa_frame, text=pisa_text, justify="left", wraplength=700)
            self.pisa_label.grid(row=0, column=0)

    def copy_pisa_values(self):
        if self.pisa_label:
            pisa_text = self.pisa_label.cget("text")
            print(f"Copying to clipboard: {pisa_text}")
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
