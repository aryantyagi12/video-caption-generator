import subprocess
import os 

def burn_subtitles(video_path,srt_path,output_path,ffmpeg_path):
    video_full=os.path.abspath(video_path)
    output_full=os.path.abspath(output_path)

    command=f'"{ffmpeg_path}" -i "{video_full}" -vf "subtitles={srt_path}" "{output_full}"'
    print("path is running")
    print(command)

    try:
        subprocess.run(command,shell=True,check=True)
        print(f"[✅] video with burn in caption generated:{output_full}")
    except subprocess.CalledProcessError as e:
        print(f"[Error] could not burn subtitles:{e}")
if __name__=="__main__":
    video_path="video/video.mp4"
    srt_path="srt_output/output.srt"
    output_path="video/output.mp4"
    ffmpeg_path=r"C:\Users\Aryan\Downloads\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

    burn_subtitles(video_path,srt_path,output_path,ffmpeg_path)
