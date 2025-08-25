import os
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
        self.files_by_folder = {}  # folder_name -> list of full file paths

    def prepare_file_list(self):
        """
        Collect all MP3 files in each subfolder of main_directory.
        Returns:
            dict: folder_name -> list of MP3 file paths
        """
        self.files_by_folder = {}

        # Loop through all subfolders
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
        Sets 'artist' = folder name, 'album' = self.album_name.
        Returns:
            list: log of dictionaries for each file processed
        """
        if not self.files_by_folder:
            self.prepare_file_list()

        log = []

        for folder_name, files in self.files_by_folder.items():
            for filepath in files:
                file_log = {
                    "file": filepath,
                    "artist_set": folder_name,
                    "album_set": self.album_name,
                    "status": None,
                    "error": None
                }

                try:
                    try:
                        audio = EasyID3(filepath)
                    except ID3NoHeaderError:
                        audio = ID3()
                        audio.save(filepath)
                        audio = EasyID3(filepath)

                    # Set tags
                    audio["artist"] = folder_name
                    audio["album"] = self.album_name
                    audio.save()

                    file_log["status"] = "updated"

                except Exception as e:
                    file_log["status"] = "error"
                    file_log["error"] = str(e)

                log.append(file_log)

        return log
