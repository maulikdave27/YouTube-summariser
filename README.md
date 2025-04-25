# Flask Backend for YouTube Transcript Summarizer

This is the backend code for the **YouTube Transcript Summarizer** project. It is a Flask-based web server that integrates with the Gemini API for summarization and Google Translate API for translations. It also includes session-based login, transcript processing, and download features.

---

## 📌 Features

- 🔑 Simple session-based login
- 🎥 YouTube transcript extraction
- ✍️ Gemini-powered summarization (10-point summary)
- 🌍 Translate summary into multiple languages using Google Translate
- 💾 Download summaries as `.txt` files
- 🕓 Search history saved per user session

---

## ⚙️ Tech Stack

- Flask (Python)
- Google Gemini API
- `youtube-transcript-api`
- `googletrans` for translation
- `python-dotenv` for API key management

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- `pip`
- Google Gemini API key

### Installation
```bash
git clone https://github.com/your-username/youtube-transcript-summarizer.git
cd youtube-transcript-summarizer
pip install -r requirements.txt
```

### Environment Setup
Create a `.env` file with the following:
```env
GOOGLE_API_KEY=your_gemini_api_key
```

### Run the Server
```bash
python app.py
```
Visit: [http://localhost:5000](http://localhost:5000)

---

## 📁 File Overview

- `app.py` - Main Flask app with all endpoints
- `templates/` - HTML templates for login and main UI
- `static/` - CSS and JS files (if any)

---

## 🔐 Auth
A mock in-memory user database is used:
```python
users = {"abc": "123"}
```
Modify as needed or integrate with a real auth system.

---

## 📬 API Endpoints

### `/` [GET, POST]  
Login page with session-based authentication.

### `/home` [GET]  
Main app interface after login.

### `/summarize` [POST]  
Accepts JSON `{"url": "<YouTube_URL>"}` and returns a Gemini-generated summary.

### `/translate` [POST]  
Accepts JSON `{"summary": "text", "language": "hi"}` and returns the translated summary.

### `/download` [POST]  
Returns a downloadable `.txt` file of the summary.

### `/logout` [GET]  
Clears session and redirects to login.

---

## 🔮 To Do / Improvements

- [ ] Secure login with hashed passwords
- [ ] OAuth (Google/GitHub)
- [ ] Video/audio upload for summarization
- [ ] Real-time transcript fetching progress

---

## 📜 License
[MIT](LICENSE)

---

## 👨‍💻 Author
Created by [Maulik](https://github.com/your-username)

---

