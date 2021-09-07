from pytube import YouTube
import os
def dl(url):
    # url input from user
    yt = YouTube(url)
    # extract only audio
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path='./audio/')
    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = '1' + '.mp3'
    os.rename(out_file, new_file)

os.remove('1.mp3')