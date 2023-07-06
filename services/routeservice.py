from flask import jsonify, redirect, url_for
from googletrans import Translator
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable, NoTranscriptFound

from server.server import ServerSession


class YoutubeService(ServerSession):

    def __init__(self):
        super().__init__()

    def get_subtitles(self, video_link):
        print(video_link)
        video_id = str(video_link).split('/')
        video_id = video_id[-1]
        if '=' in video_id:
            video_id = video_id.split('=')[-1]
        if not video_id[0].isalpha():
            video_id = video_id[1:]
        print(video_id)
        try:
            subtitle = YouTubeTranscriptApi.get_transcript(video_id)
            paragraph = ""
            for word in subtitle:
                text = word["text"]
                if text != "[Music]":
                    paragraph += text + " "
            print(paragraph)
            data = self.dbconnect.output.find_one({'_id': video_id}, {'_id': 1})
            if not data:
                transcript = {"_id": video_id, "Transcript": paragraph}
                db_response = self.dbconnect.output.insert_one(transcript)
                response = jsonify({"Message": "New Transcript added", "_id": db_response.inserted_id})
            else:
                response = jsonify({"Message": "Transcript already exists", "_id": video_id})
            # print(response)
            return redirect(url_for('auth.index'))

        except (TranscriptsDisabled, VideoUnavailable, NoTranscriptFound):
            response = jsonify({"error": "Could not retrieve a transcript for the video"}), 400
            print(response)
            return redirect(url_for('auth.index'))

        except Exception as err:
            response = jsonify({"error": "An error occurred while processing the video", "cause": err}), 500
            print(response)
            return redirect(url_for('auth.index'))

    def get_summary(self, video_id):
        summarizer = pipeline('summarization', model="facebook/bart-large-cnn")
        text = self.dbconnect.output.find_one({'_id': video_id})
        summary = summarizer(text['Transcript'][:1023],
                             max_length=150, min_length=30, do_sample=False)[0]['summary_text']
        self.dbconnect.output.update_one({'_id': video_id}, {'$set': {'Summary': summary}})
        response = jsonify({"Message": "summary added"})
        print(response)
        text = self.dbconnect.output.find_one({'_id': video_id})
        return jsonify(({"Summary": f"{text['Summary']}"}))

    def analyze_sentiment(self, video_id):
        text = self.dbconnect.output.find_one({'_id': video_id})
        classifier = pipeline("sentiment-analysis")
        results = classifier(text['Summary'])
        sentiment = results[0]['label']
        return jsonify({"sentiment": sentiment, "word count": len(text['Transcript'])})
