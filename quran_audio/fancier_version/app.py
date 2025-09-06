import os
import requests
import json
from flask import Flask, render_template, request, redirect, url_for
from audio_downloader import AudioDownloader

# Initialize the Flask application
app = Flask(__name__)

# Global variables for data
RECITORS = {}
SURAHS = {}

# --- Function to load data from JSON files ---
def load_data_from_json():
    """
    Loads recitor and surah data from their respective JSON files.
    The files are expected to be in the same directory as this script.
    """
    global RECITORS, SURAHS
    
    # Load recitor names
    recitor_filepath = 'reciter_names.json'
    try:
        with open(recitor_filepath, 'r') as f:
            recitor_data = json.load(f)
            if isinstance(recitor_data, list):
                temp_recitors = {}
                for item in recitor_data:
                    try:
                        # Get the base formatted name
                        formatted_name = item['formatted_name']
                        
                        # Collect all other key-value pairs
                        extra_info = [v for k, v in item.items() if k not in ['stored_name', 'formatted_name']]
                        
                        if extra_info:
                            # Join the extra information into a single string
                            display_name = f"{formatted_name} ({', '.join(extra_info)})"
                        else:
                            display_name = formatted_name
                            
                        # Assign the full display name to the dictionary
                        temp_recitors[item['stored_name']] = display_name
                    except KeyError as e:
                        print(f"KeyError: Missing key {e} in object: {item}. Please check your reciter_names.json file.")
                RECITORS = temp_recitors
            else:
                print(f"Error: The data in '{recitor_filepath}' is not a list.")
        print("Recitor data loaded successfully from reciter_names.json")
    except FileNotFoundError:
        print(f"Error: The file '{recitor_filepath}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{recitor_filepath}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred while loading recitors: {e}")

    # Load surah names
    surah_filepath = 'quran_surahs.json'
    try:
        with open(surah_filepath, 'r') as f:
            surah_data = json.load(f)
            if isinstance(surah_data, list):
                temp_surahs = {}
                for item in surah_data:
                    try:
                        # Now including the English name in the display string
                        temp_surahs[str(item['id'])] = f"{item['name']} ({item['englishName']})"
                    except KeyError as e:
                        print(f"KeyError: Missing key {e} in object: {item}. Please check your quran_surahs.json file.")
                SURAHS = temp_surahs
            else:
                print(f"Error: The data in '{surah_filepath}' is not a list.")
        print("Surah data loaded successfully from quran_surahs.json")
    except FileNotFoundError:
        print(f"Error: The file '{surah_filepath}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{surah_filepath}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred while loading surahs: {e}")

# --- Flask Routes ---
@app.route('/', methods=['GET', 'POST'])
def home():
    report_data = []
    # Check if the request method is POST, which means the form was submitted.
    if request.method == 'POST':
        # Get data from the form
        recitor_key = request.form['recitors']
        surah_numbers = request.form.getlist('surahs') # getlist is used for multiple selections
        download_dir = request.form['download_dir']

        # Validate form input (basic check)
        if not recitor_key or not surah_numbers or not download_dir:
            # For now, let's keep a simple string message for general errors
            # A more advanced version might have a dedicated error section in the report
            report_data = "Error: All fields are required."
        else:
            # Create a dictionary to hold the report for this reciter
            reciter_report = {
                'name': RECITORS.get(recitor_key, "Unknown Reciter"),
                'downloads': []
            }
            
            # Create an instance of the AudioDownloader
            downloader = AudioDownloader(
                download_dir=download_dir,
                recitors_list=[recitor_key],
                surah_selection=surah_numbers,
                surah_data=SURAHS,
                recitor_data=RECITORS
            )
            
            # Run the download process and get the results
            download_results = downloader.download_surahs()

            # Build the report data structure
            for i, surah_number in enumerate(surah_numbers):
                surah_name = SURAHS.get(str(surah_number), "Unknown Surah")
                result_message = download_results[i]
                
                # Append a dictionary for each surah download
                reciter_report['downloads'].append({
                    'surah_name': surah_name,
                    'status': 'success' if 'Successfully downloaded' in result_message else 'failure',
                    'message': result_message
                })
            
            report_data.append(reciter_report)

    # Render the HTML template, passing the data and the report message.
    return render_template('index.html', 
                           recitors=RECITORS, 
                           surahs=SURAHS, 
                           report=report_data)

# This block runs the application in debug mode for development.
if __name__ == '__main__':
    # Load data from JSON files before starting the app
    load_data_from_json()

    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
