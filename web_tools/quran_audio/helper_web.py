import os
import requests
from urllib.parse import urlparse
import time
import random
from helper_string import range_padder


def download_file(url, subfolder_name="downloads"):
    """
    Downloads a file from a URL, infers the filename, and saves it to a
    specified subfolder.

    Args:
        url (str): The URL of the file to download.
        subfolder_name (str): The name of the subfolder to save the file in.
                              Defaults to "downloads".
    """
    try:
        print(f"Starting download from URL: {url}")

        # Extract the filename from the URL
        parsed_url = urlparse(url)
        local_filename = os.path.basename(parsed_url.path)

        if not local_filename:
            print("WARNING: Could not determine a filename from the URL. Aborting.")
            return

        # Create the subfolder if it doesn't exist
        os.makedirs(subfolder_name, exist_ok=True)
        
        # Construct the full path to the file
        full_path = os.path.join(subfolder_name, local_filename)

        # Check if the file already exists
        if os.path.exists(full_path):
            print(f"INFO: File already exists at '{full_path}'. Skipping download.")
            return

        print(f"File does not exist. Saving to: {full_path}")

        # Send a GET request with stream=True
        with requests.get(url, stream=True) as r:
            print("Sending request...")
            r.raise_for_status()

            with open(full_path, 'wb') as f:
                print("Connection established. Starting to write file...")
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"SUCCESS: File downloaded successfully to {full_path}")

    except requests.exceptions.RequestException as e:
        print(f"ERROR: An error occurred during the request: {e}")
    except IOError as e:
        print(f"ERROR: An I/O error occurred: {e}")


def fetch_surahs_by_recitor(recitor, first_surah, last_surah=None):
    surah_number_range = range_padder(first_surah, last_surah)
    for surah_number in surah_number_range:
        file_url = f"https://download.quranicaudio.com/quran/{recitor}/{surah_number}.mp3"
        print(f'attempting to download {file_url}')
        download_file(file_url, recitor)
        sleep_dur = random.random()
        time.sleep(sleep_dur)
    time.sleep(sleep_dur*2)