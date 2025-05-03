from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(title="FairShare: Group Expense Tracker")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ← change to your frontend port if needed
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"]   # allow Content-Type and others
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)