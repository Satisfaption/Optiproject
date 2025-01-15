"""
This style sheet is focused on the search page. main and central widget are included for clarity.
The structure is as follows:

QMainWindow (MainWindow)
│
├── QWidget (self.centralwidget)
│   ├── QStackedWidget (self.widget_main)
│   │   ├── QWidget (self.page_search)  -  Starting here
│   │   │   ├── QFrame (self.frame_Filter)
│   │   │   │   ├── QLabel ("Such Parameter")
│   │   │   │   ├── QComboBox (self.comboBox_Partner)
│   │   │   │   ├── QComboBox (self.comboBox_Begruenungsart)
│   │   │   │   └── QPushButton (self.pB_Suche)
│   │   │   ├── QFrame (self.frame_Table)
│   │   │   │   └── QTableView (self.tableView)
│   │   │   ├── QFrame (self.frame_Details)
│   │   │   │   ├── QLabel (self.label_ors_title, "ORS Nutzung")
│   │   │   │   ├── QLabel (self.label_ors_usage, "0 / 2000")
│   │   │   │   ├── QLabel (self.label_pisa_values, "Pisa")
│   │   │   │   └── QPushButton (self.button_copy_pisa, "Pisa kopieren")
│   │   │   └── QLabel (self.status_label)
│   │
│

"""

FILTER_FRAME = """
QWidget {
    background-color: white;
}
QFrame {
    background-color: white;
    border: 1px solid #cccccc;
    border-radius: 4px;
}
QLineEdit {
    padding: 5px;
    border: 2px solid #cccccc;
    border-radius: 3px;
    background-color: white;
}
QComboBox {
    padding: 5px;
    border: 2px solid #cccccc;
    border-radius: 3px;
    background-color: white;
}
QPushButton {
    padding: 5px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 3px;
}
QPushButton:hover {
    background-color: #45a049;
}
QLabel {
    color: #333333;
    border: none;
}
"""

HEADER_LABEL = """
QLabel {
    font-weight: bold;
    font-size: 14px;
    margin-bottom: 10px;
    color: #333333;
}
"""


SEARCH_BUTTON = """
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

DETAILS_FRAME = """
QFrame {
    background-color: #4CAF50;
}
"""
PISA_FRAME = """
QFrame {
    border-left: 2px solid black;
    border-top: none;
    border-right: none;
    border-bottom: none;
}
QLabel {
    font-size: 12px;
    color: #333333;
    border: none;
}
"""

PISA_BUTTON = """
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
}"""

STATUS_MESSAGE = """
QLabel {
    background-color: rgba(255, 255, 255, 0.9);
    padding: 10px;
    border-radius: 5px;
    font-size: 14px;
}
"""

TABLE = """
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
    border: none;
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

CONTEXT_MENU = """
QMenu {
    background-color: white;
    border: 1px solid #cccccc;
    padding: 5px;
}
QMenu::item {
    padding: 5px 20px;
    margin: 0px;
}
QMenu::item:selected {
    background-color: #e6e6e6;
}
"""