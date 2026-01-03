import os
import time
import threading
import requests
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="App1 Health Monitor", version="1.0.0")

# Configuration
APP2_URL = os.getenv("APP2_URL", "http://localhost:5002")
CALL_INTERVAL = int(os.getenv("CALL_INTERVAL", "45"))  # seconds

# Get current directory for templates
current_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

class App2Caller:
    def __init__(self):
        self.running = False
        self.last_called = None
        self.total_calls = 0
        self.successful_calls = 0
        self.errors = 0
        self.last_response = None
        self.received_data = []

    def call_app2_verification(self):
        """Call app2 verification endpoint periodically"""
        while self.running:
            try:
                # Call the verification endpoint
                response = requests.get(
                    f"{APP2_URL}/verification", 
                    timeout=10
                )
                
                self.total_calls += 1
                self.last_called = datetime.now().isoformat()
                
                if response.status_code == 200:
                    self.successful_calls += 1
                    self.last_response = response.json()
                    print(f"✓ App2 verification successful: {self.last_response}")
                else:
                    self.errors += 1
                    print(f"✗ App2 verification failed. Status: {response.status_code}")
                    
            except Exception as e:
                self.total_calls += 1
                self.errors += 1
                print(f"✗ Error calling App2: {str(e)}")
            
            time.sleep(CALL_INTERVAL)

    def start(self):
        """Start calling app2 periodically"""
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self.call_app2_verification, daemon=True)
            thread.start()
            print(f"📞 App2 caller started. Calling every {CALL_INTERVAL} seconds to {APP2_URL}")

    def stop(self):
        """Stop calling app2"""
        self.running = False
        print("🛑 App2 caller stopped")

    def add_received_data(self, data):
        """Add received data from app3 to the list (keep last 10)"""
        self.received_data.append({
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last 10 items
        if len(self.received_data) > 10:
            self.received_data = self.received_data[-10:]

# Global app2 caller instance
app2_caller = App2Caller()

@app.on_event("startup")
async def startup_event():
    """Start app2 calling when the app starts"""
    # Wait a bit for app2 to be ready
    def delayed_start():
        time.sleep(15)  # Wait 15 seconds for app2 to be ready
        app2_caller.start()
    
    thread = threading.Thread(target=delayed_start, daemon=True)
    thread.start()

@app.on_event("shutdown")
async def shutdown_event():
    """Stop app2 calling when the app shuts down"""
    app2_caller.stop()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Main page showing application health status"""
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "app_name": "App1 Health Monitor", 
            "status": "healthy",
            "app2_stats": {
                "running": app2_caller.running,
                "total_calls": app2_caller.total_calls,
                "successful_calls": app2_caller.successful_calls,
                "errors": app2_caller.errors,
                "last_called": app2_caller.last_called,
                "last_response": app2_caller.last_response
            },
            "received_data": app2_caller.received_data[-5:]  # Last 5 items
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy", 
        "service": "app1", 
        "port": 5001,
        "app2_caller_active": app2_caller.running,
        "app2_stats": {
            "total_calls": app2_caller.total_calls,
            "successful_calls": app2_caller.successful_calls,
            "errors": app2_caller.errors,
            "last_called": app2_caller.last_called
        }
    }

@app.get("/app2-stats")
async def get_app2_stats():
    """Get detailed statistics about app2 calls"""
    return {
        "running": app2_caller.running,
        "total_calls": app2_caller.total_calls,
        "successful_calls": app2_caller.successful_calls,
        "errors": app2_caller.errors,
        "success_rate": round((app2_caller.successful_calls / app2_caller.total_calls * 100), 2) if app2_caller.total_calls > 0 else 0,
        "last_called": app2_caller.last_called,
        "last_response": app2_caller.last_response,
        "target_url": APP2_URL,
        "call_interval": CALL_INTERVAL
    }

@app.post("/data")
async def receive_data(data: dict):
    """Endpoint to receive data from app3"""
    print(f"Received data from App3: {data}")
    app2_caller.add_received_data(data)
    return {"status": "success", "message": "Data received successfully"}

@app.post("/start-app2-caller")
async def start_app2_caller():
    """Manually start the app2 caller"""
    app2_caller.start()
    return {"message": "App2 caller started", "status": "running"}

@app.post("/stop-app2-caller")
async def stop_app2_caller():
    """Manually stop the app2 caller"""
    app2_caller.stop()
    return {"message": "App2 caller stopped", "status": "stopped"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)