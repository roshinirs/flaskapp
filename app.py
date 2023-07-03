from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable, NoTranscriptFound
from transformers import pipeline
from googletrans import Translator

app = Flask(__name__)

storage = {}


@app.route("/")
def home():
    return "This is home page"


@app.route("/get_subtitles", methods=['POST'])
def get_subtitles():
    video_link = request.form.get("video_link")

    video_id = str(video_link).split('/')
    video_id = video_id[-1]
    if '=' in video_id:
        video_id = video_id.split('=')[-1]
    if not video_id[0].isalpha():
        video_id = video_id[1:]
    try:
        subtitle = YouTubeTranscriptApi.get_transcript(video_id)
        paragraph = ""
        for word in subtitle:
            text = word["text"]
            if text != "[Music]":
                paragraph += text + " "
        storage["Transcript"] = paragraph
        response = jsonify({"Transcript": paragraph})
        return response

    except (TranscriptsDisabled, VideoUnavailable, NoTranscriptFound):
        return jsonify({"error": "Could not retrieve a transcript for the video"}), 400

    except Exception:
        return jsonify({"error": "An error occurred while processing the video"}), 500


@app.route('/get_summary')
def get_summary():
    summarizer = pipeline('summarization', model="facebook/bart-large-cnn")
    summary = summarizer(storage.get("Transcript"), max_length=150, min_length=30, do_sample=False)[0]['summary_text']
    storage["Summary"] = summary
    return jsonify({'summary': summary})


@app.route('/get_translate')
def translate_english_to_tamil():
    translator = Translator(service_urls=['translate.google.com'])
    translated_text = translator.translate(storage.get("Transcript"), src='en', dest='ta')
    return jsonify({'Tamil': translated_text.text})


@app.route('/get_analysis')
def analyze_sentiment():
    classifier = pipeline("sentiment-analysis")
    results = classifier(storage.get("Summary"))
    sentiment = results[0]['label']
    return jsonify({"sentiment": sentiment, "word count": len(storage.get("Transcript"))})


if __name__ == "__main__":
    app.run(port=8080, debug=True)
