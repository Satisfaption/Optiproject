import requests
import hashlib
import os
import yaml
from datetime import datetime
from optiapp.config import new_version, filename, download_url


def get_latest_version_info():
    url = "https://raw.githubusercontent.com/username/repository/main/latest.yml"  # change to same as version
    response = requests.get(url)
    version_info = response.text
    return yaml.safe_load(version_info)


def get_current_version():
    from version import __version__
    return __version__


def check_for_updates():
    latest_version_info = get_latest_version_info()
    current_version = get_current_version()

    latest_version = latest_version_info['version']
    if latest_version != current_version:
        print(f"Update available: {latest_version}")
        download_update(latest_version_info)
    else:
        print("You are using the latest version")


def download_update(version_info):
    url = version_info['files'][0]['url']
    expected_sha512 = version_info['files'][0]['sha512']
    file_name = version_info['files'][0]['path']

    response = requests.get(url)
    with open(file_name, "wb") as file:
        file.write(response.content)

    # Verify the file integrity
    sha512_hash = hashlib.sha512()
    with open(file_name, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha512_hash.update(byte_block)

    if sha512_hash.hexdigest() == expected_sha512:
        print("Update downloaded and verified successfully.")
        # Proceed with installation or replacement of old files
        install_update(file_name)
    else:
        print("Downloaded file is corrupted. Please try again.")


def install_update(file_name):
    # Replace old files with the new ones, or run the installer
    os.system(file_name)  # This will run the installer


def calculate_sha512(file_path):
    sha512_hash = hashlib.sha512()
    with open(file_path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha512_hash.update(byte_block)
    return sha512_hash.hexdigest()


def generate_version_file(version, file_path, url):
    file_sha512 = calculate_sha512(file_path)
    file_size = os.path.getsize(file_path)

    release_date = datetime.utcnow().isoformat() + 'Z'

    version_info = {
        'version': version,
        'files': [
            {
                'url': url,
                'sha512': file_sha512,
                'size': file_size
            }
        ],
        'path': os.path.basename(file_path),
        'sha512': file_sha512,
        'releaseDate': release_date
    }

    with open("version.yml", "w") as version_file:
        yaml.dump(version_info, version_file)


generate_version_file(new_version, filename, download_url)
check_for_updates()
