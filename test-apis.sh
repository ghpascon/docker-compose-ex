# API Testing with curl

## App1 - Health Monitor Service (Port 5001)

# Get health dashboard (HTML)
curl http://localhost:5001/

# Health check (JSON)
curl http://localhost:5001/health

# Get App2 call statistics
curl http://localhost:5001/app2-stats

# Manually start App2 caller
curl -X POST http://localhost:5001/start-app2-caller

# Manually stop App2 caller
curl -X POST http://localhost:5001/stop-app2-caller

# Send test data (simulate App3)
curl -X POST http://localhost:5001/data \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1234,
    "type": "temperature",
    "value": 23.5,
    "unit": "°C",
    "timestamp": "2025-01-03T10:00:00",
    "sensor_id": "sensor_1"
  }'

## App2 - Verification Service (Port 5002)

# Service information
curl http://localhost:5002/

# Health check
curl http://localhost:5002/health

# Simple verification (GET)
curl http://localhost:5002/verification

# Complex verification (POST)
curl -X POST http://localhost:5002/verification \
  -H "Content-Type: application/json" \
  -d '{
    "token": "test-token-123",
    "user_id": "user-456"
  }'

## App3 - Data Sender Service (Background Process)

# App3 now runs as a simple background process that sends data to App1
# No API endpoints available - check App1 to see received data
# Monitor logs with: docker-compose logs -f app3