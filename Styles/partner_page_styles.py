"""
This style sheet is focused on the partner page. main and central widget are included for clarity.
The structure is as follows:

QMainWindow (MainWindow)
│
├── QWidget (self.centralwidget)
│   ├── QStackedWidget (self.widget_main)
│   │   ├── QWidget (self.page_partner)  -  Starting here
│   │   │   ├── QFrame (self.frame_top)
│   │   │   │   ├── QLineEdit (self.partner_search)
│   │   │   │   └── QPushButton (self.partner_add_btn)
│   │   │   ├── QFrame (self.frame_table)
│   │   │   │   └── QTableView (self.partner_table)
│   │
│

"""

ADD_PARTNER_BUTTON = """
QPushButton {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
}
QPushButton:hover {
    background-color: #45a049;
}
QPushButton:pressed {
    background-color: #0D47A1;
}
QPushButton:disabled {
    background-color: #BDBDBD;
}
"""

PARTNER_TABLE = """
QHeaderView::section {
    background-color: #f0f0f0;
    padding: 10px;
    border: 1px solid #cccccc;
    font-weight: bold;
}
QTableView {
    gridline-color: #cccccc;
    alternate-background-color: #f9f9f9;
    selection-background-color: #0078d4;
    selection-color: white;
    border: 1px solid #cccccc;
}

QTableView::item {
    padding: 5px;
    border: none;
}

QTableView::item:selected {
    background-color: #0078d4;
    color: white;
}

QTableView::item:focus {
    background-color: #0078d4;
    color: white;
    border: none;
    outline: none;
}

QTableView::item:selected:active {
    background-color: #0078d4;
    color: white;
}

QTableView::item:selected:!active {
    background-color: #dadada;
    color: black;
}

QTableView::item:alternate {
    background-color: #f9f9f9;
}
"""

PARTNER_MENU = """ 
QMenu {
    background-color: white;
    border: 1px solid #cccccc;
    padding: 5px;
}
QMenu::item {
    padding: 5px 20px;  /* Vertical, Horizontal padding */
    margin: 0px;
}
QMenu::item:selected {
    background-color: #e6e6e6;
}
"""

PARTNER_COMBOBOX = """
QComboBox {
    padding: 5px;
    border: 2px solid #cccccc;
    border-radius: 3px;
    background-color: white;
}"""

PARTNER_LABEL = """
QLabel {
    color: #333333;
    border: none;
    background: none;
}
"""