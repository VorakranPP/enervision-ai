#!/bin/bash
source .venv/bin/activate
uvicorn backend.api:app --reload &
streamlit run dashboard/dashboard.py