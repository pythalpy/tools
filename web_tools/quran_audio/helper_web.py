import os
import requests
import time
import random
from urllib.parse import urlparse

def download_file(url, subfolder_name, download_directory):
    """
    Downloads a file from a URL, infers the filename, and saves it to a
    specified subfolder inside a base directory.

    Args:
        url (str): The URL of the file to download.
        subfolder_name (str): The name of the subfolder to save the file in.
        download_directory (str): Base directory for downloads.

    Returns:
        dict: {
            "status": "success" | "skipped" | "error",
            "path": str or None,
            "error": str or None,
            "filename": str or None,
        }
    """
    try:
        print(f"Starting download from URL: {url}")

        # Extract the filename from the URL
        parsed_url = urlparse(url)
        local_filename = os.path.basename(parsed_url.path)

        if not local_filename:
            warning_msg = "Could not determine a filename from the URL."
            print(f"WARNING: {warning_msg}")
            return {"status": "error", "path": None, "error": warning_msg, "filename": None}

        # Build dirs
        # Sanitize the subfolder name
        sanitized_subfolder_name = subfolder_name.split('/')[0]
        
        # Build dirs
        subfolder_path = os.path.join(download_directory, sanitized_subfolder_name)
        os.makedirs(subfolder_path, exist_ok=True)

        # Full file path
        full_path = os.path.join(subfolder_path, local_filename)

        # Skip if exists
        if os.path.exists(full_path):
            msg = f"File already exists at '{full_path}'."
            print(f"INFO: {msg}")
            return {"status": "skipped", "path": full_path, "error": None, "filename": local_filename}

        print(f"File does not exist. Saving to: {full_path}")

        # Download
        with requests.get(url, stream=True) as r:
            print("Sending request...")
            r.raise_for_status()

            with open(full_path, 'wb') as f:
                print("Connection established. Writing file...")
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Random sleep to simulate throttling
        sleep_dur = random.random()
        time.sleep(sleep_dur)

        print(f"SUCCESS: File downloaded successfully to {full_path}")
        return {"status": "success", "path": full_path, "error": None, "filename": local_filename}

    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {e}"
        print(f"ERROR: {error_msg}")
        return {"status": "error", "path": None, "error": error_msg, "filename": None}
    except IOError as e:
        error_msg = f"I/O error: {e}"
        print(f"ERROR: {error_msg}")
        return {"status": "error", "path": None, "error": error_msg, "filename": None}
