from helper_web import fetch_surahs_by_recitor

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
    "sa3d_al-ghaamidi/complete"
    ]

def download_surahs(list_of_recitors, first_surah_number, last_surah_number=None):
    """
    Download The Surahs Needed. 
    # This download tool can only work in conjunction with all of the
    # hard work done by the folks at quranicaudio.com, alhamdulillah,
    # and the simple file management strategy they have chosen.
    # Please be nice to their servers and only download what you need.
    """
    for recitor in list_of_recitors:
        fetch_surahs_by_recitor(recitor, first_surah_number, last_surah_number)

### Download a single surah by a single recitor
download_surahs("mishaari_raashid_al_3afaasee", 36)

### Download a range of surahs by a single recitor (1 through 3)
download_surahs("khalifah_taniji", 1, 3)

### Download a single surah by multiple recitors (Surah Yaseen)
download_surahs(list_of_recitors, 36)

### Download a range of surahs by multiple recitors (Juz Amma)
download_surahs(list_of_recitors, 78, 114)

