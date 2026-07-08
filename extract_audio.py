from moviepy import VideoFileClip

import os

def extractaudio(video_path,audio_path):
    try:
        video=VideoFileClip(video_path)
        audio=video.audio
        if audio:
            audio.write_audiofile(audio_path)
            print(f"audio is extracted")
        else:
            print("no audio in the video")
    except Exception as e:
        print(f"error extracting audio {e}")


if __name__=="__main__":
    video_file="video/video.mp4"
    output_file="audio/sample_audio2.wav"

    os.makedirs(os.path.dirname(output_file),exist_ok=True)

    extractaudio(video_file,output_file)