import customtkinter as ctk

from baselayout import BaseLayout
from customtable import CustomTable
from functions import get_table_data


class MainPage(BaseLayout):
    def __init__(self, parent):
        super().__init__(parent)
        auth_manager = self.master.auth_manager
        # pisa frame contains pisa label which will be a string to copy (C-15-123456)
        self.pisa_frame = None
        self.pisa_label = None
        # custom_table is a custom-made 'table' consisting of header & content frame with labels for text
        # the content will be populated by the populate_table method which produces the table_data attribute
        self.custom_table = None
        self.table_data = None
        # the 4 entry fields capture user input data, so does the greening_option but with 3 limited choices
        self.greening_option = None
        self.umkreis_entry = None
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

        options = ["Extensiv", "Intensiv", "Verkehrsdach"]
        self.greening_option = ctk.CTkOptionMenu(self.side_frame, values=options)
        self.greening_option.set("Begrünungsart")
        self.greening_option.grid(row=4, column=0)
        self.umkreis_entry = ctk.CTkEntry(self.side_frame, placeholder_text="Umkreis (km)")
        self.umkreis_entry.grid(row=5, column=0)
        side_button = ctk.CTkButton(self.side_frame, text="Suchen", command=self.populate_table)
        side_button.grid(row=6, column=0)

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
        perimeter = float(self.umkreis_entry.get())

        self.table_data = get_table_data(street, plz, town, greenings, perimeter)

        for partner_id, partner_info in self.table_data.items():
            name = partner_info['Name']
            pisa = partner_info['Pisa']
            plz = partner_info['PLZ']
            ort = partner_info['Ort']
            for greening_type, greening_info in partner_info['Distances'].items():
                flache_min = greening_info['Fläche (Minimum)']
                flache_max = greening_info['Fläche (Maximum)']
                distance_km = greening_info['Distance_km']
                row_data = [name, pisa, greening_type, flache_min, flache_max, plz, ort, distance_km]
                self.custom_table.add_row(row_data)

        self.update_footer()

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
