"""Start the OrgChem Studio web interface on http://127.0.0.1:8131 (local only).

    pip install -r requirements-web.txt
    python run_web.py

Seeds a private temporary copy of the app's database on start-up (a few seconds); your desktop-app database is
never touched.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("orgchem.web.app:app", host="127.0.0.1", port=8131)
