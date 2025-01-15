# === Central Widget Style ===
CENTRAL_WIDGET = """
QWidget {
    background-color: #f0f0f0;
}
"""

# === Stacked Widget Style ===
STACKED_WIDGET = """
QFrame {
    background-color: white;
}
"""

# === Menu ===
# Overlay (darkening everything)
OVERLAY_STYLE = """
background-color: rgba(0, 0, 0, 100);
"""

# Buttons
ICON_BUTTON_DEFAULT = """
QPushButton {
    background-color: rgb(0, 0, 0);
    border: none;
}
QPushButton:hover {
    background-color: rgb(45, 45, 45);
}
"""

MENU_BUTTON_DEFAULT = """
QPushButton {
    background-color: rgb(0, 0, 0);
    color: rgb(255, 255, 255);
    border: none;
    text-align: left;
    padding-left: 10px;
}
QPushButton:hover {
    background-color: rgb(45, 45, 45);
}
"""

ICON_BUTTON_ACTIVE = """
QPushButton {
    background-color: rgb(45, 45, 45);
    border: none;
}
"""

MENU_BUTTON_ACTIVE = """
QPushButton {
    background-color: rgb(45, 45, 45);
    color: rgb(255, 255, 255);
    border: none;
    text-align: left;
    padding-left: 10px;
}
"""