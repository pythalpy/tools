import os
import requests
import time
import random
from urllib.parse import urlparse

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

class ThreeDigitFormatter:
    """
    An iterator that generates a range of three-digit numbers with leading zeros.
    """
    def __init__(self, start_value, end_value=None):
        """
        Initializes the iterator with a start and end value.
        If no end_value is provided, it iterates only for the single start_value.
        
        Args:
            start_value (int): The starting number for the sequence.
            end_value (int, optional): The last number in the sequence. 
                                       If None, the sequence contains only start_value.
        """
        self.current_value = start_value - 1
        self.end_value = end_value if end_value is not None else start_value

        if self.current_value >= self.end_value:
            raise ValueError("Start value cannot be greater than or equal to the end value.")
    
    def __iter__(self):
        """
        Returns the iterator object itself.
        """
        return self
    
    def __next__(self):
        """
        Generates the next formatted three-digit number in the sequence.
        """
        self.current_value += 1
        if self.current_value > self.end_value:
            raise StopIteration
        
        return f"{self.current_value:03d}"
    

def download_surahs_by_recitor(recitor, first_surah, last_surah=None):
    surah_number_with_leading_zeros = ThreeDigitFormatter(first_surah, last_surah)
    for surah_number in surah_number_with_leading_zeros:
        file_url = f"https://download.quranicaudio.com/quran/{recitor}/{surah_number}.mp3"
        print(f'attempting to download {file_url}')
        download_file(file_url, recitor)
        sleep_dur = random.random()
        time.sleep(sleep_dur)

list_of_recitors = [
    # Add/Remove/Comment Recitors as Needed
    # Grab recitor name from download url, e.g. https://download.quranicaudio.com/quran/sudais_and_shuraim_with_urdu/034.mp3
    # is 'sudais_and_shuraim_with_urdu'
    "abdullah_basfar_w_ibrahim_walk_si", 
    "noreen_siddiq", 
    "abdul_basit_murattal", 
    "abdulbaset_mujawwad",
    "sudais_and_shuraim_with_urdu", 
    "abdulbaset_with_naeem_sultan_pickthall", 
    "khalifah_taniji",
    "mishaari_raashid_al_3afaasee"
    ]

# This download tool can only work in conjunction with all of the
# hard work done by the folks at quranicaudio.com, alhamdulillah,
# and the simple file management strategy they have chosen.
# Please be nice to their servers and only download what you need.

for recitor in list_of_recitors:
    # Download All Surahs
    download_surahs_by_recitor(recitor, 1, 114)

    # Download a Specific Sura
    # download_surahs_by_recitor(recitor, 67)

    sleep_dur = random.random()*2
    time.sleep(sleep_dur)
