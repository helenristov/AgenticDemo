Call Center AI Demo (Azure + LangChain)

Run backend:
  cd backend
  pip install -r requirements.txt
  uvicorn app.main:app --reload

Run frontend:
  cd frontend
  pip install -r requirements.txt
  streamlit run streamlit_app.py
