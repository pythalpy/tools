from AudioDownloader import AudioDownloader

# Specify Recitors
list_of_recitors = [
    # Add/Remove/Comment Recitors as Needed
    "abdullah_basfar_w_ibrahim_walk_si", 
    # "noreen_siddiq", 
    # "abdul_basit_murattal", 
    # "abdulbaset_mujawwad",
    # "sudais_and_shuraim_with_urdu", 
    # "abdulbaset_with_naeem_sultan_pickthall", 
    # "khalifah_taniji",
    # "mishaari_raashid_al_3afaasee",
    # "sa3d_al-ghaamidi/complete",
    ]

# Specify surahs to download
# Can be a single surah, e.g. Sura Yaseen
surahs_to_download = (36)

# Or a range of surahs, e.g. Juz 'Amma (from 78 through 114)
# surahs_to_download = (78, 114)

# Specify Local Download Directory
local_download_directory = "/path/to/download/folder"

# Prepare and Perform the Download
audio = AudioDownloader(local_download_directory, list_of_recitors, surahs_to_download)
result = audio.download_surahs()

# View report of the download
print("\nDownload Report")
for file_download in result:
    print(file_download)
