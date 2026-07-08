import whisper

def transcribe(audio_path):
    model=whisper.load_model("base")
    result=model.transcribe(audio_path)
    print("/n transcription result")
    print(result["text"])
    print(result["language"])
    return result
if __name__=="__main__":
    audio_path="audio/sample_audio2.wav"
    transcribe(audio_path)