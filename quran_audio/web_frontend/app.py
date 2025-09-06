from flask import Flask, render_template, request
import subprocess
import json
import shlex

app = Flask(__name__)

# Load recitor data from the JSON file
try:
    with open('reciter_names.json', 'r', encoding='utf-8') as f:
        recitor_data = json.load(f)
    
    # Process the data to include additional information in the display name
    AVAILABLE_RECITORS = {}
    for recitor in recitor_data:
        stored_name = recitor['stored_name']
        formatted_name = recitor['formatted_name']
        
        # Check for other keys like 'recitation_style'
        extra_info = [v for k, v in recitor.items() if k not in ['stored_name', 'formatted_name']]
        
        if extra_info:
            display_name = f"{formatted_name} ({', '.join(extra_info)})"
        else:
            display_name = formatted_name
            
        AVAILABLE_RECITORS[stored_name] = display_name
        
except FileNotFoundError:
    print("Error: The reciter_names.json file was not found. Please ensure it is in the same directory.")
    AVAILABLE_RECITORS = {}

# Load surah data from the JSON file
try:
    with open('quran_surahs.json', 'r', encoding='utf-8') as f:
        surah_data = json.load(f)
    SURAHS = {surah['id']: f"{surah['name']} ({surah['englishName']})" for surah in surah_data}
except FileNotFoundError:
    print("Error: The quran_surahs.json file was not found. Please ensure it is in the same directory.")
    SURAHS = {}

@app.route("/", methods=["GET", "POST"])
def index():
    report = None
    if request.method == "POST":
        recitors = request.form.get("recitors")
        selected_surahs = request.form.getlist("surahs")
        download_dir = request.form.get("download_dir")

        if recitors and selected_surahs and download_dir:
            try:
                surahs_str = ",".join(selected_surahs)
                
                command = [
                    "python", 
                    "downloader_script.py", 
                    "--recitors", recitors, 
                    "--surahs", surahs_str, 
                    "--dir", download_dir
                ]
                
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=True
                )
                report = result.stdout
            except subprocess.CalledProcessError as e:
                report = f"Error: The download script failed to run. {e.stderr}"
            except FileNotFoundError:
                report = "Error: The downloader_script.py file was not found. Please check the file path."
    
    return render_template("index.html", report=report, recitors=AVAILABLE_RECITORS, surahs=SURAHS)

if __name__ == "__main__":
    app.run(debug=True)