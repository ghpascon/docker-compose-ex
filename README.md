# Docker Compose Multi-App Project

A professional demonstration of containerized microservices using Docker, Docker Compose, FastAPI, and Poetry. This project showcases three interconnected applications running in separate containers with health monitoring and automated data exchange.

## 🏗️ Architecture

This project consists of three microservices:

### 🏥 App1 - Health Monitor Service
- **Port**: 5001
- **Description**: FastAPI application with an elegant HTML interface displaying application health status
- **Features**: 
  - Real-time health monitoring dashboard
  - RESTful health check endpoint
  - Data reception endpoint for App3
  - Auto-refresh web interface

### 🔍 App2 - Verification Service  
- **Port**: 5002
- **Description**: API service that simulates real-world verification processes
- **Features**:
  - `/verification` endpoint returning success responses
  - Realistic verification simulation with processing delays
  - Request/response validation using Pydantic models
  - Error simulation for testing resilience

### 📡 App3 - Data Sender Service
- **Port**: 5003  
- **Description**: Background service that periodically sends random data to App1
- **Features**:
  - Configurable data sending intervals
  - Random sensor data generation
  - Statistics and monitoring endpoints
  - Manual start/stop controls

## 🛠️ Technology Stack

- **Python**: 3.11
- **Framework**: FastAPI
- **Dependency Management**: Poetry
- **Containerization**: Docker & Docker Compose
- **Web Server**: Uvicorn
- **Health Monitoring**: Built-in health checks
- **Networking**: Docker bridge networks

## 📁 Project Structure

```
docker_ex/
├── app1/                     # Health Monitor Service
│   ├── templates/
│   │   └── index.html       # Health dashboard UI
│   ├── Dockerfile
│   ├── main.py
│   └── pyproject.toml
├── app2/                     # Verification Service
│   ├── Dockerfile
│   ├── main.py
│   └── pyproject.toml
├── app3/                     # Data Sender Service
│   ├── Dockerfile
│   ├── main.py
│   └── pyproject.toml
├── docker-compose.yml        # Multi-service orchestration
├── Makefile                  # Development shortcuts
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Docker Desktop
- Docker Compose
- Make (optional, for shortcuts)

### Running the Application

1. **Clone and navigate to the project**:
   ```bash
   git clone https://github.com/ghpascon/docker-compose-ex
   cd docker_ex
   ```

2. **Start all services**:
   ```bash
   # Using Docker Compose
   docker-compose up -d --build
   
   # Or using Make
   make up
   ```

3. **Access the applications**:
   - **App1 Dashboard**: http://localhost:5001
   - **App2 API**: http://localhost:5002
   - **App3 Monitor**: http://localhost:5003

### 🔧 Available Commands

```bash
# Build all images
make build

# Start services
make up

# View logs
make logs

# Check health status
make health

# Stop services
make down

# Complete cleanup
make clean
```

## 📊 Health Monitoring

All services include comprehensive health checks:

- **Endpoint**: `/health` on each service
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3 attempts
- **Start Period**: 40 seconds

## 🌐 API Endpoints

### App1 (Port 5001)
- `GET /` - Health dashboard (HTML)
- `GET /health` - Health check (JSON)
- `POST /data` - Receive data from App3

### App2 (Port 5002)
- `GET /` - Service information
- `GET /health` - Health check
- `GET /verification` - Simple verification
- `POST /verification` - Complex verification with request body

### App3 (Port 5003)
- `GET /` - Service information
- `GET /health` - Health check with sender statistics
- `GET /stats` - Detailed sending statistics
- `POST /start` - Start data sender
- `POST /stop` - Stop data sender

## ⚙️ Configuration

### Environment Variables

**App3 Configuration**:
- `APP1_URL`: Target URL for data sending (default: http://app1:5001)
- `SEND_INTERVAL`: Interval in seconds between data sends (default: 30)

### Docker Network

All services communicate through a dedicated bridge network (`docker_ex_network`) ensuring:
- Service isolation
- Internal DNS resolution
- Secure inter-service communication

## 📈 Monitoring & Observability

- **Health Checks**: Built-in Docker health checks for all services
- **Service Discovery**: Docker Compose DNS for service resolution
- **Logging**: Centralized logging via `docker-compose logs`
- **Statistics**: Real-time metrics available through REST endpoints

## 🔧 Development

### Local Development
```bash
# Start with live reloading
make dev

# View specific service logs
make logs-app1
make logs-app2  
make logs-app3
```

### Production Deployment
```bash
# Production mode
make prod
```

## 🧪 Testing

Test the complete workflow:

1. **Check all services are healthy**:
   ```bash
   make health
   ```

2. **Verify data flow**:
   - Visit App1 dashboard: http://localhost:5001
   - Check App3 statistics: http://localhost:5003/stats
   - Test verification: http://localhost:5002/verification

3. **Monitor logs**:
   ```bash
   make logs
   ```

## 🚨 Troubleshooting

- **Services not starting**: Check `docker-compose logs`
- **Health checks failing**: Ensure ports are not in use
- **Network issues**: Verify Docker daemon is running
- **Build failures**: Try `make clean` then `make build`

## 📜 License

This project is licensed under the terms specified in the LICENSE file.