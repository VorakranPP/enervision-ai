##Terminal 1:
source .venv/bin/activate
uvicorn backend.api:app --reload
##(หลังบ้าน)
Terminal 2:
source .venv/bin/activate
streamlit run dashboard/dashboard.py
##(หน้าบ้าน)
http://127.0.0.1:8000/docs
kill -9 $(lsof -ti :8000)