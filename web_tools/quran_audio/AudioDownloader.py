from three_digit_iterator import ThreeDigitFormatter
import helper_web
from mutagen.easyid3 import EasyID3

class AudioDownloader:
    def __init__(self, download_dir, recitors_list, surah_range):
        self.download_dir = download_dir
        self.recitors_list = recitors_list
        self.surah_range = surah_range
        self.results = []
    
    def _generate_url(self, recitor, surah_number):
        return f"https://download.quranicaudio.com/quran/{recitor}/{surah_number}.mp3"
    
    def download_surahs(self):
        for recitor in self.recitors_list:
            for surah in ThreeDigitFormatter(self.surah_range):
                download_result = helper_web.download_file(self._generate_url(recitor, surah), recitor, self.download_dir)
                self.results.append(download_result)
        return self.results
    