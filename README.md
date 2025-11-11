# 🔗 FastAPI URL Shortener

A simple RESTful API built with **FastAPI** and **SQLite** that lets you shorten long URLs, track click stats, and manage links.

🌍 **Live Demo:**  
[https://url-shortener-1-bqsr.onrender.com/](https://url-shortener-1-bqsr.onrender.com/)

## 🚀 Features
- Create short URLs
- Redirect to original links
- Track number of clicks
- Update or delete short links
- Simple HTML frontend with copy + stats

## 🧠 Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Then open http://127.0.0.1:8000