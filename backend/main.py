"""PromptLab API Server

Run with: python main.py
"""

import uvicorn
from app.api import app

if __name__ == "__main__":
    # Pass the app object directly so the import is used (satisfies linters)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
