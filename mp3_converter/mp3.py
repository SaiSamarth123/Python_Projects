# from pytube import YouTube, Playlist
# from moviepy.editor import *
# import os
# import re


# def download_video(url):
#     try:
#         youtube = YouTube(url)
#     except Exception as e:
#         print(f"Could not download the video. Reason: {e}")
#         return None

#     video = youtube.streams.first()
#     out_file = video.download()
#     return out_file


# def convert_to_mp3(file_path):
#     try:
#         mp3_file_path = re.sub(r"\.[^.]+$", ".mp3", file_path)
#         mp3_file_path = os.path.join("music", os.path.basename(mp3_file_path))
#         videoclip = VideoFileClip(file_path)
#         audioclip = videoclip.audio
#         audioclip.write_audiofile(mp3_file_path)
#         audioclip.close()
#         videoclip.close()
#     except Exception as e:
#         print(f"Could not convert video to mp3. Reason: {e}")
#         return None

#     return mp3_file_path


# def main():
#     playlist_url = input("Enter the playlist URL here: ")

#     if not os.path.exists("music"):
#         os.makedirs("music")

#     playlist = Playlist(playlist_url)
#     failed_downloads = []
#     for url in playlist.video_urls:
#         file_path = download_video(url)
#         if file_path is not None:
#             mp3_file_path = convert_to_mp3(file_path)
#             if mp3_file_path is not None:
#                 print(
#                     f"Successfully converted video to mp3. File saved at: {mp3_file_path}"
#                 )
#             else:
#                 print("Could not convert video to mp3.")

#             try:
#                 os.remove(file_path)
#             except Exception as e:
#                 print(f"Could not remove original video file. Reason: {e}")

#         else:
#             failed_downloads.append(url)

#     if len(failed_downloads) > 0:
#         print("\nFailed to download the following videos:")
#         for url in failed_downloads:
#             print(url)


# if __name__ == "__main__":
#     main()


from pytube import YouTube, Playlist
from moviepy.editor import *
import os
import re

# ask for the link from user
playlist_url = input("Enter the playlist URL here: ")
if not os.path.exists("music"):
    os.makedirs("music")

playlist = Playlist(playlist_url)

PlayListLinks = playlist.video_urls
N = len(PlayListLinks)
print(f"This link found to be a Playlist Link with number of videos equal to {N} ")
print(f"\n Lets Download all {N} videos")

errors = []
for i, link in enumerate(PlayListLinks):
    try:
        yt = YouTube(link)
        if yt.views >= 100000:
            print("Title: ", yt.title)
            print("Number of views: ", yt.views)
            print("Length of video: ", yt.length)
            stream = yt.streams.get_by_itag(140)
            print("Downloading...")
            mp4_file = stream.download("music")
            print(i + 1, " Video is Downloaded.")
            print("Converting to MP3...")
            mp3_file = mp4_file.replace(".mp4", ".mp3")
            AudioFileClip(mp4_file).write_audiofile(mp3_file)
            os.remove(mp4_file)
            print("Conversion to MP3 completed and MP4 file deleted.")
        errors.append((link, "Less views"))
    except Exception as e:
        print(f"Error downloading {link}, continuing with next video.")
        errors.append((link, str(e)))

print("All downloads completed!!")

if errors:
    print("\nThe following videos encountered errors during download:")
    for link, error in errors:
        print(f"Video {link} gave error: {error}")


# # Showing details
# print("Title: ", yt.title)
# print("Number of views: ", yt.views)
# print("Length of video: ", yt.length)
# print("Rating of video: ", yt.rating)
# # Getting the best version of audio possible
# t = yt.streams.filter(only_audio=True).all()
# ys = yt.streams.get_highest_resolution()

# # Starting download
# print("Downloading...")
# t[0].download("music")
# print("Download completed!!")


# from pytube import Playlist
# playlist = Playlist('https://www.youtube.com/playlist?list=PLwdnzlV3ogoXUifhvYB65lLJCZ74o_fAk')

# playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

# print(len(playlist.video_urls))

# for url in playlist.video_urls:
#     print(url)

# for video in playlist.videos:
#     video.streams.get_highest_resolution().download()


# import re
# from pytube import Playlist

# YOUTUBE_STREAM_AUDIO = '140' # modify the value to download a different stream
# DOWNLOAD_DIR = 'D:\\Users\\Jean-Pierre\\Downloads'

# playlist = Playlist('https://www.youtube.com/playlist?list=PLzwWSJNcZTMSW-v1x6MhHFKkwrGaEgQ-L')

# # this fixes the empty playlist.videos list
# playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

# print(len(playlist.video_urls))

# for url in playlist.video_urls:
#     print(url)

# # physically downloading the audio track
# for video in playlist.videos:
#     audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
#     audioStream.download(output_path=DOWNLOAD_DIR)
