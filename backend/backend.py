from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import uvicorn
from google.cloud import bigquery
from mysql.connector import connect, Error
import query #databse connection

# Load environment variables
load_dotenv()

# FastAPI app initialization
app = FastAPI()

# Configure CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
}

# Utility function to get database connection
def get_db_connection():
    try:
        conn = connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed.")

# Query BigQuery
def query_block_value():
    client = bigquery.Client()
    query = """
    SELECT *
    FROM `bigquery-public-data.us_res_real_est_data.block_value`
    LIMIT 10
    """
    query_job = client.query(query)
    return [dict(row) for row in query_job]

# Routes
@app.get("/")
async def api_entry():
    return {"Welcome": "Database API"}

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    return {"Function": "Function"}

@app.get("/block-values")
def get_block_values():
    data = query_block_value()
    return {"block_values": data}

# Main function
def main():
    try:
        HOST = os.getenv("HOST", "127.0.0.1")
        PORT = int(os.getenv("PORT", 8000))
    except Exception as e:
        print(f"Error: {e}")
        exit(2)
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")

if __name__ == "__main__":
    main()
