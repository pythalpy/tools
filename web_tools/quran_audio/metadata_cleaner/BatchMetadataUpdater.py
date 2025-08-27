import os
import json
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError

class BatchMetadataUpdater:
    def __init__(self, main_directory, album_name="name_static"):
        """
        Initialize the updater for all folders inside a main directory.

        Args:
            main_directory (str): Path containing multiple subfolders with MP3 files.
            album_name (str): Static album name to set for all files.
        """
        self.main_directory = main_directory
        self.album_name = album_name
        self.files_by_folder = {}

    def prepare_file_list(self):
        """
        Collect all MP3 files in each subfolder of main_directory.
        Returns:
            dict: folder_name -> list of MP3 file paths
        """
        self.files_by_folder = {}

        for folder in os.listdir(self.main_directory):
            folder_path = os.path.join(self.main_directory, folder)
            if not os.path.isdir(folder_path):
                continue

            mp3_files = [
                os.path.join(folder_path, f)
                for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(".mp3")
            ]

            if mp3_files:
                self.files_by_folder[folder] = mp3_files

        return self.files_by_folder

    def update_metadata(self):
        """
        Update metadata for all MP3 files in all subfolders.
        Sets the title and artist tags based on the respective JSON files.
        Logs each update as it occurs.
        """
        if not self.files_by_folder:
            self.prepare_file_list()

        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Load Surah data
        quran_surahs = {}
        try:
            with open(os.path.join(script_dir, 'quran_surahs.json'), 'r', encoding='utf-8') as f:
                surahs_list = json.load(f)
                quran_surahs = {str(sura['id']).zfill(3): sura for sura in surahs_list}
        except FileNotFoundError:
            print(f"Error: quran_surahs.json not found at {os.path.join(script_dir, 'quran_surahs.json')}")
            return
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from quran_surahs.json")
            return

        # Load Reciter data
        reciter_info = {}
        try:
            with open(os.path.join(script_dir, 'reciter_names.json'), 'r', encoding='utf-8') as f:
                reciters_list = json.load(f)
                reciter_info = {reciter['stored_name']: reciter for reciter in reciters_list}
        except FileNotFoundError:
            print(f"Error: reciter_names.json not found at {os.path.join(script_dir, 'reciter_names.json')}")
            return
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from reciter_names.json")
            return

        for folder_name, files in self.files_by_folder.items():
            # Determine the artist name based on the folder name
            artist_name = folder_name
            if folder_name in reciter_info:
                reciter_data = reciter_info[folder_name]
                artist_name = reciter_data['formatted_name']
                
                if 'recitation_style' in reciter_data:
                    artist_name += f" ({reciter_data['recitation_style']} recitation)"
                
                if 'translation_language' in reciter_data:
                    # Check for translation reader and translation to apply the new format
                    if 'translation_reader' in reciter_data and 'translation' in reciter_data:
                        translation_part = f" - {reciter_data['translation_reader']}, {reciter_data['translation']}"
                        if reciter_data['translation_language'].lower() == 'english':
                            translation_part += " English Translation"
                        else:
                            translation_part += f" {reciter_data['translation_language']} Translation"
                        artist_name += translation_part
                    else:
                        # Fallback to the old format for translations without a specific reader/style
                        artist_name += f" w {reciter_data['translation_language']} Translation"


            for filepath in files:
                file_log = {
                    "file": filepath,
                    "artist_set": artist_name,
                    "album_set": self.album_name,
                    "status": None,
                    "error": None,
                    "title_set": None
                }
                
                try:
                    try:
                        audio = EasyID3(filepath)
                    except ID3NoHeaderError:
                        audio = ID3()
                        audio.save(filepath)
                        audio = EasyID3(filepath)

                    # Set Artist and Album tags
                    audio["artist"] = artist_name
                    audio["album"] = self.album_name

                    # Set Title tag based on Surah data
                    filename_stem = os.path.splitext(os.path.basename(filepath))[0]
                    if filename_stem in quran_surahs:
                        sura_info = quran_surahs[filename_stem]
                        
                        sura_id = sura_info['id']
                        sura_name = sura_info['name']
                        english_name = sura_info['englishName']
                        revelation_place = sura_info['revelationPlace']
                        number_of_ayahs = sura_info['numberOfAyahs']
                        
                        title = (
                            f"{sura_id:03d} - "
                            f"{sura_name} "
                            f"({english_name}) "
                            f"[{revelation_place}, "
                            f"{number_of_ayahs} ayahs]"
                        )
                        audio["title"] = title
                        file_log["title_set"] = title
                    else:
                        file_log["status"] = "error"
                        file_log["error"] = "No matching surah found in JSON for filename"
                        print(file_log)
                        continue

                    audio.save()
                    file_log["status"] = "updated"
                
                except Exception as e:
                    file_log["status"] = "error"
                    file_log["error"] = str(e)
                
                print(file_log)