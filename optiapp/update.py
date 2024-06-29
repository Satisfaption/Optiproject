import subprocess
import time
import requests
import hashlib
import os
import yaml
import customtkinter as ctk
from config import latest_url
from packaging import version


def get_latest_version_info():
    # Assuming the latest.yml file is uploaded as an asset in the latest release
    try:
        response = requests.get(latest_url)
        response.raise_for_status()
        release_info = response.json()

        # Get yml download url
        for asset in release_info['assets']:
            if asset['name'] == 'latest.yml':
                version_url = asset['browser_download_url']
                break
        else:
            raise ValueError("latest.yml not found in release assets")

        # Download the latest.yml content
        response = requests.get(version_url)
        response.raise_for_status()
        version_info = yaml.safe_load(response.text)

        return version_info
    except requests.exceptions.RequestException as e:
        print(f"Error fetching latest version info: {e}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing latest.yml: {e}")
        return None
    except KeyError as e:
        print(f"Key error: {e}")
        return None
    except ValueError as e:
        print(f"Value error: {e}")
        return None


def get_current_version():
    from version import __version__
    return __version__


def check_for_updates():
    latest_version_info = get_latest_version_info()
    if not latest_version_info:
        return

    current_version = get_current_version()
    latest_version = latest_version_info['version']

    if version.parse(latest_version) > version.parse(current_version):
        print(f"Update available: {latest_version}")
        return latest_version_info
    else:
        print("You are using the latest version")


def download_update(version_info):
    url = version_info['files'][0]['url']
    expected_sha512 = version_info['files'][0]['sha512']
    file_name = version_info['path']
    print(url, expected_sha512, file_name)

    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(file_name, "wb") as file:
            file.write(response.content)

        # Verify the file integrity
        sha512_hash = hashlib.sha512()
        with open(file_name, "rb") as file:
            for byte_block in iter(lambda: file.read(4096), b""):
                sha512_hash.update(byte_block)

        if sha512_hash.hexdigest() == expected_sha512:
            print("Update downloaded and verified successfully.")
            return file_name
        else:
            print("Downloaded file is corrupted. Please try again.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading update: {e}")


def show_info(parent, title, message):
    info_window = ctk.CTkToplevel(parent)
    info_window.title(title)
    info_window.geometry("300x150")

    label = ctk.CTkLabel(info_window, text=message, wraplength=280)
    label.pack(pady=20, padx=20)

    button = ctk.CTkButton(info_window, text="OK", command=info_window.destroy)
    button.pack(pady=10)


def show_error(parent, title, message):
    error_window = ctk.CTkToplevel(parent)
    error_window.title(title)
    error_window.geometry("300x150")

    label = ctk.CTkLabel(error_window, text=message, wraplength=280)
    label.pack(pady=20, padx=20)

    button = ctk.CTkButton(error_window, text="OK", command=error_window.destroy)
    button.pack(pady=10)


def restart_application(file_name):
    try:
        # Close the current application
        parent_pid = os.getpid()
        subprocess.Popen(file_name)
        os.kill(parent_pid, 9)
    except Exception as e:
        print(f"Error restarting application: {e}")


def prompt_update(parent, on_no_callback, on_yes_callback=None):
    latest_version_info = check_for_updates()
    if latest_version_info:
        def on_yes():
            time.sleep(0.1)
            update_window.destroy()
            file_name = download_update(latest_version_info)
            if file_name:
                show_info(parent, "Update", "Download abgeschlossen, App startet neu.")
                restart_application(file_name)
            else:
                show_error(parent, "Update", "Fehler beim Download.")
            if on_yes_callback:
                on_yes_callback()

        def on_no():
            time.sleep(0.1)
            update_window.destroy()
            on_no_callback()

        update_window = ctk.CTkToplevel(parent)
        update_window.title("Update Information")
        update_window.geometry("300x150")

        label = ctk.CTkLabel(update_window,
                             text=f"Ein Update ist vorhanden. Möchten Sie auf Version {latest_version_info['version']} aktualisieren?",
                             wraplength=280)
        label.pack(pady=20, padx=20)

        button_yes = ctk.CTkButton(update_window, text="Ja", command=on_yes)
        button_yes.pack(side="left", padx=(20, 10), pady=10)

        button_no = ctk.CTkButton(update_window, text="Nein", command=on_no)
        button_no.pack(side="right", padx=(10, 20), pady=10)

        center_window(update_window, 300, 150)
    else:
        on_no_callback()


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
