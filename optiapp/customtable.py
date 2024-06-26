import customtkinter as ctk


class CustomTable(ctk.CTkFrame):
    def __init__(self, master, column_names, column_widths, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.content_frame = None
        self.column_names = column_names
        self.column_widths = column_widths
        self.columns = {}
        self.configure(fg_color='black')
        self.current_row = 1
        self.selected_rows = set()
        self.row_widgets = []

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.create_table()

    def create_table(self):
        # header frame
        header_frame = ctk.CTkFrame(self, height=30, fg_color='#b1eba4')
        header_frame.rowconfigure(0, weight=1)
        header_frame.grid(row=0, column=0, sticky="nsew", pady=5, padx=5)
        header_frame.grid_propagate(False)

        # content frame
        content_frame = ctk.CTkScrollableFrame(self, fg_color='#b1eba4', scrollbar_button_color='black')
        content_frame.grid(row=1, column=0, sticky="nsew", pady=5, padx=5)

        for col_index, (name, width) in enumerate(zip(self.column_names, self.column_widths)):
            # even spacing with same weight for each column
            header_frame.columnconfigure(col_index, weight=1)
            content_frame.columnconfigure(col_index, weight=1)
            # header widgets
            header_label = ctk.CTkLabel(header_frame, text=name, font=("Arial", 14, "bold"), width=width)
            header_label.grid(row=0, column=col_index, sticky="nsew")

        # Store the content frame for later use
        self.content_frame = content_frame

    def add_row(self, row_data):
        row_widgets = []
        for col_index, (col_name, value) in enumerate(zip(self.column_names, row_data)):
            data_label = ctk.CTkLabel(self.content_frame, text=value, width=self.column_widths[col_index],
                                      wraplength=self.column_widths[col_index])
            data_label.grid(row=self.current_row, column=col_index, sticky="nsew", pady=2)
            data_label.bind("<Button-1>", lambda e, row=self.current_row: self.toggle_row_selection(row))
            row_widgets.append(data_label)
        self.row_widgets.append(row_widgets)
        self.current_row += 1

    def toggle_row_selection(self, row):
        if row in self.selected_rows:
            self.selected_rows.remove(row)
            for widget in self.row_widgets[row - 1]:
                widget.configure(fg_color='#b1eba4')
        else:
            self.selected_rows.add(row)
            for widget in self.row_widgets[row - 1]:
                widget.configure(fg_color='#ffcccb')

    def get_selected_rows_data(self):
        selected_data = []
        for row in self.selected_rows:
            row_data = [widget.cget("text") for widget in self.row_widgets[row - 1]]
            selected_data.append(row_data)
        return selected_data

    def remove_selected_rows(self):
        for row in sorted(self.selected_rows, reverse=True):
            for widget in self.row_widgets[row - 1]:
                widget.destroy()
            del self.row_widgets[row - 1]
        self.selected_rows.clear()

    def clear_table(self):
        for row_widgets in self.row_widgets:
            for widget in row_widgets:
                widget.destroy()
        self.row_widgets.clear()
        self.selected_rows.clear()
        self.current_row = 1