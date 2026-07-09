import os
import streamlit as st 
import subprocess
from datetime import timedelta
import whisper
import srt
from moviepy import VideoFileClip

def extractaudio(video_path,audio_path):
    try:
        video=VideoFileClip(video_path)
        audio=video.audio
        if audio:
            audio.write_audiofile(audio_path)
            return True
        else:
            st.error("no audio track found in the video")
            return False
    except Exception as e:
        st.error(f"an error occured {str(e)}")
        return False
def transcribe(audio_path):
    try:

        model=whisper.load_model("base")
        result=model.transcribe(audio_path)
        return result
    except Exception as e:
        st.error(f"error transcribing audio {e}")
        return None
def convert_to_srt(transcription_result):
    try:

        subtitles=[]
        for i,seg in enumerate(transcription_result.get("segments",[])):
            
            subtitle=srt.Subtitle(
                index=i+1,
                start=timedelta(seconds=seg["start"]),
                end=timedelta(seconds=seg["end"]),
                content=seg["text"].strip()


            )
            subtitles.append(subtitle)
        return srt.compose(subtitles)
    except Exception as e:
        st.error(f"error  generating  srt: {e}")
        return ""

def burn_subtitles(video_path,srt_path,output_path,ffmpeg_path):
    video_full=os.path.abspath(video_path)
    output_full=os.path.abspath(output_path)

    command=f'"{ffmpeg_path}" -i "{video_full}" -vf "subtitles={srt_path}" "{output_full}"'
    

    try:
        subprocess.run(command,shell=True,check=True)
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"error burning subtitles: {e}")
        return False
def main():
    st.title("Youtube Auto Captions Generator")
    st.write("upload video to generate captions")
    video_file=st.file_uploader("upload video",type=["mp4","avi","mov"])
    if video_file:
        video_path="video/video_file.mp4"
        os.makedirs("video",exist_ok=True)
        with open(video_path,"wb") as f:
            f.write(video_file.getbuffer())
        st.video(video_path)

        if st.button("generate  caption"):
            os.makedirs("audio",exist_ok=True)
            audio_path="audio/upload_audio.wav"
            st.write("extracting audio")
            if not extractaudio(video_path,audio_path):
                return
            st.write("transcribing audio")
            transcription_result=transcribe(audio_path)
            if not transcription_result:
                return
            st.write("transcribing result")
            st.write(transcription_result.get("text",""))

            srt_content=convert_to_srt(transcription_result)
            os.makedirs("captions",exist_ok=True)
            srt_path="captions/out_srt.srt"

            with open(srt_path,"w",encoding="utf-8")as f:
                f.write(srt_content)
            st.success("SRT file generated")

            ffmpeg_path=r"C:\Users\Aryan\Downloads\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"
            st.write("burning captions")
            if burn_subtitles(video_path,srt_path,"video/output_video.mp4",ffmpeg_path):
                st.success("captions burned")
                st.video("video/output_video.mp4")
                
if __name__=="__main__":
    main()

            
        


    
           

