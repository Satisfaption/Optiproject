import subprocess
import sys
import time

import requests
import hashlib
import os
import yaml
from utils.config import latest_url
from packaging import version
from PySide6.QtWidgets import (QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


def get_latest_version_info(parent=None):
    try:
        response = requests.get(latest_url)
        response.raise_for_status()
        release_info = response.json()

        # find latest.yaml
        version_asset = next(
            (asset for asset in release_info.get('assets', []) if asset.get('name') == 'latest.yml'),
            None
        )
        if not version_asset:
            raise ValueError("Asset 'latest.yml' konnte nicht gefunden werden.")

        # parse latest.yaml
        version_response = requests.get(version_asset['browser_download_url'])
        version_response.raise_for_status()
        version_info = yaml.safe_load(version_response.text)

        if not isinstance(version_info, dict):
            raise ValueError("Inhalt der latest.yml-Datei fehlerhaft.")

        return version_info

    except (requests.RequestException, yaml.YAMLError, ValueError) as e:
        show_info(parent, "Update Information", f"Update Check fehlgeschlagen:\n{e}")
        return None

def get_current_version():
    from utils.version import __version__
    return __version__

def check_for_updates():
    latest_version_info = get_latest_version_info()
    if not latest_version_info:
        sys.exit(0)

    try:
        current_version = version.parse(get_current_version())
        latest_version = version.parse(latest_version_info['version'])

        if latest_version > current_version:
            return latest_version_info
        else:
            #print("No update available. You're on the latest version.")
            return None
    except Exception as e:
        #print(f"Error comparing versions: {e}")
        return None

def prepare_for_update(version_info, parent=None):
    current_executable = sys.executable

    if not current_executable.lower().endswith(".exe") or "python" in os.path.basename(current_executable).lower():
        show_info(parent, "Update Error", "development mode blocker for me")
        sys.exit(0)

    backup_executable = current_executable.replace(".exe", "_old.exe")

    try:
        # rename running executable
        os.rename(current_executable, backup_executable)
        #print(f"Renamed current executable to: {backup_executable}")
    except OSError as e:
        show_info(parent, "Update Fehlgeschlagen", f"Alte Datei konnte nicht umbenannt werden: \n{e}")
        sys.exit(0)

    new_file = download_update(version_info, current_executable, parent)

    if new_file is None:
        # Roll back
        try:
            os.rename(backup_executable, current_executable)
            #print(f"Reverted to original executable: {current_executable}")
        except OSError as e:
            show_info(parent, "Update Fehlgeschlagen", f"Wiederherstellen des Ursprungsnamen fehlgeschlagen: \n{e}")
        sys.exit(0)

def download_update(version_info, target_file, parent=None):
    url = f"{version_info['files'][0]['url']}"
    expected_sha512 = version_info['files'][0]['sha512']

    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(target_file, "wb") as file:
            file.write(response.content)

        # verify file integrity
        sha512_hash = hashlib.sha512()
        with open(target_file, "rb") as file:
            for byte_block in iter(lambda: file.read(4096), b""):
                sha512_hash.update(byte_block)

        if sha512_hash.hexdigest().lower() != expected_sha512.lower():
            os.remove(target_file)  # Clean up corrupted file
            show_info(parent, "Update Fehlgeschlagen", "Prüfsumme der Datei stimmt nicht überein.\nDatei beschädigt oder manipuliert.")
            return None
        return target_file
    except requests.exceptions.RequestException as e:
        show_info(parent, "Update Fehlgeschlagen", f"Fehler beim Download der Datei: {e}")
        return None
    except OSError as e:
        show_info(parent, "Update Fehlgeschlagen", f"Fehler beim Speichern der Datei: {e}")
        return None

def show_info(parent, title, message):
    error_dialog = QDialog(parent)
    error_dialog.setWindowTitle(title)
    layout = QVBoxLayout(error_dialog)

    label = QLabel(message)
    font = QFont()
    font.setPointSize(12)
    label.setFont(font)
    layout.addWidget(label)

    button_layout = QHBoxLayout()

    button = QPushButton("OK")
    button.setFixedSize(80, 30)
    button.clicked.connect(error_dialog.accept)
    button_layout.addWidget(button)

    layout.addLayout(button_layout)

    error_dialog.setMinimumHeight(120)

    error_dialog.exec()

def cleanup_old_version():
    exe_dir = os.path.dirname(sys.executable)
    old_exe = os.path.join(exe_dir, "Matrix_old.exe")

    if os.path.exists(old_exe):
        try:
            os.remove(old_exe)
            #print("Old version deleted.")
        except Exception as e:
            pass #print(f"Failed to remove old version: {e}")

def prompt_update(parent, on_no_callback, on_ok_callback=None):
    latest_version_info = check_for_updates()
    if latest_version_info:
        update_dialog = QDialog(parent)
        update_dialog.setWindowTitle("Update Information")
        layout = QVBoxLayout(update_dialog)

        label = QLabel(f"Ein Update ist verfügbar. App wird auf Version {latest_version_info['version']} aktualisiert.")
        font = QFont()
        font.setPointSize(12)
        label.setFont(font)
        layout.addWidget(label)

        button_layout = QHBoxLayout()

        button_ok = QPushButton("OK")
        button_ok.setFixedSize(80, 30)
        button_ok.clicked.connect(lambda: on_ok(update_dialog, latest_version_info))
        button_layout.addWidget(button_ok)

        layout.addLayout(button_layout)

        update_dialog.setMinimumHeight(120)

        update_dialog.setWindowModality(Qt.ApplicationModal)
        update_dialog.finished.connect(lambda result: handle_dialog_close(result))
        update_dialog.exec()

def handle_dialog_close(result):
    if result == QDialog.Rejected:
        sys.exit(0)

def on_ok(update_dialog, latest_version_info):
    update_dialog.accept()

    # rename + download
    prepare_for_update(latest_version_info, update_dialog.parent())

    # restart new downloaded version which will run cleanup on startup to delete old one
    show_info(update_dialog.parent(), "Update Information", "Update abgeschlossen. Bitte die neue Datei starten.")
    time.sleep(1)
    sys.exit(0)