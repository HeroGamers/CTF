from fastapi import FastAPI, Query, HTTPException
import pandas as pd

app = FastAPI()

CSV_FILE = "ctf_results.csv"
try:
    df = pd.read_csv(CSV_FILE)
except Exception as e:
    raise RuntimeError(f"Failed to load CSV: {e}")

@app.get("/")
def home():
    return {"message": "Welcome to the CTF Results API! Use /query?filter=QUERY to search. For example: /query?filter=Points>200"}

@app.get("/query")
def query_dataframe(filter: str = Query(..., description="Enter a pandas query string", max_length=40)):
    try:
        result = df.query(filter)
        return result.to_dict(orient="records")  # Convert to JSON format
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid query: {str(e)}")