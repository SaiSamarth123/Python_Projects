from pytube import YouTube, Playlist
from moviepy.editor import AudioFileClip
import os


def download_and_convert_to_mp3(yt, download_path):
    try:
        print("Title: ", yt.title)
        print("Number of views: ", yt.views)
        print("Length of video: ", yt.length)

        # Get the video stream
        stream = yt.streams.filter(only_audio=False).first()
        print("Downloading...")

        # Download the file
        mp4_file = stream.download(download_path)
        print("Video is Downloaded.")

        # Convert to MP3
        print("Converting to MP3...")
        mp3_file = mp4_file.replace(".mp4", ".mp3")
        AudioFileClip(mp4_file).write_audiofile(mp3_file)
        os.remove(mp4_file)
        print("Conversion to MP3 completed and MP4 file deleted.")
        return None
    except Exception as e:
        return str(e)


# Ask for the link from user
playlist_url = input("Enter the playlist URL here: ")
if not os.path.exists("downloads"):
    os.makedirs("downloads")

try:
    playlist = Playlist(playlist_url)
    PlayListLinks = playlist.video_urls
    N = len(PlayListLinks)
    print(f"This link found to be a Playlist Link with number of videos equal to {N}")
    print(f"\nLet's Download all {N} videos")

    errors = []
    for i, link in enumerate(PlayListLinks):
        yt = YouTube(link)
        if yt.views >= 100000:
            error = download_and_convert_to_mp3(yt, "music")
            if error:
                print(
                    f"Error downloading {link}, continuing with next video. Error: {error}"
                )
                errors.append((link, error))
        else:
            errors.append((link, "Less views"))

    print("All downloads completed!!")

    if errors:
        print("\nThe following videos encountered errors during download:")
        for link, error in errors:
            print(f"Video {link} gave error: {error}")

except Exception as e:
    print(f"Error processing playlist: {e}")


# from pytube import YouTube
# from moviepy.editor import AudioFileClip
# import os


# def clean_url(url):
#     # Ensure the URL is properly formatted
#     if "youtube.com" in url and "&" in url:
#         url = url.split("&")[0]
#     return url


# # Ask for the video link from the user
# video_url = input("Enter the video URL here: ")
# video_url = clean_url(video_url)

# # Create a directory for downloads if it doesn't exist
# if not os.path.exists("downloads"):
#     os.makedirs("downloads")

# try:
#     yt = YouTube(video_url)
#     print("Title: ", yt.title)
#     print("Number of views: ", yt.views)
#     print("Length of video: ", yt.length)

#     # Get the audio stream
#     stream = yt.streams.filter(only_audio=True).first()
#     print("Downloading...")

#     # Download the file
#     mp4_file = stream.download("downloads")
#     print("Video is Downloaded.")

#     # Convert to MP3
#     print("Converting to MP3...")
#     mp3_file = mp4_file.replace(".mp4", ".mp3")
#     AudioFileClip(mp4_file).write_audiofile(mp3_file)
#     os.remove(mp4_file)
#     print("Conversion to MP3 completed and MP4 file deleted.")

# except Exception as e:
#     print(f"Error downloading {video_url}: {e}")

# print("Download and conversion completed!")
