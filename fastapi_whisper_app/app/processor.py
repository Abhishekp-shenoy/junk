
import whisper
import torchaudio
import moviepy.editor as mp
from langdetect import detect
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy

whisper_model = whisper.load_model("large")
nlp = spacy.load("en_core_web_sm")
sid = SentimentIntensityAnalyzer()

def extract_audio(path):
    if path.endswith(".mp4"):
        audio_path = path.replace(".mp4", ".wav")
        mp.AudioFileClip(path).write_audiofile(audio_path)
        return audio_path
    return path

def process_file(path):
    audio_path = extract_audio(path)
    lang = detect(open(audio_path, 'rb').read(2048).decode(errors='ignore'))

    result = whisper_model.transcribe(audio_path, language=lang, verbose=True, word_timestamps=True, condition_on_previous_text=False)
    transcription = result['text']

    sentiment = sid.polarity_scores(transcription)
    doc = nlp(transcription)
    meds = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT"]]

    summary = f"Detected language: {lang}. Sentiment: {sentiment['compound']}. Mentioned: {', '.join(meds)}"

    return {
        "language": lang,
        "transcription": transcription,
        "translated": transcription,
        "sentiment": sentiment,
        "medicines": meds,
        "summary": summary
    }
