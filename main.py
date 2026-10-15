import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. Strict CORS Policy
# Rejects all origins except the explicitly assigned one. No wildcards allowed[cite: 7].
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dash-ta491h.example.com"],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# 2. Forced Middleware Injection
# Wraps every request (including blocked CORS preflights) to ensure headers are always present[cite: 7].
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    
    return response

# 3. The Payload Endpoint
@app.get("/stats")
async def compute_stats(values: str):
    # Parse comma-separated integers[cite: 7]
    nums = [int(x.strip()) for x in values.split(",")]
    
    count = len(nums)
    total_sum = sum(nums)
    
    return {
        # Extracted from your active browser tab[cite: 7]
        "email": "24f3001311@ds.study.iitm.ac.in", 
        "count": count,
        "sum": total_sum,
        "min": min(nums),
        "max": max(nums),
        "mean": total_sum / count
    }