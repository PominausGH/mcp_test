# app.py
from fastapi import FastAPI, HTTPException
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

GOOGLE_CSE_API_KEY = os.getenv("GOOGLE_CSE_API_KEY")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_CSE_ID")

@app.get("/search/")
async def search(query: str, num_results: int = 5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_CSE_API_KEY,
        "cx": GOOGLE_SEARCH_ENGINE_ID,
        "q": query,
        "num": num_results,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error in search API request")
    
    data = response.json()
    results = []
    for item in data.get("items", []):
        results.append({
            "title": item["title"],
            "snippet": item["snippet"],
            "link": item["link"]
        })

    return {"query": query, "results": results}