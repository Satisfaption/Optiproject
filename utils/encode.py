import hashlib
import yaml
import os
from datetime import datetime, timezone
from utils.config import download_url
from utils.version import __version__


def compute_sha512(file_path):
    """Compute SHA-512 hash of the file"""
    sha512_hash = hashlib.sha512()
    try:
        with open(file_path, "rb") as file:
            for byte_block in iter(lambda: file.read(4096), b""):
                sha512_hash.update(byte_block)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        raise
    return sha512_hash.hexdigest()

def create_yaml(file_path, output_yaml_path):
    """Create a YAML file with specific information."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, file_path)
    output_yaml_path = os.path.join(base_dir, output_yaml_path)

    file_name = os.path.basename(file_path)
    sha512_hash = compute_sha512(file_path)
    file_size = os.path.getsize(file_path)

    release_date = datetime.now(timezone.utc).isoformat()

    version_info = {
        'files': [{
            'sha512': sha512_hash,
            'size': file_size,
            'url': f"{download_url}{file_name}"
        }],
        'path': file_name,
        'releaseDate': release_date,
        'sha512': sha512_hash,
        'version': __version__
    }

    with open(output_yaml_path, 'w') as yml_file:
        yaml.dump(version_info, yml_file, default_flow_style=False)

    print(f"YAML file created: {output_yaml_path}")

file_to_encode = 'dist/Matrix.exe'
output_yaml = 'latest.yml'
create_yaml(file_to_encode, output_yaml)