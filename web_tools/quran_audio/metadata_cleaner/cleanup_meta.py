from metadata_cleaner import BatchMetadataUpdater

# local_download_directory = "/Volumes/SD2TBSSD/HomeMedia/Audio/Quran/QuranicAudioDL082325"
local_download_directory = "/Volumes/QURAN_AUDIO/Quran"

updater = BatchMetadataUpdater(main_directory=local_download_directory, album_name="Qur'an")

# Prepare file list (optional)
updater.prepare_file_list()

# Update metadata and get log
log = updater.update_metadata()

# Print log
for entry in log:
    print(entry)
