# Docker Compose Commands for Multi-App Project

.PHONY: help build up down logs clean restart health status

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build all Docker images
	docker-compose build --no-cache

up: ## Start all services
	docker-compose up -d --build

down: ## Stop all services
	docker-compose down

logs: ## Show logs from all services
	docker-compose logs -f

logs-app1: ## Show logs from app1 only
	docker-compose logs -f app1

logs-app2: ## Show logs from app2 only
	docker-compose logs -f app2

logs-app3: ## Show logs from app3 only
	docker-compose logs -f app3

clean: ## Remove containers, networks, and images
	docker-compose down -v --rmi all --remove-orphans

restart: ## Restart all services
	docker-compose restart

health: ## Check health status of all services
	@echo "Checking health status..."
	@curl -s http://localhost:5001/health | jq . || echo "App1 not responding"
	@curl -s http://localhost:5002/health | jq . || echo "App2 not responding"
	@curl -s http://localhost:5003/health | jq . || echo "App3 not responding"

status: ## Show running containers
	docker-compose ps

dev: ## Start services for development
	docker-compose up --build

prod: ## Start services in production mode
	docker-compose -f docker-compose.yml up -d --build