import os
import random
import time
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="App2 Verification Service", version="1.0.0")

# Models
class VerificationRequest(BaseModel):
    token: Optional[str] = None
    user_id: Optional[str] = None

class VerificationResponse(BaseModel):
    success: bool
    message: str
    timestamp: str
    request_id: str

@app.get("/")
async def read_root():
    """Root endpoint with service information"""
    return {
        "service": "App2 Verification Service",
        "version": "1.0.0",
        "port": 5002,
        "endpoints": ["/verification", "/health"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy", 
        "service": "app2", 
        "port": 5002,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/verification", response_model=VerificationResponse)
async def verify_request(request: VerificationRequest):
    """
    Verification endpoint that simulates a real API verification process
    Returns success with high probability to simulate a working service
    """
    # Simulate processing time
    time.sleep(random.uniform(0.1, 0.5))
    
    # Generate a random request ID
    request_id = f"req_{random.randint(100000, 999999)}"
    
    # Simulate occasional failures (5% chance)
    if random.random() < 0.05:
        raise HTTPException(
            status_code=400, 
            detail="Verification failed: Invalid request parameters"
        )
    
    return VerificationResponse(
        success=True,
        message="Verification completed successfully",
        timestamp=datetime.now().isoformat(),
        request_id=request_id
    )

@app.get("/verification")
async def verify_get():
    """GET endpoint for simple verification checks"""
    return {
        "success": True,
        "message": "Verification service is operational",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)