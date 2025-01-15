import sys
import os
from urllib.parse import quote_plus

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                              QFrame, QMessageBox, QSizePolicy, QLabel, QPushButton, QDialog, QFormLayout, QGroupBox,
                              QHeaderView, QSpacerItem, QApplication, QTableView, QLineEdit, QDialogButtonBox,
                               QGridLayout, QMenu, QComboBox, QFileDialog, QTabWidget, QInputDialog, QTextEdit)
from PySide6.QtCore import (QPropertyAnimation, QEasingCurve, QRect, Qt, QSize, Signal, QPoint)
from PySide6.QtGui import (QIcon, QStandardItemModel, QStandardItem)

from Database.logging import Logger
from Main_Window.UI.index import Ui_MainWindow
from Database.datafilter import DataFilter
from Database.connection import DatabaseConnectionError, Database
from Database.queries import DatabaseQueries
from utils.geocoding import get_coordinates
from utils.customs import parse_value
from Styles.general_styles import *
from Styles.search_page_styles import *
from Styles.partner_page_styles import *
from Styles.settings_page_styles import *
import json
from bson import ObjectId


class MainWindow(QMainWindow, Ui_MainWindow):

    logout_signal = Signal()
    _login_window_instance = None

    def __init__(self, auth_manager=None):
        super().__init__()
        self.auth_manager = auth_manager
        try:
            self.db = self.auth_manager.get_db() if auth_manager else None
            if not self.db:
                uri = os.getenv('MONGODB_URI_GUEST')
                db_name = os.getenv('MONGODB_NAME')
                self.db = Database(uri, db_name)

            self.db_queries = DatabaseQueries(self.db.db)
            self.current_user = self.auth_manager.get_current_user() if auth_manager else "Guest"

        except DatabaseConnectionError as e:
            QMessageBox.critical(self, "Datenbank Error", str(e))
            sys.exit(1)

        self.logger = Logger(self.db.db)

        # window title
        self.setupUi(self)
        self.setWindowTitle(f"Matrix - {self.current_user}")
        self.setWindowIcon(QIcon('og_transparent.ico'))
        self._setup_initial_styles()
        self.centralwidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.widget_main.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.widget_main.setMinimumSize(QSize(0, 0))
        self.widget_main.setMaximumSize(QSize(16777215, 16777215))

        # icon menu
        self.widget_icons.setFixedWidth(60)
        self.widget_icons.setMinimumHeight(0)
        self.widget_icons.setMaximumHeight(16777215)
        self.widget_icons.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.layoutWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layoutWidget.setGeometry(QRect(0, 0, 60, self.height()))

        # expandable menu
        self.widget_menu.setFixedWidth(180)
        self.widget_menu.setMinimumHeight(0)
        self.widget_menu.setMaximumHeight(16777215)
        self.widget_menu.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.layoutWidget1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layoutWidget1.setGeometry(QRect(0, 0, 180, self.height()))

        self.setMinimumSize(1500, 750)

        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)

        self._init_variables()
        self._init_menu()
        self._init_pages()
        self._init_signals()

    # === Initialization Methods ===
    def _init_variables(self):
        """Initialize class variables"""
        self.is_menu_expanded = False
        self.current_page = None
        self.ors_usage_count = 0

    def _init_menu(self):
        """Initialize menu and overlay (builds on index.py)"""
        self.widget_menu.setParent(self.centralwidget)
        self.widget_menu.raise_()
        self.widget_menu.setGeometry(QRect(-180, 0, 180, self.height()))

        self.vL_Menu.setSpacing(0)
        self.vL_Menu.setContentsMargins(0, 20, 0, 5)

        self.vSpacer_Menu.changeSize(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.vL_MenuIcon.setSpacing(0)
        self.vL_MenuIcon.setContentsMargins(0, 20, 0, 5)
        self.vSpacer_MenuIcon.changeSize(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.menu_animation = QPropertyAnimation(self.widget_menu, b"geometry")
        self.menu_animation.setDuration(250)
        self.menu_animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.overlay = QWidget(self.widget_main)
        self.overlay.setStyleSheet(OVERLAY_STYLE)
        self.overlay.hide()
        self.overlay.setGeometry(self.widget_main.rect())

        for layout in [self.vL_Menu, self.vL_MenuIcon]:
            layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            bottom_layout = layout.itemAt(layout.count() - 1).layout()
            if bottom_layout:
                bottom_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        menu_buttons = [
            self.pB_MenuIcon,
            self.pB_SearchIcon,
            self.pB_PartnerIcon,
            self.pB_SettingsIcon,
            self.pB_LogoutIcon,
            # expanded menu buttons
            self.pB_Menu,
            self.pB_Search,
            self.pB_Partner,
            self.pB_Settings,
            self.pB_Logout
        ]

        for button in menu_buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self._set_menu_visibility()

    def _setup_initial_styles(self):
        """Set up initial styles for all buttons (change from initial design from index.py)"""
        self.centralwidget.setStyleSheet(CENTRAL_WIDGET)

        self.widget_main.setStyleSheet(STACKED_WIDGET)

        self.frame_Filter.setStyleSheet(FILTER_FRAME)

        icon_buttons = [
            self.pB_MenuIcon,
            self.pB_SearchIcon,
            self.pB_PartnerIcon,
            self.pB_SettingsIcon,
            self.pB_LogoutIcon
        ]
        for button in icon_buttons:
            button.setStyleSheet(ICON_BUTTON_DEFAULT)

        menu_buttons = [
            self.pB_Menu,
            self.pB_Search,
            self.pB_Partner,
            self.pB_Settings,
            self.pB_Logout
        ]
        for button in menu_buttons:
            button.setStyleSheet(MENU_BUTTON_DEFAULT)

    def _init_pages(self):
        """Initialize all pages in the stacked widget"""
        self._init_search_page()
        self._init_partner_page()
        self._init_settings_page()

    def _init_signals(self):
        """Initialize all signal connections"""
        self._init_menu_signals()
        self._init_navigation_signals()
        self._init_search_page_signals()
        self._init_partner_page_signals()
        self._init_settings_page_signals()

    # === Menu Related Methods ===
    def _init_menu_signals(self):
        """Initialize menu-related signals"""
        self.pB_MenuIcon.clicked.connect(self._toggle_menu)
        self.pB_Menu.clicked.connect(self._toggle_menu)
        self.overlay.mousePressEvent = lambda event: self._toggle_menu()

        self.pB_LogoutIcon.clicked.connect(self.handle_logout)
        self.pB_Logout.clicked.connect(self.handle_logout)

    def _init_navigation_signals(self):
        """Initialize page navigation signals"""
        # search buttons
        self.pB_SearchIcon.clicked.connect(
            lambda: self.navigate_to_page(self.page_search, self.pB_SearchIcon, self.pB_Search))
        self.pB_Search.clicked.connect(
            lambda: self.navigate_to_page(self.page_search, self.pB_SearchIcon, self.pB_Search))

        # partner buttons
        self.pB_PartnerIcon.clicked.connect(
            lambda: self.navigate_to_page(self.page_partner, self.pB_PartnerIcon, self.pB_Partner))
        self.pB_Partner.clicked.connect(
            lambda: self.navigate_to_page(self.page_partner, self.pB_PartnerIcon, self.pB_Partner))

        # settings buttons
        self.pB_SettingsIcon.clicked.connect(
            lambda: self.navigate_to_page(self.page_settings, self.pB_SettingsIcon, self.pB_Settings))
        self.pB_Settings.clicked.connect(
            lambda: self.navigate_to_page(self.page_settings, self.pB_SettingsIcon, self.pB_Settings))

    def _toggle_menu(self):
        """Toggle the expanded menu"""
        target_x = 0 if not self.is_menu_expanded else -180

        # animation
        self.menu_animation.setStartValue(self.widget_menu.geometry())
        self.menu_animation.setEndValue(QRect(target_x, 0, 180, self.height()))

        # overlay
        if not self.is_menu_expanded:
            self.overlay.setGeometry(self.widget_main.rect())
            self.overlay.show()
            self.overlay.raise_()  # Bring overlay above content
            self.widget_menu.raise_()  # Bring menu above overlay
        else:
            self.overlay.hide()

        self.menu_animation.start()
        self.is_menu_expanded = not self.is_menu_expanded

    def _set_menu_visibility(self):
        """Set visibility of menu items based on user role"""
        user_roles = self.db.get_user_roles(self.current_user)

        if 'dbOwner' in user_roles or 'atlasAdmin' in user_roles:
            self.pB_Partner.setVisible(True)
            self.pB_Settings.setVisible(True)
            self.pB_PartnerIcon.setVisible(True)
            self.pB_SettingsIcon.setVisible(True)
        else:
            self.pB_Partner.setVisible(False)
            self.pB_Settings.setVisible(False)
            self.pB_PartnerIcon.setVisible(False)
            self.pB_SettingsIcon.setVisible(False)

    def handle_logout(self):
        """Handle logout button clicks"""
        try:
            if self.db:
                self.db.close_connection()
                self.db = None

            if self.auth_manager:
                self.auth_manager.logout()

            if hasattr(self, '_login_window_instance'):
                self._login_window_instance = None

            self._redirect_to_login()

        except Exception as e:
            QMessageBox.warning(self, "Logout Error", f"Fehler beim Abmelden: {str(e)}")

    def navigate_to_page(self, page, icon_button, menu_button):
        """Handle navigation to a specific page"""
        self.widget_main.setCurrentWidget(page)
        self.update_button_styles(icon_button, menu_button)
        if self.is_menu_expanded:
            self._toggle_menu()

    def update_button_styles(self, icon_button, menu_button):
        """Update buttons to show current selection"""
        self.reset_button_styles()
        self.set_active_button_styles(icon_button, menu_button)

    def reset_button_styles(self):
        """Reset all button styles to default"""
        for btn in [self.pB_SearchIcon, self.pB_PartnerIcon, self.pB_SettingsIcon]:
            btn.setStyleSheet(ICON_BUTTON_DEFAULT)

        for btn in [self.pB_Search, self.pB_Partner, self.pB_Settings]:
            btn.setStyleSheet(MENU_BUTTON_DEFAULT)

    def set_active_button_styles(self, icon_button, menu_button):
        """Set styles for active buttons"""
        icon_button.setStyleSheet(ICON_BUTTON_ACTIVE)
        menu_button.setStyleSheet(MENU_BUTTON_ACTIVE)

    # === Search Page Methods ===
    def _init_search_page(self):
        """Initialize search page components"""
        self.page_search = QWidget()
        self.widget_main.addWidget(self.page_search)

        self.widget_main.setGeometry(QRect(60, 0, self.width() - 60, self.height()))
        self.widget_main.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # main layout
        layout = QHBoxLayout(self.page_search)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # filter frame
        self.frame_Filter.setParent(self.page_search)
        self.frame_Filter.setFixedWidth(180)
        self.frame_Filter.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.frame_Filter.setContentsMargins(0, 0, 0, 0)
        self.frame_Filter.setMinimumHeight(0)
        self.frame_Filter.setMaximumHeight(16777215)

        # widget that holds vL_Filter
        self.widget.setContentsMargins(5, 5, 5, 5)
        self.widget.setGeometry(0, 0, 180, self.frame_Filter.height())
        self.widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.widget.setMaximumHeight(self.frame_Filter.height())
        self.widget.setMinimumHeight(0)
        self.widget.setMaximumHeight(16777215)

        self.widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.vL_Filter.setContentsMargins(10, 10, 10, 10)
        self.vL_Filter.setSpacing(0)

        # remove and re add to better/easier align
        self.vL_Choice.removeWidget(self.comboBox_Partner)
        self.vL_Choice.removeWidget(self.comboBox_Begruenungsart)
        self.vL_Filter.removeWidget(self.pB_Suche)
        self.vL_Filter.removeItem(self.vL_Choice)
        self.vL_Filter.removeItem(self.vSpacer_Filter)

        i = self.vL_Filter.count() - 1
        while i >= 0:
            item = self.vL_Filter.itemAt(i)
            if item and item.spacerItem():
                self.vL_Filter.removeItem(item)
            i -= 1

        self.vL_Filter.insertStretch(1, 2)  # After PLZ
        self.vL_Filter.insertStretch(3, 2)  # After Fläche
        self.vL_Filter.insertStretch(5, 2)  # After Straße
        self.vL_Filter.insertStretch(7, 2)  # After Ort (smaller space)

        self.vL_Filter.addWidget(self.comboBox_Partner)
        self.vL_Filter.addStretch(2)
        self.vL_Filter.addWidget(self.comboBox_Begruenungsart)
        self.vL_Filter.addStretch(4)
        self.vL_Filter.addWidget(self.pB_Suche)

        search_params_label = QLabel("Such Parameter")
        search_params_label.setStyleSheet(HEADER_LABEL)
        self.vL_Filter.insertWidget(0, search_params_label)
        self.vL_Filter.insertStretch(1, 2)

        self.pB_Suche.setContentsMargins(0, 10, 0, 10)
        self.pB_Suche.setStyleSheet(SEARCH_BUTTON)

        self.vSpacer_Filter.changeSize(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        right_container = QWidget()
        right_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        # table section
        self._setup_table()
        right_layout.addWidget(self.tableView)

        # details frame for ORS usage and PISA values
        self.frame_Details = QFrame()
        self.frame_Details.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_Details.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_Details.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        details_layout = QHBoxLayout(self.frame_Details)
        details_layout.setContentsMargins(10, 10, 10, 10)
        details_layout.setSpacing(5)

        # ORS Usage Section
        self.frame_ORS = QFrame()
        self.frame_ORS.setStyleSheet("border: none;")
        self.frame_ORS.setMinimumWidth(150)
        self.frame_ORS.setMaximumWidth(150)

        ors_layout = QVBoxLayout(self.frame_ORS)
        ors_layout.setContentsMargins(5, 5, 5, 5)

        self.label_ors_title = QLabel("ORS Nutzung")
        self.label_ors_title.setStyleSheet(HEADER_LABEL)
        self.label_ors_usage = QLabel("0 / 2000")
        self.label_ors_usage.setStyleSheet("font-size: 14px;")

        ors_layout.addWidget(self.label_ors_title)
        ors_layout.addWidget(self.label_ors_usage)

        details_layout.addWidget(self.frame_ORS)

        # PISA Values Section
        self.frame_Pisa = QFrame()
        self.frame_Pisa.setStyleSheet(PISA_FRAME)

        self.label_pisa_values = QLabel("Pisa")
        self.label_pisa_values.setWordWrap(True)

        pisa_layout = QVBoxLayout(self.frame_Pisa)
        pisa_layout.setContentsMargins(10, 5, 5, 5)
        pisa_layout.addWidget(self.label_pisa_values)

        details_layout.addWidget(self.frame_Pisa)

        self.button_copy_pisa = QPushButton("Pisa kopieren")
        self.button_copy_pisa.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.button_copy_pisa.setMinimumWidth(100)
        self.button_copy_pisa.setStyleSheet(PISA_BUTTON)

        details_layout.addWidget(self.button_copy_pisa)

        right_layout.addWidget(self.frame_Details)

        layout.addWidget(self.frame_Filter)
        layout.addWidget(right_container)

        # stretch factors
        layout.setStretch(0, 0)  # Filter no stretch
        layout.setStretch(1, 1)  # table side stretches

        self.status_label = QLabel(self.tableView)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(STATUS_MESSAGE)
        self.status_label.hide()

        self._update_ors_display()

    def show_status_message(self, message):
        """Status message of search progress"""
        label_width = 250
        label_height = 40
        x = (self.tableView.width() - label_width) // 2
        y = (self.tableView.height() - label_height) // 2
        self.status_label.setGeometry(x, y, label_width, label_height)
        self.status_label.setText(message)
        self.status_label.show()
        QApplication.processEvents()

    def hide_status_message(self):
        self.status_label.hide()

    def _init_search_page_signals(self):
        """Initialize search page signals"""
        self.pB_Suche.clicked.connect(self._handle_search)
        self.tableView.clicked.connect(self._handle_table_click)
        self.button_copy_pisa.clicked.connect(self._copy_pisa_values)

    def _setup_table(self):
        """Set up table (continuation/adjustment from index.py)"""
        self.table_model = QStandardItemModel(0, 7, self)  # 0 rows, 7 columns
        self.table_model.setHorizontalHeaderLabels([
            'Name', 'Pisa', 'PLZ', 'Gebietsleiter', 'Entfernung (km)', 'Kurzform', 'Zusatzinfo'])

        self.tableView.setModel(self.table_model)
        self.tableView.verticalHeader().hide()
        self.last_selected_row = None

        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.tableView.setSortingEnabled(True)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.tableView.setSelectionMode(QTableView.SelectionMode.MultiSelection)
        self.tableView.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.tableView.setStyleSheet(TABLE)

        # context menu (right click)
        self.tableView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self._show_copy_menu)

    def _show_copy_menu(self, pos: QPoint):
        """Context menu with a 'Copy X' option"""
        index = self.tableView.indexAt(pos)
        if not index.isValid():
            return

        menu = QMenu(self)
        menu.setStyleSheet(CONTEXT_MENU)
        copy_pisa_action = menu.addAction("Pisa kopieren")
        copy_zusatzinfo_action = menu.addAction("Kurzform kopieren")
        action = menu.exec(self.tableView.viewport().mapToGlobal(pos))

        if action == copy_pisa_action:
            self._copy_selected_column(1)  # Column index for 'Pisa'
        elif action == copy_zusatzinfo_action:
            self._copy_selected_column(5)  # Column index for 'Kurzform'

    def _copy_selected_column(self, column_index):
        """Copy values from the specified column for all selected rows"""
        selected_indexes = self.tableView.selectedIndexes()
        specific_values = []

        for idx in selected_indexes:
            if idx.column() == column_index:
                specific_values.append(self.tableView.model().data(idx))

        if specific_values:
            # DDifferent separator based on the column index
            if column_index == 1:  # Pisa column
                separator = " | "
            elif column_index == 5:  # Zusatzinfo column
                separator = "\n"
            else:
                separator = ", "  # Default separator for other columns

            copied_text = separator.join(specific_values)

            clipboard = QApplication.clipboard()
            clipboard.setText(copied_text)

    def _handle_search(self):
        """Handle search button click"""
        try:
            plz = self.lineEdit_PLZ.text().strip()
            flaeche = self.lineEdit_Flaeche.text().strip()
            street = self.lineEdit_Strasse.text().strip()
            town = self.lineEdit_Ort.text().strip()
            begruenungsart = self.comboBox_Begruenungsart.currentText()
            partner_type = self.comboBox_Partner.currentText()

            if not plz or not flaeche:
                QMessageBox.warning(self, "Eingabe Fehler", "PLZ und Fläche sind erforderliche Felder.")
                return

            self.table_model.removeRows(0, self.table_model.rowCount())

            self.show_status_message("Suche läuft...")
            self.pB_Search.setEnabled(False)

            data_filter = DataFilter(self.db_queries)

            filtered_data, error_message = data_filter.filter_data(
                plz=plz,
                flaeche=flaeche,
                begruenungsart=begruenungsart,
                partner_type=partner_type,
                street=street,
                town=town
            )

            if error_message:
                QMessageBox.warning(self, "Fehler bei der Suche", "\n".join(error_message))

            if not filtered_data:
                self.table_model.removeRows(0, self.table_model.rowCount())
                self.show_status_message("Keine Ergebnisse gefunden.")
            else:
                self.hide_status_message()
                self._update_table_with_data(filtered_data)
                self._update_ors_display()
                self._populate_pisa_values()

        except Exception as e:
            self.table_model.removeRows(0, self.table_model.rowCount())
            self.show_status_message(f"Ein Fehler ist aufgetreten: {str(e)}")

        finally:
            self.pB_Search.setEnabled(True)
            self.pB_Search.setText("Suchen")

    def _update_table_with_data(self, data):
        """Update table with filtered data"""
        self.table_model.removeRows(0, self.table_model.rowCount())

        for row, (kundennummer, details) in enumerate(data.items()):
            kurzform = f"{details.get('Name', '')} - {details.get('Postleitzahl', '')} - {details.get('Ort', '')}"

            # distance item with sorting
            distance_item = QStandardItem()
            distance_item.setData(float(details.get('Distance', 0)), Qt.ItemDataRole.DisplayRole)

            row_items = [
                QStandardItem(str(details.get('Name', ''))),
                QStandardItem(str(details.get('Pisa', ''))),
                QStandardItem(str(details.get('Postleitzahl', ''))),
                QStandardItem(str(details.get('Gebietsleiter', ''))),
                distance_item,
                QStandardItem(kurzform),
                QStandardItem(str(details.get('Zusatzinfo', '')))
            ]

            for item in row_items:
                item.setEditable(False)

            self.table_model.appendRow(row_items)

        for row in range(self.table_model.rowCount()):
            self.tableView.resizeRowToContents(row)
        for column in range(self.table_model.columnCount()):
            self.tableView.resizeColumnToContents(column)

    def _handle_table_click(self, index):
        """Allow dor deselection"""
        current_row = index.row()

        if current_row == self.last_selected_row:
            self.tableView.clearSelection()
            self.last_selected_row = None
        else:
            self.last_selected_row = current_row

    def _update_ors_display(self):
        """Update ORS value"""
        ors_count = self.db_queries.get_latest_ors_count()
        self.label_ors_usage.setText(f"{ors_count} / 2000")

    def _populate_pisa_values(self):
        """get & set PISA values"""
        pisa_values = []

        for row in range(self.table_model.rowCount()):
            item = self.table_model.item(row, 1)
            if item is not None:
                value = item.text().strip()
                if value:
                    pisa_values.append(value)

        self.label_pisa_values.setText(" | ".join(pisa_values))

    def _copy_pisa_values(self):
        """Copy PISA values to clipboard"""
        pisa_text = self.label_pisa_values.text()
        clipboard = QApplication.clipboard()
        clipboard.setText(pisa_text)

    # === Partner Page Methods ===
    def _init_partner_page(self):
        """Initialize partner page components"""
        self.page_partner = QWidget()
        self.widget_main.addWidget(self.page_partner)
        layout = QVBoxLayout(self.page_partner)

        # Top Layout for Searchbar & add new
        search_layout = QHBoxLayout()
        self.partner_search = QLineEdit()
        self.partner_search.setPlaceholderText("Nach Name suchen...")
        self.partner_search.setFixedWidth(300)
        self.partner_search.setMinimumHeight(30)

        self.partner_add_btn = QPushButton("Eintrag erstellen")
        self.partner_add_btn.setMinimumHeight(30)
        self.partner_add_btn.setFixedWidth(150)
        self.partner_add_btn.setStyleSheet(ADD_PARTNER_BUTTON)

        # Collection selection
        collection_label = QLabel("Geschäftstyp:")
        collection_label.setStyleSheet(PARTNER_LABEL)
        collection_selection = ['Partner', 'Dachdecker', 'Handel']
        self.partner_collection_cb = QComboBox()
        self.partner_collection_cb.setMinimumWidth(150)
        self.partner_collection_cb.setMaximumWidth(150)
        self.partner_collection_cb.setStyleSheet(PARTNER_COMBOBOX)

        for coll in collection_selection:
            self.partner_collection_cb.addItem(coll)

        search_layout.addWidget(collection_label)
        search_layout.addWidget(self.partner_collection_cb)
        search_layout.addStretch()
        search_layout.addWidget(self.partner_search)
        search_layout.addStretch()
        search_layout.addWidget(self.partner_add_btn)
        layout.addLayout(search_layout)

        # Table
        self.partner_table = QTableView()
        self.partner_model = QStandardItemModel(0, 7)
        self.partner_model.setHorizontalHeaderLabels([
            "Name", "Pisa", "PLZ", "Begrünungsart", "Fläche (Min-Max)", "Entfernung", "Kundennummer"
        ])
        self.partner_table.setModel(self.partner_model)

        self.partner_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.partner_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.partner_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.partner_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.partner_table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.partner_table.setSortingEnabled(True)

        header = self.partner_table.horizontalHeader()
        header.setStyleSheet(PARTNER_TABLE)

        layout.addWidget(self.partner_table)

        # Context menu
        self.partner_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.partner_table.customContextMenuRequested.connect(self._show_context_menu)

        self.partner_collection_cb.currentIndexChanged.connect(self._load_partners)  # combobox connect moved to after table

        self._load_partners()

    def _show_context_menu(self, position):
        """context menu for partner table with options to edit/delete"""
        menu = QMenu(self)
        menu.setStyleSheet(PARTNER_MENU)

        edit_action = menu.addAction("Bearbeiten")
        delete_action = menu.addAction("Löschen")

        global_pos = self.partner_table.viewport().mapToGlobal(position)

        index = self.partner_table.currentIndex()
        if index.isValid():
            action = menu.exec(global_pos)
            if action == edit_action:
                self._edit_selected_partner()
            elif action == delete_action:
                self._delete_selected_partner()

    def _load_partners(self):
        """Load all partners into table"""
        try:
            self.partner_model.removeRows(0, self.partner_model.rowCount())
            query = {}
            query_hash = self.db_queries._hash_query(query)
            selected_collection = self.partner_collection_cb.currentText()
            partners_data = self.db_queries.get_table_data(query_hash, selected_collection)

            if not partners_data:
                return

            for row, (kundennummer, partner) in enumerate(partners_data.items()):
                name_item = QStandardItem(str(partner.get('Name', '')))
                name_item.setData(partner.get('_id'), Qt.UserRole)  # store ID in UserRole

                pisa_item = QStandardItem(str(partner.get('Pisa', '')))
                kunde_item = QStandardItem(str(kundennummer))
                plz_value = partner.get('Postleitzahl', '')
                plz_item = QStandardItem(str(plz_value))

                # unpack Begrünungsart
                begruenungsarten = partner.get('Begrünungsart', {})
                if begruenungsarten:
                    begruenungsart_texts = []
                    flaeche_texts = []
                    entfernung_texts = []

                    for art, details in begruenungsarten.items():
                        begruenungsart_texts.append(art)
                        flaeche_min = details.get('Fläche (Minimum)', '-')
                        flaeche_max = details.get('Fläche (Maximum)', '-')
                        flaeche_texts.append(f"{flaeche_min} - {flaeche_max}")
                        entfernung = details.get('Entfernung', '-')
                        entfernung_texts.append(str(entfernung))

                    begruenungsart_item = QStandardItem('\n'.join(begruenungsart_texts))
                    flaeche_item = QStandardItem('\n'.join(flaeche_texts))
                    entfernung_item = QStandardItem('\n'.join(entfernung_texts))
                else:
                    begruenungsart_item = QStandardItem('-')
                    flaeche_item = QStandardItem('-')
                    entfernung_item = QStandardItem('-')

                self.partner_model.appendRow(
                    [name_item, pisa_item, plz_item, begruenungsart_item, flaeche_item, entfernung_item, kunde_item])
                self.partner_table.resizeRowToContents(row)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fehler beim Laden der Partner: {str(e)}")

    def _handle_partner_search(self, text):
        """Filter partners based on search input string"""
        text = text.strip()
        if len(text) < 3:
            for row in range(self.partner_model.rowCount()):
                self.partner_table.showRow(row)
            return

        for row in range(self.partner_model.rowCount()):
            name_item = self.partner_model.item(row, 0)
            if name_item and text.lower() in name_item.text().lower():
                self.partner_table.showRow(row)
            else:
                self.partner_table.hideRow(row)

    def _show_partner_dialog(self, partner_data=None):
        """Dialog window to input new data for partners"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Details - " + self.partner_collection_cb.currentText())
        dialog.setMinimumWidth(1000)

        # Main layout
        main_layout = QVBoxLayout(dialog)

        form_widget = QWidget()
        form_layout = QGridLayout(form_widget)

        line_edit_width = 200

        fields = [
            ("Name*:", "Name"),
            ("Pisa:", "Pisa"),
            ("Straße:", "Straße"),
            ("PLZ:", "Postleitzahl"),
            ("Ort:", "Ort"),
            ("Gebietsleiter:", "Gebietsleiter"),
            ("Kundennummer*:", "Kundennummer"),
            ("Präferierter DD:", "Präferierter DD"),
            ("Zusatzinfo:", "Zusatzinfo")
        ]

        line_edits = {}

        # label + lineEdit for each value (9 items split into 3 columns)
        for i, (label_text, field_name) in enumerate(fields):
            label = QLabel(label_text)
            line_edit = QLineEdit()
            line_edit.setFixedWidth(line_edit_width)

            if partner_data:
                line_edit.setText(str(partner_data.get(field_name, '')))

            line_edits[field_name] = line_edit

            row = i // 3
            col = (i % 3) * 2
            form_layout.addWidget(label, row, col)
            form_layout.addWidget(line_edit, row, col + 1)

        main_layout.addWidget(form_widget)

        # Begrünungsart section
        begruenungsart_widget = QWidget()
        begruenungsart_layout = QHBoxLayout(begruenungsart_widget)
        begruenungsart_fields = {}

        begruenungsart_types = ['Extensiv', 'Intensiv', 'Verkehrsdach']
        existing_begruenungsart = partner_data.get('Begrünungsart', {}) if partner_data else {}

        for art_type in begruenungsart_types:
            group = QGroupBox(art_type)
            group_layout = QFormLayout(group)

            flaeche_min_edit = QLineEdit()
            flaeche_max_edit = QLineEdit()
            entfernung_edit = QLineEdit()

            for edit in (flaeche_min_edit, flaeche_max_edit, entfernung_edit):
                edit.setFixedWidth(100)

            if art_type in existing_begruenungsart:
                details = existing_begruenungsart[art_type]
                flaeche_min_edit.setText(str(details.get('Fläche (Minimum)', '')))
                flaeche_max_edit.setText(str(details.get('Fläche (Maximum)', '')))
                entfernung_edit.setText(str(details.get('Entfernung', '')))

            group_layout.addRow("Fläche (Min):", flaeche_min_edit)
            group_layout.addRow("Fläche (Max):", flaeche_max_edit)
            group_layout.addRow("Entfernung:", entfernung_edit)

            begruenungsart_layout.addWidget(group)
            begruenungsart_fields[art_type] = (flaeche_min_edit, flaeche_max_edit, entfernung_edit)

        main_layout.addWidget(begruenungsart_widget)

        # dialog with option for ok/save & cancel
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        main_layout.addWidget(buttons)

        ok_button = buttons.button(QDialogButtonBox.Ok)
        cancel_button = buttons.button(QDialogButtonBox.Cancel)

        ok_button.setText("Speichern")
        cancel_button.setText("Abbrechen")

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        # capture new data on ok/save
        if dialog.exec() == QDialog.Accepted:
            selected_collection = self.partner_collection_cb.currentText()
            new_partner_data = {
                'Name': line_edits['Name'].text(),
                'Gebietsleiter': line_edits['Gebietsleiter'].text(),
                'Präferierter DD': line_edits['Präferierter DD'].text(),
                'Pisa': line_edits['Pisa'].text(),
                'Kundennummer': parse_value(line_edits['Kundennummer'].text(), int),
                'Zusatzinfo': line_edits['Zusatzinfo'].text(),
                'Straße': line_edits['Straße'].text(),
                'Postleitzahl': line_edits['Postleitzahl'].text(),
                'Ort': line_edits['Ort'].text(),
                'Begrünungsart': {}
            }

            try:
                # calculate lat/long coordinates for entered values
                lat, lon = get_coordinates(
                    plz=new_partner_data['Postleitzahl'],
                    street=new_partner_data['Straße'],
                    town=new_partner_data['Ort']
                )

                if lat is not None and lon is not None:
                    new_partner_data['Latitude'] = lat
                    new_partner_data['Longitude'] = lon
                else:
                    QMessageBox.warning(
                        self,
                        "Warnung",
                        "Koordinaten konnten nicht berechnet werden. Bitte überprüfen Sie die Adressdaten."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Fehler",
                    f"Unerwarteter Fehler bei der Koordinatenberechnung: {str(e)}"
                )

            for art_type, (min_edit, max_edit, ent_edit) in begruenungsart_fields.items():
                if min_edit.text().strip() or max_edit.text().strip() or ent_edit.text().strip():
                    new_partner_data['Begrünungsart'][art_type] = {
                        'Fläche (Minimum)': parse_value(min_edit.text(), int),
                        'Fläche (Maximum)': parse_value(max_edit.text(), int),
                        'Entfernung': parse_value(ent_edit.text(), int)
                    }

            # save/update data
            try:
                if partner_data and '_id' in partner_data:
                    self.db_queries.update_partner(partner_data['_id'], new_partner_data, selected_collection)
                    QMessageBox.information(self, "Information", "Partner Daten wurden aktualisiert.")
                    self.logger.log_partner_action(self.current_user, "aktualisiert", new_partner_data['Name'])
                    self._refresh_logs()
                else:
                    self.db_queries.insert_partner(new_partner_data, selected_collection)
                    QMessageBox.information(self, "Information", "Neuer Partner wurde erstellt.")
                    self.logger.log_partner_action(self.current_user, "erstellt", new_partner_data['Name'])
                    self._refresh_logs()
                self._load_partners()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Fehler beim Speichern: {str(e)}")

    def _edit_selected_partner(self):
        """Edit selected partner"""
        index = self.partner_table.currentIndex()
        selected_collection = self.partner_collection_cb.currentText()
        if not index.isValid():
            QMessageBox.warning(self, "Warnung", "Bitte wählen Sie einen Eintrag aus.")
            return

        partner_id = self.partner_model.item(index.row(), 0).data(Qt.UserRole)

        try:
            partner_data = self.db_queries.get_partner_by_id(partner_id, selected_collection)
            if not partner_data:
                raise ValueError("Keinen Datenbank Eintrag gefunden")

            self._show_partner_dialog(partner_data)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fehler beim Laden der Daten: {str(e)}")

    def _delete_selected_partner(self):
        """Delete selected partner"""
        index = self.partner_table.currentIndex()
        selected_collection = self.partner_collection_cb.currentText()
        if not index.isValid():
            QMessageBox.warning(self, "Warnung", "Bitte wählen Sie einen Eintrag aus.")
            return

        reply = QMessageBox(self)
        reply.setWindowTitle(selected_collection + " - Eintrag löschen")
        reply.setText("Möchten Sie diesen Eintrag wirklich löschen?")

        confirm_button = reply.addButton("Ja", QMessageBox.ButtonRole.AcceptRole)
        cancel_button = reply.addButton("Nein", QMessageBox.ButtonRole.RejectRole)

        reply.exec()

        if reply.clickedButton() == confirm_button:
            try:
                partner_item = self.partner_model.item(index.row(), 0)
                partner_name = partner_item.text()
                partner_id = partner_item.data(Qt.UserRole)

                self.logger.log_partner_action(self.current_user, "gelöscht", partner_name)
                self._refresh_logs()
                self.db_queries.delete_partner(partner_id, selected_collection)
                self._load_partners()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Fehler beim Löschen: {str(e)}")

    def _init_partner_page_signals(self):
        """Initialize partner page signals"""
        self.partner_search.textChanged.connect(self._handle_partner_search)
        self.partner_add_btn.clicked.connect(self._show_partner_dialog)

    # === Settings Page Methods ===
    def _init_settings_page(self):
        """Initialize settings page components"""
        self.page_settings = QWidget()
        self.widget_main.addWidget(self.page_settings)
        layout = QGridLayout(self.page_settings)

        # === Change Password Section ===
        change_password_group = QGroupBox("Passwort ändern")
        change_password_layout = QGridLayout(change_password_group)
        change_password_group.setStyleSheet(CHANGE_PW_SECTION)

        # current password input
        self.current_password_label = QLabel("Aktuelles Passwort:")
        self.current_password_label.setFixedWidth(160)
        self.current_password_edit = QLineEdit()
        self.current_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.current_password_edit.setFixedWidth(150)
        current_password_reveal = QPushButton("🙈")
        current_password_reveal.setCheckable(True)
        current_password_reveal.setFixedWidth(30)
        current_password_reveal.setStyleSheet(TRANSPARENT_BUTTON)
        current_password_reveal.toggled.connect(
            lambda: self._toggle_password_visibility(self.current_password_edit, current_password_reveal))

        current_password_layout = QHBoxLayout()
        current_password_layout.addWidget(self.current_password_label)
        current_password_layout.addWidget(self.current_password_edit)
        current_password_layout.addWidget(current_password_reveal)
        current_password_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        change_password_layout.addLayout(current_password_layout, 0, 0)  # Row 0, Column 0

        # new password input
        self.new_password_label = QLabel("Neues Passwort:")
        self.new_password_label.setFixedWidth(160)
        self.new_password_edit = QLineEdit()
        self.new_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_edit.setFixedWidth(150)
        new_password_reveal = QPushButton("🙈")
        new_password_reveal.setCheckable(True)
        new_password_reveal.setFixedWidth(30)
        new_password_reveal.setStyleSheet(TRANSPARENT_BUTTON)
        new_password_reveal.toggled.connect(
            lambda: self._toggle_password_visibility(self.new_password_edit, new_password_reveal))

        new_password_layout = QHBoxLayout()
        new_password_layout.addWidget(self.new_password_label)
        new_password_layout.addWidget(self.new_password_edit)
        new_password_layout.addWidget(new_password_reveal)
        new_password_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        change_password_layout.addLayout(new_password_layout, 1, 0)  # Row 1, Column 0

        # confirm password input
        self.confirm_password_label = QLabel("Neues Passwort bestätigen:")
        self.confirm_password_label.setFixedWidth(160)
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_edit.setFixedWidth(150)
        confirm_password_reveal = QPushButton("🙈")
        confirm_password_reveal.setCheckable(True)
        confirm_password_reveal.setFixedWidth(30)
        confirm_password_reveal.setStyleSheet(TRANSPARENT_BUTTON)
        confirm_password_reveal.toggled.connect(
            lambda: self._toggle_password_visibility(self.confirm_password_edit, confirm_password_reveal))

        confirm_password_layout = QHBoxLayout()
        confirm_password_layout.addWidget(self.confirm_password_label)
        confirm_password_layout.addWidget(self.confirm_password_edit)
        confirm_password_layout.addWidget(confirm_password_reveal)
        confirm_password_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        change_password_layout.addLayout(confirm_password_layout, 2, 0)  # Row 2, Column 0

        # save button
        button_layout = QHBoxLayout()
        change_password_button = QPushButton("Passwort ändern")
        change_password_button.clicked.connect(self._change_password)
        change_password_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button_layout.addWidget(change_password_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        change_password_layout.addLayout(button_layout, 3, 0)

        change_password_layout.setVerticalSpacing(15)

        layout.addWidget(change_password_group, 0, 0)  # Row 0, Column 0



        # === Snapshot Section ===
        snapshot_group = QGroupBox("Datenbank-Snapshot erstellen")
        snapshot_layout = QGridLayout(snapshot_group)

        collection_layout = QHBoxLayout()

        # collection selection
        collection_label = QLabel("Sammlung:")
        collection_label.setFixedWidth(collection_label.sizeHint().width())
        self.snapshot_collection_cb = QComboBox()
        self._load_collections()
        self.snapshot_collection_cb.setFixedWidth(150)

        collection_layout.addWidget(collection_label)
        collection_layout.addWidget(self.snapshot_collection_cb)
        collection_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        snapshot_layout.addLayout(collection_layout, 0, 0)

        # create snapshot + explanation
        snapshot_create_layout = QHBoxLayout()
        snapshot_explanation = QLabel("Erstellen Sie einen Snapshot der ausgewählten Sammlung. "
                                      "Ein Snapshot speichert den aktuellen Zustand der Datenbank im JSON Format.")
        snapshot_explanation.setWordWrap(True)
        snapshot_explanation.setFixedHeight(40)
        snapshot_explanation.setFixedWidth(400)
        snapshot_create_layout.addWidget(snapshot_explanation)
        snapshot_create_layout.setContentsMargins(0, 10, 0, 0)

        snapshot_button = QPushButton("Snapshot erstellen")
        snapshot_button.setFixedWidth(150)
        snapshot_button.clicked.connect(self._create_snapshot)

        snapshot_create_layout.addWidget(snapshot_button)
        snapshot_layout.addLayout(snapshot_create_layout, 1, 0)

        # upload snapshot + explanation
        snapshot_upload_layout = QHBoxLayout()
        upload_explanation = QLabel("Ausgewählte Sammlung wird auf den Zustand der ausgewählten Datei zurück gesetzt. "
                                    "Nur im Notfall benutzen, da alles überschrieben wird.")
        upload_explanation.setWordWrap(True)
        upload_explanation.setFixedHeight(40)
        upload_explanation.setFixedWidth(400)
        snapshot_upload_layout.addWidget(upload_explanation)
        snapshot_upload_layout.setContentsMargins(0, 10, 0, 0)

        upload_button = QPushButton("Backup hochladen")
        upload_button.setFixedWidth(150)
        upload_button.clicked.connect(self._upload_data)

        snapshot_upload_layout.addWidget(upload_button)
        snapshot_layout.addLayout(snapshot_upload_layout, 2, 0)

        snapshot_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        snapshot_layout.setVerticalSpacing(15)

        snapshot_group.setStyleSheet(SNAPSHOT_SECTION)

        layout.addWidget(snapshot_group, 0, 1)  # Row 0, Column 1

        # === Manage User Section ===
        manage_users_group = QGroupBox("Benutzer verwalten")
        manage_users_layout = QGridLayout(manage_users_group)

        tab_widget = QTabWidget()
        manage_users_layout.addWidget(tab_widget, 0, 0)

        # Manage User tab
        manage_user_tab = QWidget()
        manage_user_layout = QVBoxLayout(manage_user_tab)

        self.user_combo = QComboBox()
        self._load_users()
        user_label = QLabel("Benutzer:")
        self.user_combo.setFixedWidth(150)
        self.user_combo.setFixedHeight(30)
        user_label.setFixedWidth(150)
        user_label.setFixedHeight(30)

        user_combo_layout = QHBoxLayout()
        user_combo_layout.addWidget(user_label)
        user_combo_layout.addWidget(self.user_combo)
        user_combo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        manage_user_layout.addLayout(user_combo_layout)

        self.role_combo_manage = QComboBox()
        roles_label = QLabel("Rolle:")
        self.role_combo_manage.setFixedWidth(150)
        self.role_combo_manage.setFixedHeight(30)
        roles_label.setFixedWidth(150)
        roles_label.setFixedHeight(30)

        role_combo_layout = QHBoxLayout()
        role_combo_layout.addWidget(roles_label)
        role_combo_layout.addWidget(self.role_combo_manage)
        role_combo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        manage_user_layout.addLayout(role_combo_layout)

        self.password_edit_manage = QLineEdit()
        self.password_edit_manage.setEchoMode(QLineEdit.Password)
        password_label = QLabel("Passwort ändern:")
        self.password_edit_manage.setFixedWidth(150)
        self.password_edit_manage.setFixedHeight(30)
        password_label.setFixedWidth(150)
        password_label.setFixedHeight(30)

        password_layout = QHBoxLayout()
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_edit_manage)
        password_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        manage_user_layout.addLayout(password_layout)

        self.confirm_password_manage = QLineEdit()
        self.confirm_password_manage.setEchoMode(QLineEdit.Password)
        password_confirm_label = QLabel("Passwort bestätigen:")
        self.confirm_password_manage.setFixedWidth(150)
        self.confirm_password_manage.setFixedHeight(30)
        password_confirm_label.setFixedWidth(150)
        password_confirm_label.setFixedHeight(30)

        password_confirm_layout = QHBoxLayout()
        password_confirm_layout.addWidget(password_confirm_label)
        password_confirm_layout.addWidget(self.confirm_password_manage)
        password_confirm_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        manage_user_layout.addLayout(password_confirm_layout)

        self.save_button = QPushButton("Speichern")
        self.delete_button = QPushButton("Benutzer löschen")
        self.save_button.setFixedWidth(150)
        self.save_button.setFixedHeight(40)
        self.delete_button.setFixedWidth(150)
        self.delete_button.setFixedHeight(40)

        manage_buttons_layout = QHBoxLayout()
        manage_buttons_layout.addWidget(self.save_button)
        manage_buttons_layout.addWidget(self.delete_button)
        manage_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        manage_user_layout.addLayout(manage_buttons_layout)

        tab_widget.addTab(manage_user_tab, "Benutzer bearbeiten")

        # Create User tab
        create_user_tab = QWidget()
        create_user_layout = QVBoxLayout(create_user_tab)

        self.create_user_line = QLineEdit()
        create_user_label = QLabel("Benutzer:")
        self.create_user_line.setFixedWidth(150)
        self.create_user_line.setFixedHeight(30)
        create_user_label.setFixedWidth(150)
        create_user_label.setFixedHeight(30)

        create_user_line_layout = QHBoxLayout()
        create_user_line_layout.addWidget(create_user_label)
        create_user_line_layout.addWidget(self.create_user_line)
        create_user_line_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        create_user_layout.addLayout(create_user_line_layout)

        self.role_combo_create = QComboBox()
        self._load_roles()
        roles_create_label = QLabel("Rolle:")
        self.role_combo_create.setFixedWidth(150)
        self.role_combo_create.setFixedHeight(30)
        roles_create_label.setFixedWidth(150)
        roles_create_label.setFixedHeight(30)

        role_create_combo_layout = QHBoxLayout()
        role_create_combo_layout.addWidget(roles_create_label)
        role_create_combo_layout.addWidget(self.role_combo_create)
        role_create_combo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        create_user_layout.addLayout(role_create_combo_layout)

        self.password_edit_create = QLineEdit()
        self.password_edit_create.setEchoMode(QLineEdit.Password)
        password_create_label = QLabel("Passwort:")
        self.password_edit_create.setFixedWidth(150)
        self.password_edit_create.setFixedHeight(30)
        password_create_label.setFixedWidth(150)
        password_create_label.setFixedHeight(30)

        password_create_layout = QHBoxLayout()
        password_create_layout.addWidget(password_create_label)
        password_create_layout.addWidget(self.password_edit_create)
        password_create_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        create_user_layout.addLayout(password_create_layout)

        self.confirm_password_create = QLineEdit()
        self.confirm_password_create.setEchoMode(QLineEdit.Password)
        password_confirm_create_label = QLabel("Passwort bestätigen:")
        self.confirm_password_create.setFixedWidth(150)
        self.confirm_password_create.setFixedHeight(30)
        password_confirm_create_label.setFixedWidth(150)
        password_confirm_create_label.setFixedHeight(30)

        password_confirm_create_layout = QHBoxLayout()
        password_confirm_create_layout.addWidget(password_confirm_create_label)
        password_confirm_create_layout.addWidget(self.confirm_password_create)
        password_confirm_create_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        create_user_layout.addLayout(password_confirm_create_layout)

        self.create_button = QPushButton("Benutzer erstellen")
        self.create_button.setFixedWidth(150)
        self.create_button.setFixedHeight(40)

        create_buttons_layout = QHBoxLayout()
        create_buttons_layout.addWidget(self.create_button)
        create_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        create_user_layout.addLayout(create_buttons_layout)

        tab_widget.addTab(create_user_tab, "Benutzer erstellen")

        manage_users_group.setStyleSheet(MANAGE_USER_SECTION)

        layout.addWidget(manage_users_group, 1, 0)  # Row 1, Column 0

        # === Changelog Section ===
        logs_group = QGroupBox("Änderungsprotokoll")
        logs_layout = QVBoxLayout(logs_group)

        log_tab = QTabWidget()
        logs_layout.addWidget(log_tab)

        self.user_logs_tab = QTextEdit()
        self.user_logs_tab.setReadOnly(True)
        log_tab.addTab(self.user_logs_tab, 'Benutzer Protokoll')

        self.partner_logs_tab = QTextEdit()
        self.partner_logs_tab.setReadOnly(True)
        log_tab.addTab(self.partner_logs_tab, 'Partner Protokoll')

        self.ors_logs_tab = QTextEdit()
        self.ors_logs_tab.setReadOnly(True)
        log_tab.addTab(self.ors_logs_tab, 'ORS Statistik')

        self._refresh_logs()
        logs_group.setStyleSheet(LOG_SECTION)

        layout.addWidget(logs_group, 1, 1)  # Row 1, Column 1

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)

    # password section might get deleted
    def _change_password(self):
        """Password change process"""
        current_password = self.current_password_edit.text()
        new_password = self.new_password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        validation_error = self._validate_password_inputs(current_password, new_password, confirm_password)
        if validation_error:
            self._show_message("Warnung", validation_error, QMessageBox.Icon.Warning)
            return

        try:
            self._perform_password_change(current_password, new_password)
            self._show_message("Erfolg", "Passwort erfolgreich geändert.", QMessageBox.Icon.Information)
            self.handle_logout()
        except Exception as e:
            self._show_message("Fehler", str(e), QMessageBox.Icon.Critical)

    def _validate_password_inputs(self, current_password, new_password, confirm_password):
        """Validate user password inputs"""
        if not current_password or not new_password or not confirm_password:
            return "Alle Felder müssen ausgefüllt sein."
        if new_password != confirm_password:
            return "Passwörter stimmen nicht überein."
        return None

    def _perform_password_change(self, current_password, new_password):
        """Change password"""
        authenticated, message = self.auth_manager.authenticate_user(self.auth_manager.get_current_user(),
                                                                     current_password)
        if not authenticated:
            raise Exception(message)

        try:
            success, success_message = self.db.update_password(self.auth_manager.get_current_user(), new_password)
            if not success:
                raise Exception(success_message)

            self.auth_manager.logout()
            self.db.close_connection()
        except Exception as e:
            raise Exception(f"Fehler: {str(e)}.")

    def _show_message(self, title, message, icon):
        """Displays a message box with the given title & message"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
    # end of password section

    def _create_snapshot(self):
        """Snapshot of the selected collection in JSON format"""
        collection_name = self.snapshot_collection_cb.currentText()
        if not collection_name:
            QMessageBox.warning(self, "Warnung", "Bitte wählen Sie eine Sammlung aus.")
            return

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Speichern unter", "", "JSON Files (*.json);;All Files (*)",
                                                   options=options)
        if not file_name:
            return

        try:
            collection = self.db.db[collection_name]
            data = list(collection.find({}))

            for document in data:
                document['_id'] = str(document['_id'])

            with open(file_name, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            QMessageBox.information(self, "Snapshot erstellt",
                                    f"Die Sammlung '{collection_name}' wurde erfolgreich als JSON gespeichert.")
            self.logger.log_user_action(self.current_user, "created backup file of: ", collection_name)
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Erstellen des Snapshots: {str(e)}")

    def _load_collections(self):
        """Load all collections from the current database into the combo box"""
        try:
            collections = self.db.db.list_collection_names()
            self.snapshot_collection_cb.addItems(collections)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fehler beim Laden der Sammlungen: {str(e)}")

    def _upload_data(self):
        """Upload data from JSON file to the specified collection"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Datei auswählen", "", "JSON Files (*.json);;All Files (*)",
                                                   options=options)
        if not file_name:
            return

        collection_name = self.snapshot_collection_cb.currentText()
        if not collection_name:
            QMessageBox.warning(self, "Warnung", "Bitte wählen Sie eine Sammlung aus.")
            return

        try:
            with open(file_name, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            collection = self.db.db[collection_name]

            if collection.count_documents({}) > 0:
                collection.delete_many({})

            if isinstance(data, list):
                for document in data:
                    # Convert _id to ObjectId if it exists
                    if '_id' in document and isinstance(document['_id'], str):
                        document['_id'] = ObjectId(document['_id'])

                collection.insert_many(data)
            else:
                if '_id' in data and isinstance(data['_id'], str):
                    data['_id'] = ObjectId(data['_id'])
                collection.insert_one(data)

            QMessageBox.information(self, "Erfolg",
                                    f"Die Daten wurden erfolgreich in die Sammlung '{collection_name}' hochgeladen.")
            self._load_partners()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Hochladen der Daten: {str(e)}")

    def _load_users(self):
        """Load database users"""
        try:
            users = self.db.load_users()
            self.user_combo.clear()

            for user in users:
                self.user_combo.addItem(user)

        except Exception as e:
            print(f"Error loading database users: {e}")

    def _load_roles(self):
        """Populate roles combobox"""
        roles = ['Admin', 'Gast']
        self.role_combo_create.clear()
        self.role_combo_manage.clear()

        for role in roles:
            self.role_combo_create.addItem(role)
            self.role_combo_manage.addItem(role)

    def _create_user(self):
        """Create a new user with the specified role and password"""
        username = self.create_user_line.text()
        new_role = self.role_combo_create.currentText()
        new_password = self.password_edit_create.text()
        confirm_password = self.confirm_password_create.text()

        if not new_password or not confirm_password or not username:
            QMessageBox.warning(self, "Fehler", "Bitte füllen Sie alle Felder aus.")
            self.create_user_line.clear()
            self.password_edit_create.clear()
            self.confirm_password_create.clear()
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Fehler", "Passwörter stimmen nicht überein.")
            self.password_edit_create.clear()
            self.confirm_password_create.clear()
            return

        role_mapping = {
            'Admin': 'dbOwner',
            'Gast': 'readWrite'
        }
        actual_role = role_mapping.get(new_role)

        if not actual_role:
            QMessageBox.warning(self, "Fehler", "Ungültige Rolle ausgewählt.")
            return

        roles = [actual_role]

        try:
            self.db_queries.create_database_user(username, new_password, roles)
            QMessageBox.information(self, "Erfolg", f"Benutzer {username} erfolgreich erstellt.")
            self._load_users()
            self.logger.log_user_action(self.current_user, "erstellt", username)
            self._refresh_logs()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Erstellen des Benutzers: {str(e)}")
        self.create_user_line.clear()
        self.password_edit_create.clear()
        self.confirm_password_create.clear()

    def _update_user(self):
        """Update selected user (role & password)"""
        selected_user = self.user_combo.currentText()
        new_role = self.role_combo_manage.currentText()
        new_password = self.password_edit_manage.text()
        confirm_password = self.confirm_password_manage.text()

        if not new_password or not confirm_password:
            QMessageBox.warning(self, "Fehler", "Bitte füllen Sie beide Passwort Felder aus.")
            self.password_edit_manage.clear()
            self.confirm_password_manage.clear()
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Fehler", "Passwörter stimmen nicht überein.")
            self.password_edit_manage.clear()
            self.confirm_password_manage.clear()
            return

        role_mapping = {
            'Admin': 'dbOwner',
            'Gast': 'readWrite'
        }
        actual_role = role_mapping.get(new_role)

        if not actual_role:
            QMessageBox.warning(self, "Fehler", "Ungültige Rolle ausgewählt.")
            return

        roles = [actual_role]

        try:
            self.db_queries.update_database_user(selected_user, new_password, roles)
            QMessageBox.information(self, "Erfolg", f"Benutzer {selected_user} erfolgreich aktualisiert.")
            self.logger.log_user_action(self.current_user, "aktualisiert", selected_user)
            self._refresh_logs()

            if self.current_user == selected_user:
                self.handle_logout()

        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Aktualisieren des Benutzers: {str(e)}")
        self.password_edit_manage.clear()
        self.confirm_password_manage.clear()

    def _delete_user(self):
        """Delete selected user"""
        selected_user = self.user_combo.currentText()

        if not selected_user:
            QMessageBox.warning(self, "Fehler", "Bitte wählen Sie einen Benutzer aus.")
            return

        try:
            self.db_queries.delete_database_user(selected_user)
            QMessageBox.information(self, "Erfolg", f"Benutzer {selected_user} erfolgreich gelöscht.")
            self.logger.log_user_action(self.current_user, "gelöscht", selected_user)
            self._refresh_logs()

            if self.current_user == selected_user:
                self.handle_logout()
            else:
                self._load_users()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Löschen des Benutzers: {str(e)}")

    def _prompt_for_password_and_create_user(self):
        """Dialog to authorize current user for requested action (create)"""
        entered_password, ok = QInputDialog.getText(self, "Passwort erforderlich", "Bitte geben Sie Ihr Passwort ein:",
                                                    QLineEdit.EchoMode.Password)

        if ok and entered_password:
            success, message = self.auth_manager.authenticate_user(self.current_user, entered_password)
            if not success:
                QMessageBox.warning(self, "Fehler", message)
                return

            self._create_user()

    def _prompt_for_password_and_update_user(self):
        """Dialog to authorize current user for requested action (update)"""
        entered_password, ok = QInputDialog.getText(self, "Passwort erforderlich", "Bitte geben Sie Ihr Passwort ein:",
                                                    QLineEdit.EchoMode.Password)

        if ok and entered_password:
            success, message = self.auth_manager.authenticate_user(self.current_user, entered_password)
            if not success:
                QMessageBox.warning(self, "Fehler", message)
                return

            self._update_user()

    def _prompt_for_password_and_delete_user(self):
        """Dialog to authorize current user for requested action (delete)"""
        entered_password, ok = QInputDialog.getText(self, "Passwort erforderlich", "Bitte geben Sie Ihr Passwort ein:",
                                                    QLineEdit.EchoMode.Password)

        if ok and entered_password:
            success, message = self.auth_manager.authenticate_user(self.current_user, entered_password)
            if not success:
                QMessageBox.warning(self, "Fehler", message)
                return

            self._delete_user()

    def _redirect_to_login(self):
        """Redirects to login page"""
        from App_Login.login import LoginWindow
        if MainWindow._login_window_instance is None or not MainWindow._login_window_instance.isVisible():
            MainWindow._login_window_instance = LoginWindow()
            MainWindow._login_window_instance.show()
        else:
            MainWindow._login_window_instance.raise_()

        self.close()

    def _refresh_logs(self):
        """Load latest logs"""
        self._display_user_logs()
        self._display_partner_logs()
        self._display_ors_logs()

    def _display_user_logs(self):
        """get & set user logs"""
        logs = self.db.get_collection("Änderungsprotokoll").find({"type": "user"})
        user_logs_text = ""

        for log in logs:
            timestamp = log['timestamp'].strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            action = log['action']
            user = log['user']
            target = log['target']

            # Color coding based on action
            if action == "erstellt":
                action_color = "green"
            elif action == "aktualisiert":
                action_color = "blue"
            elif action == "gelöscht":
                action_color = "red"
            else:
                action_color = "black"

            user_logs_text += f'<span>{timestamp}: <b>{user}</b> hat <b>{target}</b> <span style="color: {action_color};">{action}</span></span><br>'

        self.user_logs_tab.setHtml(user_logs_text)

    def _display_partner_logs(self):
        """get & set partner logs"""
        logs = self.db.get_collection("Änderungsprotokoll").find({"type": "partner"})
        partner_logs_text = ""

        for log in logs:
            timestamp = log['timestamp'].strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            action = log['action']
            user = log['user']
            target = log['target']

            # Color coding based on action
            if action == "erstellt":
                action_color = "green"
            elif action == "aktualisiert":
                action_color = "blue"
            elif action == "gelöscht":
                action_color = "red"
            else:
                action_color = "black"

            partner_logs_text += f'<span>{timestamp}: <b>{user}</b> hat <b>{target}</b> <span style="color: {action_color};">{action}</span></span><br>'

        self.partner_logs_tab.setHtml(partner_logs_text)

    def _display_ors_logs(self):
        """ORS 'logs' to show a history of daily usage"""
        logs = self.db.get_collection("Änderungsprotokoll").find({"type": "ors"})
        ors_logs_text = ""

        for log in logs:
            timestamp = log['timestamp']
            ors = log['ors_usage_count']
            ors_logs_text += f'<span>{timestamp}: {ors}</span><br>'

        self.ors_logs_tab.setHtml(ors_logs_text)

    def _init_settings_page_signals(self):
        """Initialize settings page signals"""
        self.save_button.clicked.connect(self._prompt_for_password_and_update_user)
        self.create_button.clicked.connect(self._prompt_for_password_and_create_user)
        self.delete_button.clicked.connect(self._prompt_for_password_and_delete_user)

    # === Event Handlers ===
    def resizeEvent(self, event):
        """Handle window resize events"""
        super().resizeEvent(event)

        # widget_main
        content_width = self.width() - 60
        content_height = self.height()
        self.widget_main.setGeometry(QRect(60, 0, content_width, content_height))

        # icon menu
        self.widget_icons.setGeometry(QRect(0, 0, 60, content_height))
        self.layoutWidget.setGeometry(QRect(0, 0, 60, content_height))

        # filter frame
        self.frame_Filter.setGeometry(QRect(10, 10, 180, content_height - 20))
        self.widget.setGeometry(QRect(10, 20, 160, content_height - 40))
        frame_height = self.height() - 20
        self.frame_Filter.setGeometry(QRect(10, 10, 180, frame_height))
        self.widget.setGeometry(5, 5, 170, frame_height - 10)

        # expandable menu
        if hasattr(self, 'is_menu_expanded'):
            menu_x = 0 if self.is_menu_expanded else -180
            self.widget_menu.setGeometry(menu_x, 0, 180, content_height)
            self.layoutWidget1.setGeometry(QRect(0, 0, 180, content_height))

        # overlay
        if hasattr(self, 'overlay'):
            self.overlay.setGeometry(self.widget_main.rect())

        # status label
        if hasattr(self, 'status_label') and self.status_label.isVisible():
            label_width = 250
            label_height = 40
            x = (self.tableView.width() - label_width) // 2
            y = (self.tableView.height() - label_height) // 2
            self.status_label.setGeometry(x, y, label_width, label_height)

    def _toggle_password_visibility(self, line_edit, button):
        """Toggle password visibility"""
        if button.isChecked():
            line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setText("👁️")
        else:
            line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            button.setText("🙈")
