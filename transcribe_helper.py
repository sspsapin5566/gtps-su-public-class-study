import os
import sys
import whisper

def transcribe_file(audio_path, output_txt, output_srt):
    print(f"Loading model for {audio_path}...", flush=True)
    model = whisper.load_model("base")
    print(f"Transcribing {audio_path}...", flush=True)
    result = model.transcribe(audio_path, language="zh", verbose=True)
    
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    print(f"Done transcribing {audio_path} -> {output_txt}", flush=True)

if __name__ == "__main__":
    audio = sys.argv[1]
    out_txt = sys.argv[2]
    out_srt = sys.argv[3]
    transcribe_file(audio, out_txt, out_srt)
