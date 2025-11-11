from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import string, random
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from database import SessionLocal, engine, Base
from models import URL
from schemas import URLCreate, URLInfo

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener API")

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html at root
@app.get("/", include_in_schema=False)
def serve_home():
    return FileResponse(Path("static/index.html"))

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to generate short code
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# --------------------------
# POST /shorten
# --------------------------
@app.post("/shorten", response_model=URLInfo)
def create_short_url(url: URLCreate, db: Session = Depends(get_db)):
    short_code = generate_short_code()
    # Ensure unique short_code
    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()
    new_url = URL(short_code=short_code, long_url=url.long_url)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

# --------------------------
# GET /{short_code} (redirect)
# --------------------------
@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if url:
        url.clicks += 1
        db.commit()
        return RedirectResponse(url.long_url)
    raise HTTPException(status_code=404, detail="Short URL not found")

# --------------------------
# GET /stats/{short_code}
# --------------------------
@app.get("/stats/{short_code}", response_model=URLInfo)
def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if url:
        return url
    raise HTTPException(status_code=404, detail="Short URL not found")

# --------------------------
# PUT /update/{short_code}
# --------------------------
@app.put("/update/{short_code}", response_model=URLInfo)
def update_url(short_code: str, updated: URLCreate, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if url:
        url.long_url = updated.long_url
        db.commit()
        db.refresh(url)
        return url
    raise HTTPException(status_code=404, detail="Short URL not found")

# --------------------------
# DELETE /delete/{short_code}
# --------------------------
@app.delete("/delete/{short_code}")
def delete_url(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if url:
        db.delete(url)
        db.commit()
        return {"detail": "Short URL deleted"}
    raise HTTPException(status_code=404, detail="Short URL not found")
