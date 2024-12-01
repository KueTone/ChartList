# keep in alphabetical order to keep it clean
from dotenv import load_dotenv
import googleapiclient
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import uvicorn
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
}

load_dotenv()

app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow credentials (e.g., cookies, authorization headers)
    allow_methods=["*"],    # Specify allowed HTTP methods (or use wildcard "*")
    allow_headers=["*"],    # Specify allowed HTTP headers (or use wildcard "*")
)

# Utility function to get database connection
def get_db_connection():
    try:
        conn = connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed.")


@app.get("/")
async def api_entry():
    return {"Welcome": "AutomatedCaller API"}

# Endpoint to handle CSV upload
@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    return {"Function": "Function"}

def main():
    try:
        HOST = os.getenv("HOST")
        PORT = int(os.getenv("PORT"))
    except Exception:
        print(
            "Error: Please make sure you have set the HOST and PORT environment variables correctly."
        )
        exit(2)
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info",
        
    )


if __name__ == "__main__":
    main()
