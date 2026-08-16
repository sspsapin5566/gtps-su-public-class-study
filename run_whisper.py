import os
import whisper

def transcribe(audio_path, txt_path, srt_path):
    print(f"Loading whisper model for {audio_path}...", flush=True)
    model = whisper.load_model("small")
    print(f"Transcribing {audio_path}...", flush=True)
    result = model.transcribe(
        audio_path,
        language="zh",
        condition_on_previous_text=False,
        initial_prompt="國小社會課公開課學生小組討論與教師說明："
    )
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"Finished {audio_path} -> {txt_path}", flush=True)

if __name__ == "__main__":
    import sys
    audio_file = sys.argv[1]
    out_txt = sys.argv[2]
    transcribe(audio_file, out_txt, out_txt.replace(".txt", ".srt"))
