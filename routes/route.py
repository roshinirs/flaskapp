from flask import Flask, request

from services.routeservice import YoutubeService

app = Flask(__name__)


@app.route("/get_subtitles", methods=['POST'])
def get_subtitles():
    video_link = request.form.get("video_link")
    obj = YoutubeService()
    response = obj.get_subtitles(video_link)
    return response


@app.route('/get_summary/<video_id>')
def get_summary(video_id):
    obj = YoutubeService()
    response = obj.get_summary(video_id)
    return response


@app.route('/get_analysis/<video_id>')
def analyze_sentiment(video_id):
    obj = YoutubeService()
    response = obj.analyze_sentiment(video_id)
    return response
