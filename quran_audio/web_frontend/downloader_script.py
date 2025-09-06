import sys
import argparse
from AudioDownloader import AudioDownloader

def main():
    parser = argparse.ArgumentParser(description="Download audio surahs based on user input.")
    parser.add_argument("--recitors", required=True, help="Recitor to download.")
    parser.add_argument("--surahs", required=True, help="Comma-separated list of surah numbers.")
    parser.add_argument("--dir", required=True, help="Local download directory.")
    
    args = parser.parse_args()

    # Process recitors
    list_of_recitors = [args.recitors]
    
    # Process surahs (comma-separated list)
    surahs_to_download = [int(s) for s in args.surahs.split(',')]

    # Perform the download
    audio = AudioDownloader(args.dir, list_of_recitors, surahs_to_download)
    result = audio.download_surahs()

    for file_download in result:
        print(file_download)

if __name__ == "__main__":
    main()