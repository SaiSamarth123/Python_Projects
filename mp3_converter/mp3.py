from pytube import YouTube, Playlist
from moviepy.editor import *
import os
import re


def download_video(url):
    try:
        youtube = YouTube(url)
    except Exception as e:
        print(f"Could not download the video. Reason: {e}")
        return None

    video = youtube.streams.first()
    out_file = video.download()
    return out_file


def convert_to_mp3(file_path):
    try:
        mp3_file_path = re.sub(r"\.[^.]+$", ".mp3", file_path)
        mp3_file_path = os.path.join("music", os.path.basename(mp3_file_path))
        videoclip = VideoFileClip(file_path)
        audioclip = videoclip.audio
        audioclip.write_audiofile(mp3_file_path)
        audioclip.close()
        videoclip.close()
    except Exception as e:
        print(f"Could not convert video to mp3. Reason: {e}")
        return None

    return mp3_file_path


def main():
    playlist_url = input(
        "https://www.youtube.com/playlist?list=PLJ3JH9y4QeIh5KQtl_O5tAbpPH_022l_T "
    )

    if not os.path.exists("music"):
        os.makedirs("music")

    playlist = Playlist(playlist_url)
    failed_downloads = []

    for url in playlist.video_urls:
        file_path = download_video(url)
        if file_path is not None:
            mp3_file_path = convert_to_mp3(file_path)
            if mp3_file_path is not None:
                print(
                    f"Successfully converted video to mp3. File saved at: {mp3_file_path}"
                )
            else:
                print("Could not convert video to mp3.")

            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Could not remove original video file. Reason: {e}")

        else:
            failed_downloads.append(url)

    if len(failed_downloads) > 0:
        print("\nFailed to download the following videos:")
        for url in failed_downloads:
            print(url)


if __name__ == "__main__":
    main()
