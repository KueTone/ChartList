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

# Routes
@app.get("/")
async def api_entry():
    return {"Welcome": "Database API"}

@app.get("/block-values")
def get_block_values():
    data = query.query_block_value()
    return {"block_values": data}

@app.get("/top-affordable-places")
def get_top_affordable_places():
    """
    Fetch the top affordable places based on average price.
    """
    try:
        data = query.query_top_affordable_places()
        return {"top_affordable_places": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")


@app.get("/property-type-comparison")
def get_property_type_comparison():
    """
    Fetch a comparison of property types including their average price and number of listings.
    """
    try:
        data = query.query_property_type_comparison()
        return {"property_type_comparison": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

@app.get("/price-distribution-comparison")
def get_price_distribution_comparison():
    """
    Fetch price distribution for different property types in each state.
    """
    try:
        data = query.query_price_distribution_comparison()
        return {"price_distribution_comparison": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")


@app.get("/cheapest-areas")
def get_cheapest_areas():
    """
    Fetch the cheapest areas based on price per square meter.
    """
    try:
        data = query.query_cheapest_areas()
        return {"cheapest_areas": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

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
