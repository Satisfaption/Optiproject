import customtkinter as ctk

from baselayout import BaseLayout
from customwidgets import CustomTable, CustomEntryLabel, AutocompleteEntry
from database import Database
from functions import get_coordinates


class PartnerPage(BaseLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.side_kundennummer_entry = None
        self.sidecontent_frame = None
        self.auth_manager = self.master.auth_manager
        self.db = Database(self.auth_manager.get_current_user_uri(), self.auth_manager.dbname)
        self.table_data = None
        self.delete_button = None
        self.autocomplete_entry = None
        self.custom_table = None
        self.display_button = None
        self.popup = None
        self.content_frame = None
        self.add_row_button = None
        self.pdd_entry = None
        self.town_entry = None
        self.plz_entry = None
        self.street_entry = None
        self.gl_entry = None
        self.pisa_entry = None
        self.kundennummer_entry = None
        self.name_entry = None
        self.button_press_count = 0
        self.greening_entries = []
        # generate widgets
        self.setup_side_content()

    def setup_side_content(self):
        # 4 rows, 1 for each widget. 1 column
        self.side_frame.columnconfigure(0, weight=1)
        self.side_frame.rowconfigure(0, weight=1)
        self.side_frame.rowconfigure(1, weight=4)
        self.side_frame.rowconfigure(2, weight=1)
        self.side_frame.rowconfigure(3, weight=1)
        self.side_frame.rowconfigure(4, weight=1)

        side_label = ctk.CTkLabel(self.side_frame, text="Partner-Optionen")
        side_label.grid(row=0, column=0)

        create_button = ctk.CTkButton(self.side_frame, text="Hinzufügen", command=self.setup_create_partner)
        create_button.grid(row=2, column=0, sticky='s')

        edit_button = ctk.CTkButton(self.side_frame, text="Bearbeiten", command=self.setup_edit_partner)
        edit_button.grid(row=3, column=0)

        delete_button = ctk.CTkButton(self.side_frame, text="Entfernen", command=self.setup_delete_partner)
        delete_button.grid(row=4, column=0, sticky='n')

    def setup_create_partner(self):
        # Clear any existing widgets
        for widget in self.main_frame.winfo_children():
            widget.grid_forget()

        # Reset state variables
        self.greening_entries = []
        self.button_press_count = 0

        self.reset_frame_configuration()
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # create content frame and set config
        self.content_frame = ctk.CTkFrame(self.main_frame, border_width=4, border_color='black', fg_color='#c8f7be')
        self.content_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.content_frame.propagate(False)
        self.content_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')
        self.content_frame.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='b')

        self.name_entry = CustomEntryLabel(self.content_frame, placeholder_text="Name")
        self.name_entry.grid(row=0, column=1)

        self.kundennummer_entry = CustomEntryLabel(self.content_frame, placeholder_text="Kundennummer")
        self.kundennummer_entry.grid(row=0, column=2)

        self.pisa_entry = CustomEntryLabel(self.content_frame, placeholder_text="Pisa")
        self.pisa_entry.grid(row=0, column=3)

        self.gl_entry = CustomEntryLabel(self.content_frame, placeholder_text="Gebietsleiter")
        self.gl_entry.grid(row=0, column=4)

        self.street_entry = CustomEntryLabel(self.content_frame, placeholder_text="Straße")
        self.street_entry.grid(row=1, column=1)

        self.plz_entry = CustomEntryLabel(self.content_frame, placeholder_text="Postleitzahl")
        self.plz_entry.grid(row=1, column=2)

        self.town_entry = CustomEntryLabel(self.content_frame, placeholder_text="Ort")
        self.town_entry.grid(row=1, column=3)

        self.pdd_entry = CustomEntryLabel(self.content_frame, placeholder_text="Präferierter DD")
        self.pdd_entry.grid(row=1, column=4)

        self.add_row_button = ctk.CTkButton(self.content_frame, text="+", command=self.add_greening_row)
        self.add_row_button.grid(row=2, column=0)

        greening_entry = CustomEntryLabel(self.content_frame, placeholder_text="Begrünungsart")
        greening_entry.grid(row=2, column=1)

        area_min_entry = CustomEntryLabel(self.content_frame, placeholder_text="Fläche (Minimum)")
        area_min_entry.grid(row=2, column=2)

        area_max_entry = CustomEntryLabel(self.content_frame, placeholder_text="Fläche (Maximum)")
        area_max_entry.grid(row=2, column=3)

        range_entry = CustomEntryLabel(self.content_frame, placeholder_text="Entfernung")
        range_entry.grid(row=2, column=4)

        self.greening_entries.append({
            'Begrünungsart': greening_entry,
            'Fläche (Minimum)': area_min_entry,
            'Fläche (Maximum)': area_max_entry,
            'Entfernung': range_entry
        })

        ctk.CTkButton(self.content_frame, text="Speichern", command=self.save_partner).grid(row=5, column=0)

    def add_greening_row(self):
        row_index = len(self.greening_entries) + 2  # Start adding from row 3

        # Add button to add more rows
        if hasattr(self, 'add_row_button'):
            # Move the existing button to the new row
            self.add_row_button.grid_forget()
            self.add_row_button.grid(row=row_index, column=0)
        else:
            self.add_row_button = ctk.CTkButton(self.content_frame, text="+", command=self.add_greening_row)
            self.add_row_button.grid(row=row_index, column=0)

        greening_entry = CustomEntryLabel(self.content_frame, placeholder_text="Begrünungsart")
        greening_entry.grid(row=row_index, column=1)

        area_min_entry = CustomEntryLabel(self.content_frame, placeholder_text="Fläche (Minimum)")
        area_min_entry.grid(row=row_index, column=2)

        area_max_entry = CustomEntryLabel(self.content_frame, placeholder_text="Fläche (Maximum)")
        area_max_entry.grid(row=row_index, column=3)

        range_entry = CustomEntryLabel(self.content_frame, placeholder_text="Entfernung")
        range_entry.grid(row=row_index, column=4)

        # Store the references to these widgets
        self.greening_entries.append({
            'Begrünungsart': greening_entry,
            'Fläche (Minimum)': area_min_entry,
            'Fläche (Maximum)': area_max_entry,
            'Entfernung': range_entry
        })

        self.button_press_count += 1
        if self.button_press_count >= 2:
            self.add_row_button.configure(state='disabled')

    def save_partner(self):
        # Validation of mandatory fields
        name = self.name_entry.get()
        kundennummer = self.convert_to_int(self.kundennummer_entry.get())
        plz = self.convert_to_int(self.plz_entry.get())

        if not name or not kundennummer or not plz:
            self.show_warning("Name, Kundennummer und PLZ sind erforderliche Felder.")
            return

        # Save customer details to the database
        customer_data = {
            'Name': self.name_entry.get(),
            'Kundennummer': self.convert_to_int(self.kundennummer_entry.get()),
            'Pisa': self.pisa_entry.get(),
            'Straße': self.street_entry.get(),
            'Postleitzahl': self.convert_to_int(self.plz_entry.get()),
            'Ort': self.town_entry.get(),
            'Gebietsleiter': self.gl_entry.get(),
            'Präferierter DD': self.pdd_entry.get(),
            'Begrünungsart': {}
        }

        # get the coordinates
        latitude, longitude = get_coordinates(customer_data['Straße'], customer_data['Postleitzahl'],
                                              customer_data['Ort'])
        customer_data['Latitude'] = latitude
        customer_data['Longitude'] = longitude

        # collect greening details
        for entry_set in self.greening_entries:
            greening = entry_set['Begrünungsart'].get()
            if greening:
                area_min = entry_set['Fläche (Minimum)'].get()
                area_max = entry_set['Fläche (Maximum)'].get()
                range_val = entry_set['Entfernung'].get()

                customer_data['Begrünungsart'][greening] = {
                    'Fläche (Minimum)': float(area_min) if area_min else None,
                    'Fläche (Maximum)': float(area_max) if area_max else None,
                    'Entfernung': float(range_val) if range_val else None
                }

        # save to database
        self.db.save_customer(customer_data)

        try:
            # Validate and save the data here
            # If successful:
            self.show_popup("Daten erfolgreich gespeichert.")
        except Exception as e:
            # If there is an error, show the error message
            self.show_popup(f"Error saving data: {str(e)}", title="Error")

    def convert_to_int(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    def show_popup(self, message, title="Notification"):
        self.popup = ctk.CTkToplevel(self.content_frame)
        self.popup.title(title)
        width = 300
        height = 150

        # Center popup on screen
        screen_width = self.popup.winfo_screenwidth()
        screen_height = self.popup.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.popup.geometry(f"{width}x{height}+{x}+{y}")

        self.popup.transient(self.content_frame)
        self.popup.grab_set()
        self.popup.focus_set()

        label = ctk.CTkLabel(self.popup, text=message)
        label.pack(pady=20)

        button = ctk.CTkButton(self.popup, text="OK", command=self.double_callback)
        button.pack(pady=10)

        self.popup.protocol("WM_DELETE_WINDOW", self.double_callback)

    def setup_edit_partner(self):
        # Clear any existing widgets
        for widget in self.main_frame.winfo_children():
            widget.grid_forget()

        self.reset_frame_configuration()
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=10)
        self.main_frame.rowconfigure(0, weight=1)

        # create content frame and set config
        self.sidecontent_frame = ctk.CTkFrame(self.main_frame, border_width=4, border_color='black', fg_color='#c8f7be')
        self.sidecontent_frame.grid(row=0, column=0, sticky='nsew', padx=3, pady=5)
        self.sidecontent_frame.propagate(False)
        self.sidecontent_frame.rowconfigure((0, 1, 2), weight=1, uniform='a')
        self.sidecontent_frame.rowconfigure(3, weight=4, uniform='a')
        self.sidecontent_frame.columnconfigure(0, weight=1, uniform='b')

        self.autocomplete_entry = AutocompleteEntry(self.sidecontent_frame, auth_manager=self.auth_manager,
                                                    placeholder_text='Name')
        self.autocomplete_entry.grid(row=0, column=0, sticky="s")

        self.side_kundennummer_entry = ctk.CTkEntry(self.sidecontent_frame, placeholder_text="Kundennummer")
        self.side_kundennummer_entry.grid(row=1, column=0)

        self.display_button = ctk.CTkButton(self.sidecontent_frame, text="Suchen", command=self.search_partner)
        self.display_button.grid(row=2, column=0, sticky="n")

    def search_partner(self):
        name_value = self.autocomplete_entry.get()
        kundennummer_value = self.side_kundennummer_entry.get()

        # Determine the query based on the input values
        if name_value and kundennummer_value:
            query = {'$and': [{'Name': name_value}, {'Kundennummer': int(kundennummer_value)}]}
        elif name_value:
            query = {'Name': name_value}
        elif kundennummer_value:
            query = {'Kundennummer': int(kundennummer_value)}
        else:
            # Neither field has a value, show a warning to the user
            self.show_warning("Es wird mindestens eines der beiden Felder benötigt.")
            return None

        # Example query: search by name or Kundennummer
        partner = self.db.find_partner(query)

        if partner:
            self.populate_edit_fields(partner)
        else:
            self.show_warning("Kein Partner mit diesen Angaben vorhanden.")

    def populate_edit_fields(self, partner):
        # create content frame and set config
        self.content_frame = ctk.CTkFrame(self.main_frame, border_width=4, border_color='black', fg_color='#c8f7be')
        self.content_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        self.content_frame.propagate(False)
        self.content_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')
        self.content_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='b')

        # entry fields with pre-filled values or placeholder text
        self.name_entry = CustomEntryLabel(self.content_frame, placeholder_text="Name")
        name = partner.get('Name', '')
        if name:
            self.name_entry.insert(0, name)
        self.name_entry.grid(row=1, column=0)

        self.kundennummer_entry = CustomEntryLabel(self.content_frame, placeholder_text="Kundennummer")
        kundennummer = partner.get('Kundennummer', '')
        if kundennummer:
            self.kundennummer_entry.insert(0, kundennummer)
        self.kundennummer_entry.grid(row=1, column=1)

        self.pisa_entry = CustomEntryLabel(self.content_frame, placeholder_text="Pisa")
        pisa = partner.get('Pisa', '')
        if pisa:
            self.pisa_entry.insert(0, pisa)
        self.pisa_entry.grid(row=1, column=2)

        self.gl_entry = CustomEntryLabel(self.content_frame, placeholder_text="Gebietsleiter")
        gl = partner.get('Gebietsleiter', '')
        if gl:
            self.gl_entry.insert(0, gl)
        self.gl_entry.grid(row=1, column=3)

        self.street_entry = CustomEntryLabel(self.content_frame, placeholder_text="Straße")
        street = partner.get('Straße', '')
        if street:
            self.street_entry.insert(0, street)
        self.street_entry.grid(row=2, column=0)

        self.plz_entry = CustomEntryLabel(self.content_frame, placeholder_text="Postleitzahl")
        plz = partner.get('Postleitzahl', '')
        if plz:
            self.plz_entry.insert(0, plz)
        self.plz_entry.grid(row=2, column=1)

        self.town_entry = CustomEntryLabel(self.content_frame, placeholder_text="Ort")
        town = partner.get('Ort', '')
        if town:
            self.town_entry.insert(0, town)
        self.town_entry.grid(row=2, column=2)

        self.pdd_entry = CustomEntryLabel(self.content_frame, placeholder_text="Präferierter DD")
        pdd = partner.get('Präferierter DD', '')
        if pdd:
            self.pdd_entry.insert(0, pdd)
        self.pdd_entry.grid(row=2, column=3)

        begrünungsart_data = partner.get('Begrünungsart', {})

        # iterate over the data and populate the entry widgets
        row_index = 3  # Start adding from row 3
        for begrünungsart, data in begrünungsart_data.items():
            greening_entry = CustomEntryLabel(self.content_frame, placeholder_text="Begrünungsart")
            if begrünungsart:
                greening_entry.insert(0, begrünungsart)
            greening_entry.grid(row=row_index, column=0)

            area_min_entry = CustomEntryLabel(self.content_frame, placeholder_text="Fläche (Minimum)")
            area_min = data.get('Fläche (Minimum)', '')
            if area_min:
                area_min_entry.insert(0, area_min)
            area_min_entry.grid(row=row_index, column=1)

            area_max_entry = CustomEntryLabel(self.content_frame, placeholder_text="Fläche (Maximum)")
            area_max = data.get('Fläche (Maximum)', '')
            if area_max:
                area_max_entry.insert(0, area_max)
            area_max_entry.grid(row=row_index, column=2)

            range_entry = CustomEntryLabel(self.content_frame, placeholder_text="Entfernung")
            range = data.get('Entfernung', '')
            if range:
                range_entry.insert(0, data.get('Entfernung', ''))
            range_entry.grid(row=row_index, column=3)

            row_index += 1

            self.greening_entries.append({
                'Begrünungsart': greening_entry,
                'Fläche (Minimum)': area_min_entry,
                'Fläche (Maximum)': area_max_entry,
                'Entfernung': range_entry
            })

        # Create a button to save the edited partner
        save_button = ctk.CTkButton(self.content_frame, text="Speichern", command=self.save_partner)
        save_button.grid(row=6, column=0, pady=10)

    def setup_delete_partner(self):
        # Clear any existing widgets
        for widget in self.main_frame.winfo_children():
            widget.grid_forget()

        self.reset_frame_configuration()
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=10)
        self.main_frame.rowconfigure(0, weight=1)

        # create content frame and set config
        self.content_frame = ctk.CTkFrame(self.main_frame, border_width=4, border_color='black', fg_color='#c8f7be')
        self.content_frame.grid(row=0, column=0, sticky='nsew', padx=3, pady=5)
        self.content_frame.propagate(False)
        self.content_frame.rowconfigure((0, 1, 2), weight=1, uniform='a')
        self.content_frame.rowconfigure(3, weight=4, uniform='a')
        self.content_frame.columnconfigure(0, weight=1, uniform='b')

        self.autocomplete_entry = AutocompleteEntry(self.content_frame, auth_manager=self.auth_manager,
                                                    placeholder_text='Name')
        self.autocomplete_entry.grid(row=0, column=0, sticky="s")

        self.kundennummer_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Kundennummer")
        self.kundennummer_entry.grid(row=1, column=0)

        self.display_button = ctk.CTkButton(self.content_frame, text="Suchen", command=self.create_table)
        self.display_button.grid(row=2, column=0, sticky="n")

        self.delete_button = ctk.CTkButton(self.content_frame, text="Löschen", command=self.delete_selection)
        self.delete_button.grid(row=3, column=0, sticky="s", pady=20)

    def double_callback(self):
        self.popup.destroy()
        #for widget in self.content_frame.winfo_children():
            #widget.grid_forget()

    def create_table(self):
        # Get values from the entry widgets
        name_value = self.autocomplete_entry.get()
        kundennummer_value = self.kundennummer_entry.get()

        # Determine the query based on the input values
        if name_value and kundennummer_value:
            query = {'$and': [{'Name': name_value}, {'Kundennummer': int(kundennummer_value)}]}
        elif name_value:
            query = {'Name': name_value}
        elif kundennummer_value:
            query = {'Kundennummer': int(kundennummer_value)}
        else:
            # Neither field has a value, show a warning to the user
            self.show_warning("Es wird mindestens eines der beiden Felder benötigt")
            return None

        self.table_data = self.db.get_table_data(query)
        columns = ['Name', 'Kundennummer', 'Straße', 'PLZ', 'Ort']
        widths = [120, 100, 120, 100, 100]
        self.custom_table = CustomTable(self.main_frame, columns, widths)
        self.custom_table.grid(row=0, column=1, rowspan=3, padx=3, pady=5, sticky='nesw')
        for kundennummer, details in self.table_data.items():
            name = details['Name']
            street = details['Straße']
            plz = details['Postleitzahl']
            ort = details['Ort']
            row_data = [name, kundennummer, street, plz, ort]
            self.custom_table.add_row(row_data)

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

    def delete_selection(self):
        if not hasattr(self, 'custom_table') or self.custom_table is None:
            self.show_warning('Keine Zeile ausgewählt die gelöscht werden soll.')
            return
        selected_rows_data = self.custom_table.get_selected_rows_data()
        if not selected_rows_data:
            self.show_warning('Keine Zeile ausgewählt die gelöscht werden soll.')
            return

        kundennummern = [row_data[1] for row_data in selected_rows_data]  # Assuming Kundennummer is the second column
        try:
            result = self.db.delete_data(kundennummern)
            if result.deleted_count > 0:
                self.custom_table.remove_selected_rows()
        except Exception as e:
            self.show_warning('Gast-Nutzer hat keine Berechtigung dafür.')
            print(f"Error deleting customers: {e}")

    def reset_frame_configuration(self):
        # Reset column and row configurations
        for i in range(self.main_frame.grid_size()[0]):
            self.main_frame.columnconfigure(i, weight=0)
        for i in range(self.main_frame.grid_size()[1]):
            self.main_frame.rowconfigure(i, weight=0)

