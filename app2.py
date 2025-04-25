from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime
from io import BytesIO
from googletrans import Translator
import os
from dotenv import load_dotenv


app = Flask(__name__)
app.secret_key = "super-secret-mock-key"  # Replace with any string for mock purposes

# Configure Gemini
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Simple user db for demo
users = {"abc": "123"}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        if users.get(username) == password:
            session['user'] = username
            session.setdefault('history', [])
            return redirect(url_for('index'))
        return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html")


@app.route('/home')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("index.html", history=session.get("history", []))

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        if 'user' not in session:
            return jsonify({"error": "Unauthorized"}), 401

        url = request.json.get("url")
        if not url:
            return jsonify({"error": "URL not provided"}), 400

        # Extract video ID
        if "v=" in url:
            video_id = url.split("v=")[-1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[-1].split("?")[0]
        else:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        srt = YouTubeTranscriptApi.get_transcript(video_id)
        subtitle = " ".join([x['text'] for x in srt])

        prompt = (
            "JOB: Summarizer\n"
            "RULES: Grammar should be proper. No explicit language. "
            "Provide a 10-point summary. \n"
            "FORMAT: Title:Content (no bold)\n"
            f"Subtitle: {subtitle}"
        )

        response = model.generate_content(prompt)
        summary = response.text

        # Save history
        session['history'].append({
            "url": url,
            "summary": summary,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        session.modified = True

        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    content = request.json.get("summary")
    if not content:
        return jsonify({"error": "No summary to download"}), 400
    buffer = BytesIO()
    buffer.write(content.encode('utf-8'))
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="summary.txt", mimetype='text/plain')

@app.route('/translate', methods=['POST'])
def translate_summary():
    data = request.json
    text = data.get('summary')
    target_lang = data.get('language', 'hi')  # Default to Hindi

    if not text:
        return jsonify({'error': 'No summary provided'}), 400

    try:
        translator = Translator()
        translated = translator.translate(text, dest=target_lang)
        return jsonify({'translated': translated.text}) 
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
