# from three_digit_iterator import ThreeDigitFormatter
# import helper_web
# from mutagen.easyid3 import EasyID3

# class AudioDownloader:
#     def __init__(self, download_dir, recitors_list, surah_range):
#         self.download_dir = download_dir
#         self.recitors_list = recitors_list
#         self.surah_range = surah_range
#         self.results = []
    
#     def _generate_url(self, recitor, surah_number):
#         return f"https://download.quranicaudio.com/quran/{recitor}/{surah_number}.mp3"
    
#     def download_surahs(self):
#         for recitor in self.recitors_list:
#             for surah in ThreeDigitFormatter(self.surah_range):
#                 download_result = helper_web.download_file(self._generate_url(recitor, surah), recitor, self.download_dir)
#                 self.results.append(download_result)
#         return self.results
    


# from three_digit_iterator import ThreeDigitFormatter
# import helper_web
# from mutagen.easyid3 import EasyID3

# class AudioDownloader:
#     def __init__(self, download_dir, recitors_list, surah_selection):
#         self.download_dir = download_dir
#         self.recitors_list = recitors_list
#         self.surah_selection = self._prepare_surahs(surah_selection)
#         self.results = []
    
#     def _prepare_surahs(self, surah_selection):
#         """
#         Parses the surah input to create a single list of numbers to iterate over.
#         Handles single surahs (int), ranges (tuple), or lists of surahs.
#         """
#         surahs_to_download = []
#         if isinstance(surah_selection, int):
#             surahs_to_download.append(surah_selection)
#         elif isinstance(surah_selection, tuple) and len(surah_selection) == 2:
#             start, end = surah_selection
#             if start > end:
#                 raise ValueError("Start of range cannot be greater than the end.")
#             surahs_to_download.extend(range(start, end + 1))
#         elif isinstance(surah_selection, list):
#             surahs_to_download = surah_selection
#         else:
#             raise ValueError("surah_selection must be a single integer, a tuple of two integers, or a list of integers.")
        
#         return surahs_to_download
    
#     def _generate_url(self, recitor, surah_number):
#         # We need the surah number to be formatted with three digits (e.g., 001)
#         formatted_surah = f"{surah_number:03d}"
#         return f"https://download.quranicaudio.com/quran/{recitor}/{surah_number}.mp3"
    
#     def download_surahs(self):
#         for recitor in self.recitors_list:
#             for surah in self.surah_selection:
#                 download_result = helper_web.download_file(self._generate_url(recitor, surah), recitor, self.download_dir)
#                 self.results.append(download_result)
#         return self.results
    

import helper_web
from mutagen.easyid3 import EasyID3

class AudioDownloader:
    def __init__(self, download_dir, recitors_list, surah_selection):
        self.download_dir = download_dir
        self.recitors_list = recitors_list
        self.surah_selection = self._prepare_surahs(surah_selection)
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
            surahs_to_download = surah_selection
        else:
            raise ValueError("surah_selection must be a single integer, a tuple of two integers, or a list of integers.")
        
        return surahs_to_download
    
    def _generate_url(self, recitor, surah_number):
        # Apply the :03d format specifier to ensure a three-digit number
        formatted_surah = f"{surah_number:03d}"
        return f"https://download.quranicaudio.com/quran/{recitor}/{formatted_surah}.mp3"
    
    def download_surahs(self):
        for recitor in self.recitors_list:
            # Iterate directly over the list of surahs prepared in __init__
            for surah_number in self.surah_selection:
                download_result = helper_web.download_file(self._generate_url(recitor, surah_number), recitor, self.download_dir)
                self.results.append(download_result)
        return self.results