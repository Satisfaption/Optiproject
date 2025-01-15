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

        for asset in release_info['assets']:
            if asset['name'] == 'latest.yml':
                version_url = asset['browser_download_url']
                break
        else:
            raise ValueError("latest.yml not found in release assets")

        response = requests.get(version_url)
        response.raise_for_status()
        version_info = yaml.safe_load(response.text)

        return version_info
    except requests.exceptions.RequestException as e:
        show_error(parent, "Error fetching latest version info", str(e))
        return None
    except yaml.YAMLError as e:
        show_error(parent, "Error parsing latest.yml", str(e))
        return None
    except KeyError as e:
        show_error(parent, "Key error", str(e))
        return None
    except ValueError as e:
        show_error(parent, "Value error", str(e))
        return None

def get_current_version():
    from utils.version import __version__
    return __version__

def check_for_updates():
    latest_version_info = get_latest_version_info()
    if not latest_version_info:
        return

    current_version = get_current_version()
    latest_version = latest_version_info['version']

    if version.parse(latest_version) > version.parse(current_version):
        return latest_version_info

def download_update(version_info):
    url = f"{version_info['files'][0]['url']}"
    expected_sha512 = version_info['files'][0]['sha512']
    file_name, file_ext = os.path.splitext(version_info['path'])
    new_file = f"{file_name}_new{file_ext}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(new_file, "wb") as file:
            file.write(response.content)

        # verify file integrity
        sha512_hash = hashlib.sha512()
        with open(new_file, "rb") as file:
            for byte_block in iter(lambda: file.read(4096), b""):
                sha512_hash.update(byte_block)

        if sha512_hash.hexdigest() == expected_sha512.lower():
            return new_file
        else:
            print("Downloaded file is corrupted. Please try again.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading update: {e}")

def show_info(parent, title, message):
    info_dialog = QDialog(parent)
    info_dialog.setWindowTitle(title)
    layout = QVBoxLayout(info_dialog)

    label = QLabel(message)
    font = QFont()
    font.setPointSize(12)
    label.setFont(font)
    layout.addWidget(label)

    button_layout = QHBoxLayout()

    button = QPushButton("OK")
    button.setFixedSize(80, 30)
    button.clicked.connect(info_dialog.accept)
    button_layout.addWidget(button)

    layout.addLayout(button_layout)

    info_dialog.setMinimumHeight(120)

    info_dialog.exec()

def show_error(parent, title, message):
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

def restart_application(file_name):
    try:
        parent_pid = os.getpid()
        subprocess.Popen(file_name)
        os.kill(parent_pid, 9)
    except Exception as e:
        print(f"Error restarting application: {e}")

def cleanup_old_version():
    current_executable = sys.executable
    file_name, file_ext = os.path.splitext(current_executable)
    original_name = f"{file_name[:-4]}{file_ext}"

    if "_new" in file_name:
        if os.path.exists(original_name):
            try:
                while True:
                    try:
                        os.remove(original_name)
                        print(f"Removed old executable: {original_name}")
                        break
                    except PermissionError:
                        print(f"Old file {original_name} is still in use. Retrying...")
                        time.sleep(1)
            except Exception as e:
                print(f"Failed to remove old executable: {e}")

        try:
            os.rename(current_executable, original_name)
            print(f"Renamed new executable to {original_name}")
        except Exception as e:
            print(f"Failed to rename new executable: {e}")

def prompt_update(parent, on_no_callback, on_ok_callback=None):
    cleanup_old_version()
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
    file_name = download_update(latest_version_info)
    if file_name:
        show_info(update_dialog.parent(), "Update", "Download abgeschlossen, App wird neu gestartet.")
        time.sleep(1)
        restart_application(file_name)
    else:
        show_error(update_dialog.parent(), "Update", "Fehler beim Download.")