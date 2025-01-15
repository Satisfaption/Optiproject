"""
This style sheet is focused on the settings page. main and central widget are included for clarity.
The structure is as follows:

QMainWindow (MainWindow)
│
├── QWidget (self.centralwidget)
│   ├── QStackedWidget (self.widget_main)
│   │   ├── QWidget (self.page_settings)  -  Starting here
│   │   │   ├── QGroupBox (change_password_group)
│   │   │   │   ├── QHBoxLayout (current_password_layout)
│   │   │   │   │   ├── QLabel (self.current_password_label)
│   │   │   │   │   ├── QLineEdit (self.current_password_edit)
│   │   │   │   │   └── QPushButton (current_password_reveal)
│   │   │   │   ├── QHBoxLayout (new_password_layout)
│   │   │   │   │   ├── QLabel (self.new_password_label)
│   │   │   │   │   ├── QLineEdit (self.new_password_edit)
│   │   │   │   │   └── QPushButton (new_password_reveal)
│   │   │   │   ├── QHBoxLayout (confirm_password_layout)
│   │   │   │   │   ├── QLabel (self.confirm_password_label)
│   │   │   │   │   ├── QLineEdit (self.confirm_password_edit)
│   │   │   │   │   └── QPushButton (confirm_password_reveal)
│   │   │   │   └── QHBoxLayout (button_layout)
│   │   │   │       └── QPushButton (change_password_button)
│   │   │   │
│   │   │   ├── QGroupBox (snapshot_group)
│   │   │   │   ├── QHBoxLayout (collection_layout)
│   │   │   │   │   ├── QLabel (collection_label)
│   │   │   │   │   └── QComboBox (self.collection_combo)
│   │   │   │   ├── QHBoxLayout (snapshot_create_layout)
│   │   │   │   │   ├── QLabel (snapshot_explanation)
│   │   │   │   │   └── QPushButton (snapshot_button)
│   │   │   │   ├── QHBoxLayout (snapshot_upload_layout)
│   │   │   │   │   ├── QLabel (upload_explanation)
│   │   │   │   │   └── QPushButton (upload_button)
│   │   │   │
│   │   │   ├── QGroupBox (manage_users_group)
│   │   │   │   ├── QTabWidget (tab_widget)
│   │   │   │   │   ├── QWidget (manage_user_tab)
│   │   │   │   │   │   ├── QHBoxLayout (user_combo_layout)
│   │   │   │   │   │   │   ├── QLabel (user_label)
│   │   │   │   │   │   │   └── QComboBox (self.user_combo)
│   │   │   │   │   │   ├── QHBoxLayout (role_combo_layout)
│   │   │   │   │   │   │   ├── QLabel (roles_label)
│   │   │   │   │   │   │   └── QComboBox (self.role_combo_manage)
│   │   │   │   │   │   ├── QHBoxLayout (password_layout)
│   │   │   │   │   │   │   ├── QLabel (password_label)
│   │   │   │   │   │   │   └── QLineEdit (self.password_edit_manage)
│   │   │   │   │   │   ├── QHBoxLayout (password_confirm_layout)
│   │   │   │   │   │   │   ├── QLabel (password_confirm_label)
│   │   │   │   │   │   │   └── QLineEdit (self.confirm_password_manage)
│   │   │   │   │   │   └── QHBoxLayout (manage_buttons_layout)
│   │   │   │   │   │       ├── QPushButton (self.save_button)
│   │   │   │   │   │       └── QPushButton (self.delete_button)
│   │   │   │   │   ├── QWidget (create_user_tab)
│   │   │   │   │   │   ├── QHBoxLayout (create_user_line_layout)
│   │   │   │   │   │   │   ├── QLabel (create_user_label)
│   │   │   │   │   │   │   └── QLineEdit (self.create_user_line)
│   │   │   │   │   │   ├── QHBoxLayout (role_create_combo_layout)
│   │   │   │   │   │   │   ├── QLabel (roles_create_label)
│   │   │   │   │   │   │   └── QComboBox (self.role_combo_create)
│   │   │   │   │   │   ├── QHBoxLayout (password_create_layout)
│   │   │   │   │   │   │   ├── QLabel (password_create_label)
│   │   │   │   │   │   │   └── QLineEdit (self.password_edit_create)
│   │   │   │   │   │   ├── QHBoxLayout (password_confirm_create_layout)
│   │   │   │   │   │   │   ├── QLabel (password_confirm_create_label)
│   │   │   │   │   │   │   └── QLineEdit (self.confirm_password_create)
│   │   │   │   │   │   └── QHBoxLayout (create_buttons_layout)
│   │   │   │   │   │       └── QPushButton (self.create_button)
│   │   │   │
│   │   │   ├── QGroupBox (logs_group)
│   │   │   │   ├── QTabWidget (log_tab)
│   │   │   │   │   ├── QTextEdit (self.user_logs_tab)
│   │   │   │   │   ├── QTextEdit (self.partner_logs_tab)
│   │   │   │   │   └── QTextEdit (self.ors_logs_tab)
│   │   │   │
│   │   │
│   │
│

"""

CHANGE_PW_SECTION = """
QGroupBox {
    font-weight: bold;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 10px;
}
QLabel {
    background: none;
    border: none;
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
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 3px;
    padding: 10px;
}
QPushButton:hover {
    background-color: #45a049;
}
"""

TRANSPARENT_BUTTON = """
QPushButton {
    background-color: transparent;
    border: none;
}
"""

SNAPSHOT_SECTION = """ 
QGroupBox {
    font-weight: bold;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 10px;
}
QLabel {
    background: none;
    border: none;
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
    background-color: #4CAF50;  /* Green background */
    color: white;  /* White text */
    border: none;  /* No border */
    border-radius: 3px;  /* Rounded corners */
    padding: 10px;  /* Padding */
}
QPushButton:hover {
    background-color: #45a049;  /* Darker green on hover */
}
"""

MANAGE_USER_SECTION = """ 
QGroupBox {
    font-weight: bold;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 10px;
}
QLabel {
    background: none;
    border: none;
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
    background-color: #4CAF50;  /* Green background */
    color: white;
    border: none;
    border-radius: 3px;
    padding: 10px;
}
QPushButton:hover {
    background-color: #45a049;  /* Darker green on hover */
}
QTabWidget::pane {
    border: none;
}
"""

LOG_SECTION = """
QGroupBox {
    font-weight: bold;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 10px;
}
QTextEdit {
    background-color: #f0f0f0;
    border: none;
}
QTabWidget::pane {
    border: 1px solid lightgray;
    border-radius: 3px;
}
"""