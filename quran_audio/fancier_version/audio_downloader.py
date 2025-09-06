import helper_web

# Note: Mutagen.easyid3 is not used in the current implementation.

class AudioDownloader:
    def __init__(self, download_dir, recitors_list, surah_selection, surah_data, recitor_data):
        self.download_dir = download_dir
        self.recitors_list = recitors_list
        self.surah_selection = self._prepare_surahs(surah_selection)
        self.surah_data = surah_data
        self.recitor_data = recitor_data
        self.results = []
    
    def _prepare_surahs(self, surah_selection):
        """
        Parses the surah input to create a single list of numbers to iterate over.
        Handles single surahs (int), ranges (tuple), or lists of surahs.
        """
        surahs_to_download = []
        if isinstance(surah_selection, int):
            surahs_to_download.append(surah_selection)
        elif isinstance(surah_selection, tuple) and len(surah_selection) == 2:
            start, end = surah_selection
            if start > end:
                raise ValueError("Start of range cannot be greater than the end.")
            surahs_to_download.extend(range(start, end + 1))
        elif isinstance(surah_selection, list):
            surahs_to_download = [int(s) for s in surah_selection]
        else:
            raise ValueError("surah_selection must be a single integer, a tuple of two integers, or a list of integers.")
        
        return surahs_to_download
    
    def _generate_url(self, recitor, surah_number):
        # Format the surah number to a three-digit string with leading zeros
        formatted_surah = f"{surah_number:03d}"
        return f"https://download.quranicaudio.com/quran/{recitor}/{formatted_surah}.mp3"
    
    def download_surahs(self):
        for recitor_key in self.recitors_list:
            for surah_number in self.surah_selection:
                surah_name_display = self.surah_data.get(str(surah_number), "Unknown")
                recitor_name_display = self.recitor_data.get(recitor_key, "Unknown")
                
                # Generate the specific download URL and formatted surah name
                formatted_surah = f"{surah_number:03d}"
                url = self._generate_url(recitor_key, surah_number)
                
                # Call the helper function to perform the actual download
                download_result = helper_web.download_file(
                    url, 
                    recitor_key, 
                    self.download_dir, 
                    formatted_surah,
                    recitor_name_display
                )
                self.results.append(download_result)
        return self.results
