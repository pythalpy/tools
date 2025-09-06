import os
import requests

def download_file(url, recitor_key, download_dir, formatted_surah, recitor_name_display):
    """
    Downloads a file from a given URL and saves it to a specified directory.
    
    Args:
        url (str): The URL of the file to download.
        recitor_key (str): The key for the reciter's folder.
        download_dir (str): The base directory to save the file.
        formatted_surah (str): The surah number formatted as a 3-digit string.
        recitor_name_display (str): The display name of the reciter.
        
    Returns:
        str: A message indicating the success or failure of the download.
    """
    
    # Construct the file path and name
    file_name = f"{formatted_surah}.mp3"
    recitor_download_path = os.path.join(download_dir, recitor_key)
    file_path = os.path.join(recitor_download_path, file_name)

    try:
        # Create the recitor directory if it doesn't exist
        os.makedirs(recitor_download_path, exist_ok=True)
    except OSError as e:
        return f"Error creating directory for recitor {recitor_name_display}: {e}"
        
    try:
        # Stream the download to handle large files efficiently
        with requests.get(url, stream=True) as r:
            r.raise_for_status() # Raise an HTTPError if the status is 4xx or 5xx
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return f"Successfully downloaded {file_name} for recitor: {recitor_name_display}"
    except requests.exceptions.RequestException as e:
        return f"Error downloading {file_name}: {e}"
    except IOError as e:
        return f"Error saving {file_name} to disk: {e}"
    except Exception as e:
        return f"An unexpected error occurred during download: {e}"
