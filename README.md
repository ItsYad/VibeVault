# 🎬 VibeVault
Platform Eksplorasi & Koleksi Entertainment Pribadi

## Tech Stack
- Frontend: Streamlit
- Backend: FastAPI + JWT Auth
- Database: SQLite
- Package Manager: pip / uv

## Cara Menjalankan

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
Backend berjalan di: http://localhost:8000
API Docs: http://localhost:8000/docs

### 2. Frontend (terminal baru)
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
Frontend berjalan di: http://localhost:8501

## Struktur Proyek
```
vibevault/
├── backend/
│   ├── main.py          # FastAPI app
│   ├── database.py      # SQLite setup & seed data
│   ├── auth_helper.py   # JWT & bcrypt helper
│   ├── requirements.txt
│   └── routes/
│       ├── auth.py      # Register & Login
│       ├── items.py     # Katalog & Surprise Me
│       ├── collection.py # Koleksi user
│       └── moodboard.py # Moodboard personal
└── frontend/
    ├── app.py           # Streamlit UI
    └── requirements.txt
```

## Fitur
- 🔐 Register & Login dengan JWT
- 🧬 Kuis selera → Badge unik
- 🔍 Discovery katalog film & musik
- 🎲 Surprise Me! (random challenge)
- 📚 Koleksi & pin item favorit
- 🎨 Personal Moodboard
