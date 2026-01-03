import os
import time
import random
import requests
from datetime import datetime

# Configuration
APP1_URL = os.getenv("APP1_URL", "http://localhost:5001")
SEND_INTERVAL = int(os.getenv("SEND_INTERVAL", "30"))  # seconds

def generate_random_data():
    """Generate random data to send to app1"""
    data_types = ["temperature", "humidity", "pressure", "cpu_usage", "memory_usage"]
    selected_type = random.choice(data_types)
    
    return {
        "id": random.randint(1000, 9999),
        "type": selected_type,
        "value": round(random.uniform(10.0, 100.0), 2),
        "unit": "%" if "usage" in selected_type else "°C",
        "timestamp": datetime.now().isoformat(),
        "sensor_id": f"sensor_{random.randint(1, 10)}"
    }

def send_data_to_app1():
    """Send data to app1"""
    try:
        data = generate_random_data()
        response = requests.post(
            f"{APP1_URL}/data", 
            json=data, 
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✓ Data sent successfully: {data}")
            return True
        else:
            print(f"✗ Failed to send data. Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error sending data: {str(e)}")
        return False

def main():
    """Main loop for sending data periodically"""
    print(f"📡 Starting data sender...")
    print(f"📡 Target URL: {APP1_URL}")
    print(f"📡 Send interval: {SEND_INTERVAL} seconds")
    
    total_sent = 0
    errors = 0
    
    # Wait a bit for app1 to be ready
    print("⏳ Waiting 10 seconds for app1 to be ready...")
    time.sleep(10)
    
    while True:
        try:
            if send_data_to_app1():
                total_sent += 1
            else:
                errors += 1
                
            print(f"📊 Stats - Total sent: {total_sent}, Errors: {errors}")
            
        except KeyboardInterrupt:
            print("\n🛑 Data sender stopped by user")
            break
        except Exception as e:
            print(f"✗ Unexpected error: {str(e)}")
            errors += 1
            
        time.sleep(SEND_INTERVAL)
    
    print(f"📊 Final stats - Total sent: {total_sent}, Errors: {errors}")

if __name__ == "__main__":
    main()